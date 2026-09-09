import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// removing StrictMode temporarily
createRoot(document.getElementById('root')).render(
    <App />
)
