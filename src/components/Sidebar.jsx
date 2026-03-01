import React from 'react'

export default function Sidebar({ onReset }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-card">
        <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
          💡 Practice Tips
        </h3>
        <ul className="text-sm text-slate-600 dark:text-slate-300 space-y-2">
          <li>🧩 Focus on one topic per session.</li>
          <li>🎧 Listen to your recorded answers.</li>
          <li>🗣️ Speak clearly and naturally.</li>
          <li>⭐ Save questions you want to revisit.</li>
        </ul>
      </div>

      <div className="sidebar-actions">
        <h4 className="text-sm font-semibold text-indigo-700 dark:text-indigo-300 mb-3">
          Quick Actions
        </h4>
        <button onClick={onReset} className="sidebar-btn-primary">
          Choose Category
        </button>
        <a href="/mock_interview" className="sidebar-btn-secondary">
          Start Mock Interview
        </a>
      </div>
    </aside>
  )
}
