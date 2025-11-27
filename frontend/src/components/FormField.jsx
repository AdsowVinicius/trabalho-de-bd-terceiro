import React from 'react'

export default function FormField({label, children}){
  return (
    <div style={{ marginBottom: 12 }}>
      <label style={{ display: 'block', marginBottom:4 }}>{label}</label>
      {children}
    </div>
  )
}
