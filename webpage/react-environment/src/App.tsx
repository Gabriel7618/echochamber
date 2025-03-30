import { useState } from 'react'
import './App.css'
import { Input } from "antd"

function App() {

  return (
    <>
      <div className="card">
        <Input placeholder="Placeholder text here" />
      </div>
      <p className="example name">
        Example text
      </p>
    </>
  )
}

export default App
