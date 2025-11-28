import React from 'react'

export default function FormSection({ title, children, icon = '📋' }) {
  return (
    <div className="form-section">
      {title && (
        <div className="form-section-title">
          <span>{icon}</span>
          {title}
        </div>
      )}
      <div className="form-grid">
        {children}
      </div>
    </div>
  )
}
