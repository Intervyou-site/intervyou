import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import CategoryGrid from './CategoryGrid'
import QuestionCard from './QuestionCard'
import Sidebar from './Sidebar'

const COMPANIES = [
  "Google", "Amazon", "Microsoft", "Meta (Facebook)", "Apple",
  "NVIDIA", "Twitter (X)", "IBM", "Oracle"
]

const CATEGORIES = [
  "Banking Interview / Aptitude",
  "HR Interview / Behavioral",
  "Aptitude / Quant",
  "Technical (Frontend)",
  "Technical (Backend)",
  "Technical (Data / DevOps)",
  "AI / ML",
  "Data Science",
  "System Design",
  "DevOps / SRE",
  "Case / Consulting",
  "Product Management",
  "Finance / Banking",
  "Campus / Fresher (HR Aptitude)",
  "Communication & Presentation",
  "Situational / Leadership",
  "Security / InfoSec",
  "Embedded Systems",
  "Sales & Marketing",
  "Customer Success / Support",
  "Design / UX",
  "Quality Assurance / Testing"
]

export default function PracticePage() {
  const [started, setStarted] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedCompany, setSelectedCompany] = useState('')
  const [question, setQuestion] = useState('Loading...')
  const [answerText, setAnswerText] = useState('')
  const [feedback, setFeedback] = useState('')
  const [score, setScore] = useState(null)
  const [timeLeft, setTimeLeft] = useState(150)
  const [progress, setProgress] = useState(0)
  const [recording, setRecording] = useState(false)
  const [transcribing, setTranscribing] = useState(false)
  const [questionSaved, setQuestionSaved] = useState(false)
  const [difficulty, setDifficulty] = useState('beginner')
  const [questionsAtLevel, setQuestionsAtLevel] = useState(0)
  
  const timerRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])

  useEffect(() => {
    loadInitialQuestion()
    return () => clearTimer()
  }, [])

  const clearTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }

  const startTimer = () => {
    clearTimer()
    setTimeLeft(150)
    setProgress(0)
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        const newTime = prev - 1
        setProgress(Math.round(100 * (150 - newTime) / 150))
        if (newTime <= 0) {
          clearTimer()
        }
        return Math.max(0, newTime)
      })
    }, 1000)
  }

  const loadInitialQuestion = async () => {
    try {
      const res = await axios.get('/get_mock_question?index=0')
      setQuestion(res.data.question || "Explain a programming concept you're comfortable with.")
    } catch (err) {
      setQuestion("Explain a programming concept you're comfortable with.")
    }
  }

  const handleCategorySelect = async (category) => {
    setSelectedCategory(category)
    setStarted(true)
    
    try {
      await axios.post('/set_category', {
        category,
        company: selectedCompany || undefined
      })
      await loadQuestion()
    } catch (err) {
      console.error('Failed to set category:', err)
      showToast('Failed to load category')
    }
  }

  const loadQuestion = async () => {
    try {
      const res = await axios.get('/get_mock_question?index=0')
      setQuestion(res.data.question || `Explain a concept from ${selectedCategory}.`)
      setQuestionSaved(false)
      setAnswerText('')
      setFeedback('')
      setScore(null)
      startTimer()
    } catch (err) {
      setQuestion(`Explain a concept from ${selectedCategory}.`)
      startTimer()
    }
  }

  const handleCompanyChange = async (company) => {
    setSelectedCompany(company)
    try {
      await axios.post('/clear_question_cache')
      if (started && selectedCategory) {
        await axios.post('/set_category', {
          category: selectedCategory,
          company: company || undefined,
          force_refresh: true
        })
        await loadQuestion()
      }
      showToast(company ? `Filtering for ${company}` : 'Showing all companies')
    } catch (err) {
      console.error('Failed to change company:', err)
    }
  }

  const submitAnswer = async () => {
    if (!answerText.trim()) {
      showToast('Please type your answer')
      return
    }

    clearTimer()

    try {
      const res = await axios.post('/evaluate_answer', {
        question_text: question,
        answer: answerText
      })

      const evalObj = res.data.evaluation || {}
      const plagScore = res.data.plagiarism_score

      let html = ''
      if (evalObj.summary) {
        html += `<strong>Summary:</strong><div class="mt-2">${evalObj.summary}</div>`
      }
      if (evalObj.improvements && evalObj.improvements.length) {
        html += `<div class="mt-3"><strong>Improvements:</strong><ul class="list-disc pl-5 mt-1">`
        evalObj.improvements.forEach(imp => {
          html += `<li>${imp}</li>`
        })
        html += `</ul></div>`
      }
      if (plagScore != null) {
        html += `<div class="mt-3"><strong>Similarity:</strong> ${(plagScore * 100).toFixed(1)}%</div>`
      }

      setFeedback(html || 'No feedback returned.')
      setScore(evalObj.score ? Math.round(evalObj.score * 10) / 10 : null)
      
      // Update difficulty
      if (evalObj.score) {
        updateDifficulty(evalObj.score)
      }
      
      showToast('Evaluation received')
    } catch (err) {
      console.error('Evaluation failed:', err)
      showToast('Evaluation failed')
    }
  }

  const updateDifficulty = (newScore) => {
    const newCount = questionsAtLevel + 1
    setQuestionsAtLevel(newCount)

    if (newCount >= 3) {
      if (difficulty === 'beginner' && newScore >= 7.0) {
        setDifficulty('intermediate')
        setQuestionsAtLevel(0)
        showToast('🎉 Promoted to INTERMEDIATE level!')
      } else if (difficulty === 'intermediate' && newScore >= 8.0) {
        setDifficulty('advanced')
        setQuestionsAtLevel(0)
        showToast('🔥 Promoted to ADVANCED level!')
      }
    }
  }

  const toggleRecording = async () => {
    if (recording) {
      // Stop recording
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop()
      }
      setRecording(false)
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        const mediaRecorder = new MediaRecorder(stream)
        mediaRecorderRef.current = mediaRecorder
        audioChunksRef.current = []

        mediaRecorder.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data)
        }

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
          await transcribeAudio(audioBlob)
          stream.getTracks().forEach(track => track.stop())
        }

        mediaRecorder.start()
        setRecording(true)
        showToast('Recording started')
      } catch (err) {
        console.error('Failed to start recording:', err)
        showToast('Microphone access denied')
      }
    }
  }

  const transcribeAudio = async (audioBlob) => {
    setTranscribing(true)
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.webm')

      const res = await axios.post('/transcribe_audio', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      if (res.data.transcription) {
        setAnswerText(res.data.transcription)
        showToast('Transcription complete')
      }
    } catch (err) {
      console.error('Transcription failed:', err)
      showToast('Transcription failed')
    } finally {
      setTranscribing(false)
    }
  }

  const saveQuestion = async () => {
    try {
      await axios.post('/save_question', {
        question,
        company: selectedCompany || undefined
      })
      setQuestionSaved(true)
      showToast('Question saved!')
    } catch (err) {
      console.error('Failed to save question:', err)
      showToast('Failed to save question')
    }
  }

  const resetToCategories = async () => {
    setStarted(false)
    setAnswerText('')
    setFeedback('')
    setScore(null)
    setQuestionSaved(false)
    clearTimer()
    
    try {
      await axios.post('/clear_question_cache')
    } catch (err) {
      console.error('Failed to clear cache:', err)
    }
  }

  const showToast = (msg) => {
    if (window.showToast) {
      window.showToast(msg)
    } else {
      alert(msg)
    }
  }

  return (
    <div className="practice-container">
      <div className="practice-grid">
        <main className="practice-main">
          {!started ? (
            <CategoryGrid
              categories={CATEGORIES}
              companies={COMPANIES}
              selectedCompany={selectedCompany}
              onCompanyChange={handleCompanyChange}
              onCategorySelect={handleCategorySelect}
            />
          ) : (
            <QuestionCard
              category={selectedCategory}
              company={selectedCompany}
              question={question}
              answerText={answerText}
              feedback={feedback}
              score={score}
              timeLeft={timeLeft}
              progress={progress}
              recording={recording}
              transcribing={transcribing}
              questionSaved={questionSaved}
              difficulty={difficulty}
              questionsAtLevel={questionsAtLevel}
              onAnswerChange={setAnswerText}
              onSubmit={submitAnswer}
              onNext={loadQuestion}
              onToggleRecording={toggleRecording}
              onSaveQuestion={saveQuestion}
              onBack={resetToCategories}
            />
          )}
        </main>
        
        <Sidebar onReset={resetToCategories} />
      </div>
    </div>
  )
}
