import React, { useState } from 'react'

export default function CategoryGrid({ 
  categories, 
  companies, 
  selectedCompany, 
  onCompanyChange, 
  onCategorySelect 
}) {
  const [hoveredCategory, setHoveredCategory] = useState(null)

  return (
    <section className="category-section">
      <div className="category-card">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-extrabold text-slate-800 dark:text-white">
            🎯 Practice
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">
            Pick a category to start practicing questions.
          </p>
        </div>

        <div className="company-filter">
          <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
            🏢 Target Company:
          </label>
          <select
            value={selectedCompany}
            onChange={(e) => onCompanyChange(e.target.value)}
            className="company-select"
          >
            <option value="">All Companies</option>
            {companies.map(company => (
              <option key={company} value={company}>{company}</option>
            ))}
          </select>
          {selectedCompany && (
            <span className="text-xs text-indigo-600 dark:text-indigo-400">
              Showing {selectedCompany} questions
            </span>
          )}
        </div>

        <div className="category-grid">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => onCategorySelect(category)}
              onMouseEnter={() => setHoveredCategory(category)}
              onMouseLeave={() => setHoveredCategory(null)}
              className={`category-tile ${hoveredCategory === category ? 'hovered' : ''}`}
            >
              <div className="text-sm font-semibold text-slate-900 dark:text-white">
                {category}
              </div>
            </button>
          ))}
        </div>

        <div className="mt-6 text-sm text-slate-500 dark:text-slate-400 text-center">
          Tip: Click any tile to start practicing. Use the right panel for quick actions.
        </div>
      </div>
    </section>
  )
}
