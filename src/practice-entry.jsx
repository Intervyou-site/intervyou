import React from 'react'
import ReactDOM from 'react-dom/client'
import PracticePage from './components/PracticePage'
import './styles/practice.css'

// Mount React app
const root = document.getElementById('react-practice-root')
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <PracticePage />
    </React.StrictMode>
  )
}
