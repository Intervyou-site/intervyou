import React from 'react'

export default function QuestionCard({
  category,
  company,
  question,
  answerText,
  feedback,
  score,
  timeLeft,
  progress,
  recording,
  transcribing,
  questionSaved,
  difficulty,
  questionsAtLevel,
  onAnswerChange,
  onSubmit,
  onNext,
  onToggleRecording,
  onSaveQuestion,
  onBack
}) {
  const difficultyConfig = {
    beginner: { emoji: '🌱', color: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300' },
    intermediate: { emoji: '⚡', color: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300' },
    advanced: { emoji: '🔥', color: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300' }
  }

  const config = difficultyConfig[difficulty] || difficultyConfig.beginner

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSubmit()
    }
  }

  return (
    <section className="question-card">
      <div className="question-header">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-indigo-600">{category}</h1>
            {company && (
              <span className="company-badge">
                🏢 {company}
              </span>
            )}
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            {company 
              ? `Practicing ${company}-specific questions` 
              : 'Answer this question — use the text box or record your voice.'}
          </p>
          <div className={`difficulty-badge ${config.color}`}>
            <span>{config.emoji}</span>
            <span>{difficulty.toUpperCase()}</span>
            <span className="text-xs opacity-75">({questionsAtLevel} answered)</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={onBack} className="text-sm text-slate-400 hover:text-indigo-600">
            ⬅ Back
          </button>
          <div className="text-xs text-slate-400">
            ⏱ <strong>{timeLeft}</strong>s
          </div>
        </div>
      </div>

      <div className="question-box">
        <p className="text-base font-medium text-slate-800 dark:text-slate-100">
          {question}
        </p>
        <div className="question-actions">
          <button 
            onClick={() => {
              const utterance = new SpeechSynthesisUtterance(question)
              window.speechSynthesis.speak(utterance)
            }}
            className="btn-primary"
          >
            🔊 Play Question
          </button>
          <button
            onClick={onSaveQuestion}
            className={questionSaved ? 'btn-saved' : 'btn-save'}
          >
            {questionSaved ? 'Saved' : '⭐ Save Question'}
          </button>
          <div className="ml-auto text-xs text-slate-400">
            Progress <strong>{progress}%</strong>
          </div>
        </div>
      </div>

      <div className="answer-section">
        <div>
          <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
            ✍️ Type your answer
          </label>
          <textarea
            value={answerText}
            onChange={(e) => onAnswerChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Write your answer here..."
            className="answer-textarea"
          />
          <div className="answer-actions">
            <button onClick={onSubmit} className="btn-submit">
              Submit
            </button>
            <button onClick={onNext} className="btn-next">
              Next
            </button>
          </div>
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
            🎙️ Record & Transcribe
          </label>
          <div className="mt-2">
            <button
              onClick={onToggleRecording}
              className={recording ? 'btn-recording' : 'btn-record'}
            >
              {recording ? '⏹️ Stop & Transcribe' : '🎙️ Record'}
            </button>
            {transcribing && (
              <div className="mt-3 text-sm text-indigo-600 dark:text-indigo-400">
                ⏳ Transcribing with Whisper AI...
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="feedback-box">
        <div 
          dangerouslySetInnerHTML={{ __html: feedback || 'AI feedback will appear here after you submit.' }}
        />
        <div className="feedback-footer">
          <span className="text-xs text-slate-400">
            Score: <strong>{score !== null ? `${score}/10` : '—'}</strong>
          </span>
        </div>
      </div>
    </section>
  )
}
