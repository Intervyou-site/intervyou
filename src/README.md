# React Components Documentation

## Overview

This directory contains React components for the IntervYou practice page. The components are built with React 18 and use Axios for API calls.

## Component Structure

```
src/
├── components/
│   ├── PracticePage.jsx      # Main container with state management
│   ├── CategoryGrid.jsx      # Category selection interface
│   ├── QuestionCard.jsx      # Question display and answer submission
│   └── Sidebar.jsx            # Tips and quick actions
├── styles/
│   └── practice.css           # Component styles
└── practice-entry.jsx         # React app entry point
```

## Components

### PracticePage.jsx
**Main container component that manages all state and API calls.**

**State:**
- `started` - Whether user has selected a category
- `selectedCategory` - Current category name
- `selectedCompany` - Company filter (optional)
- `question` - Current question text
- `answerText` - User's typed answer
- `feedback` - AI feedback HTML
- `score` - Evaluation score (0-10)
- `timeLeft` - Timer countdown (150s)
- `recording` - Recording state
- `difficulty` - Current level (beginner/intermediate/advanced)

**Key Functions:**
- `handleCategorySelect()` - Sets category and loads first question
- `submitAnswer()` - Sends answer to `/evaluate_answer` API
- `toggleRecording()` - Starts/stops audio recording
- `updateDifficulty()` - Handles level progression

**API Endpoints Used:**
- `GET /get_mock_question?index=0` - Fetch question
- `POST /set_category` - Set practice category
- `POST /evaluate_answer` - Submit answer for evaluation
- `POST /save_question` - Save question to user's list
- `POST /clear_question_cache` - Clear question cache

### CategoryGrid.jsx
**Displays category tiles and company filter.**

**Props:**
- `categories` - Array of category names
- `companies` - Array of company names
- `selectedCompany` - Currently selected company
- `onCompanyChange` - Callback when company changes
- `onCategorySelect` - Callback when category is clicked

**Features:**
- Hover effects on category tiles
- Company dropdown filter
- Responsive grid layout

### QuestionCard.jsx
**Main question interface with answer submission.**

**Props:**
- `category` - Current category name
- `company` - Selected company (optional)
- `question` - Question text
- `answerText` - Current answer text
- `feedback` - AI feedback HTML
- `score` - Evaluation score
- `timeLeft` - Remaining time
- `recording` - Recording state
- `difficulty` - Current difficulty level
- `onAnswerChange` - Callback for text changes
- `onSubmit` - Submit answer callback
- `onToggleRecording` - Recording toggle callback

**Features:**
- Text-to-speech for questions
- Textarea with Enter-to-submit
- Recording button with state indication
- Difficulty badge with progression tracking
- Save question button
- Timer display

### Sidebar.jsx
**Tips and quick action buttons.**

**Props:**
- `onReset` - Callback to return to category selection

**Features:**
- Practice tips list
- Quick action buttons
- Links to other pages

## Styling

All styles are in `src/styles/practice.css`. The design uses:
- Tailwind-inspired utility classes
- Custom component classes
- Responsive breakpoints
- Dark mode support (via parent theme)

## API Integration

### Request Format

**Set Category:**
```javascript
POST /set_category
{
  "category": "Python",
  "company": "Google",  // optional
  "force_refresh": true  // optional
}
```

**Evaluate Answer:**
```javascript
POST /evaluate_answer
{
  "question_text": "What are Python decorators?",
  "answer": "Decorators are functions that modify..."
}
```

**Save Question:**
```javascript
POST /save_question
{
  "question": "What are Python decorators?",
  "company": "Google"  // optional
}
```

### Response Format

**Get Question:**
```javascript
{
  "question": "What are Python decorators?",
  "keywords": ["decorator", "function", "wrapper"]
}
```

**Evaluate Answer:**
```javascript
{
  "evaluation": {
    "summary": "Good explanation...",
    "improvements": ["Add more examples", "Explain use cases"],
    "score": 7.5,
    "audio_url": "/static/audio/feedback.mp3"
  },
  "plagiarism_score": 0.15,
  "matches": [...]
}
```

## State Management

The app uses React hooks for state management:
- `useState` - Component state
- `useEffect` - Side effects (loading questions, timers)
- `useRef` - MediaRecorder and timer references

## Audio Recording

Recording uses the Web Audio API:
1. Request microphone permission
2. Create MediaRecorder instance
3. Collect audio chunks
4. Convert to Blob on stop
5. Send to `/transcribe_audio` endpoint

## Difficulty Progression

**Levels:**
- Beginner (🌱) - Starting level
- Intermediate (⚡) - Promoted at avg score ≥ 7.0 (3+ questions)
- Advanced (🔥) - Promoted at avg score ≥ 8.0 (3+ questions)

**Demotion:**
- If avg score < 4.0 after 5 questions, demote one level

## Building

**Development:**
```bash
npm run dev  # Starts Vite dev server on port 3000
```

**Production:**
```bash
npm run build  # Builds to static/react-dist/
```

## Adding New Features

### Example: Add Question Difficulty Display

1. **Update API call in PracticePage.jsx:**
```javascript
const res = await axios.get('/get_mock_question?index=0&difficulty=' + difficulty)
```

2. **Add state:**
```javascript
const [questionDifficulty, setQuestionDifficulty] = useState('medium')
```

3. **Update QuestionCard.jsx props:**
```javascript
<QuestionCard
  questionDifficulty={questionDifficulty}
  // ... other props
/>
```

4. **Display in QuestionCard.jsx:**
```javascript
<span className="difficulty-indicator">
  Difficulty: {questionDifficulty}
</span>
```

## Testing

**Manual Testing Checklist:**
- [ ] Category selection works
- [ ] Company filter updates questions
- [ ] Timer counts down correctly
- [ ] Text answer submission works
- [ ] Voice recording works
- [ ] Transcription displays in textarea
- [ ] AI feedback displays correctly
- [ ] Score shows properly
- [ ] Question saving works
- [ ] Difficulty progression works
- [ ] Back button resets state
- [ ] Next question loads correctly

## Browser Compatibility

**Tested on:**
- Chrome 120+
- Firefox 120+
- Safari 17+
- Edge 120+

**Required APIs:**
- MediaRecorder API (for recording)
- SpeechSynthesis API (for text-to-speech)
- Fetch API (for HTTP requests)

## Performance

**Optimizations:**
- Debounced API calls
- Lazy loading of components (can be added)
- Memoized callbacks (can be added)
- Code splitting (can be added)

**Bundle Size:**
- React + ReactDOM: ~140KB (gzipped)
- Axios: ~13KB (gzipped)
- Custom code: ~15KB (gzipped)
- Total: ~170KB (gzipped)

## Future Enhancements

1. **TypeScript** - Add type safety
2. **React Query** - Better API state management
3. **Zustand/Redux** - Global state management
4. **React Router** - SPA navigation
5. **Framer Motion** - Smooth animations
6. **React Testing Library** - Unit tests
7. **Storybook** - Component documentation
8. **Code Splitting** - Reduce initial bundle size

## Troubleshooting

**Component not rendering:**
- Check if `react-practice-root` div exists in HTML
- Verify bundle is loaded in browser Network tab
- Check browser console for errors

**API calls failing:**
- Verify FastAPI is running
- Check CORS settings
- Inspect Network tab for request details

**Recording not working:**
- Check microphone permissions
- Verify HTTPS (required for getUserMedia)
- Test in different browser

## Contributing

When adding new components:
1. Create component file in `src/components/`
2. Add styles to `src/styles/practice.css`
3. Import in parent component
4. Update this README
5. Test thoroughly
6. Build and verify production bundle

---

**Questions?** Check the main documentation or FastAPI logs for debugging.
