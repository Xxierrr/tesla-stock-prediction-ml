/**
 * Sidebar — Left navigation pane.
 */
import React from 'react';
import { NavLink } from 'react-router-dom';
import { Database, BarChart3, BrainCircuit, Info } from 'lucide-react';

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="brand">
        TeslaPulse
      </div>

      <div className="nav-links">
        <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Database size={16} /> 1. Data Source
        </NavLink>
        <NavLink to="/eda" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <BarChart3 size={16} /> 2. Data Analysis
        </NavLink>
        <NavLink to="/predictions" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <BrainCircuit size={16} /> 3. Model Training
        </NavLink>
        <NavLink to="/about" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Info size={16} /> 4. About & Tech
        </NavLink>
      </div>

      <div style={{ flex: 1 }} />

      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        Tesla Stock Prediction<br/>
        Built with React & Flask
      </div>
    </div>
  );
}
