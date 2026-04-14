/**
 * Navbar — Top navigation with brand, links, and live price ticker.
 */
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BarChart3, BrainCircuit, Info, Zap } from 'lucide-react';
import RealTimePrice from './RealTimePrice';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        {/* Brand */}
        <div className="nav-brand">
          <div className="nav-brand-icon">
            <Zap size={20} />
          </div>
          <span style={{ background: 'var(--gradient-primary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            TeslaPulse
          </span>
        </div>

        {/* Links */}
        <div className="nav-links">
          <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <LayoutDashboard size={16} /> Dashboard
          </NavLink>
          <NavLink to="/eda" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <BarChart3 size={16} /> EDA
          </NavLink>
          <NavLink to="/predictions" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <BrainCircuit size={16} /> Predictions
          </NavLink>
          <NavLink to="/about" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <Info size={16} /> About
          </NavLink>
        </div>

        {/* Live Price */}
        <div className="nav-price">
          <RealTimePrice compact />
        </div>
      </div>
    </nav>
  );
}
