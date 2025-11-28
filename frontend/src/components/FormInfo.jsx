import React from 'react'

export default function FormInfo({ children, type = 'info' }) {
  const icons = {
    info: 'ℹ️',
    warning: '⚠️',
    error: '❌',
    success: '✅',
    tip: '💡'
  }

  return (
    <div className={`form-${type}`}>
      <span style={{ marginRight: '8px' }}>{icons[type]}</span>
      {children}
    </div>
  )
}
