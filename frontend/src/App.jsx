/**
 * App — Root component with routing.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import EDA from './pages/EDA';
import Predictions from './pages/Predictions';
import About from './pages/About';

export default function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/eda" element={<EDA />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/about" element={<About />} />
          </Routes>
          <footer style={{
            textAlign: 'center',
            padding: '2rem',
            color: 'var(--text-muted)',
            fontSize: '0.75rem',
            marginTop: '2rem',
            borderTop: '1px solid var(--border-color)',
          }}>
            TeslaPulse © {new Date().getFullYear()} — Tesla Stock Prediction Platform | Built with React, Flask & scikit-learn
          </footer>
        </main>
      </div>
    </Router>
  );
}
