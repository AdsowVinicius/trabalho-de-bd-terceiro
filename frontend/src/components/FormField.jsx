import React from 'react'

export default function FormField({label, children, error, hint, required = false, conditional = false}){
  return (
    <div className={`form-group ${conditional ? 'conditional-field' : ''}`}>
      {label && (
        <label data-required={required ? '*' : ''}>
          {label}
        </label>
      )}
      {children}
      {error && <span className="form-error">⚠️ {error}</span>}
      {hint && <span className="form-hint">ℹ️ {hint}</span>}
    </div>
  )
}
