/**
 * About — Methodology, tech stack, and project info.
 */
import React from 'react';
import { Cpu, Database, BarChart3, GitBranch, Layers, Zap, Globe, Server } from 'lucide-react';

export default function About() {
  const pipeline = [
    { icon: <Database size={20} />, title: 'Data Collection', desc: 'Historical TSLA data from Yahoo Finance API (Open, High, Low, Close, Volume)', color: 'blue' },
    { icon: <BarChart3 size={20} />, title: 'Exploratory Data Analysis', desc: 'Trend visualization, correlation heatmaps, moving averages, return distributions', color: 'cyan' },
    { icon: <Layers size={20} />, title: 'Feature Engineering', desc: 'Technical indicators: MA(20/50/200), RSI-14, Bollinger Bands, MACD, Volatility', color: 'green' },
    { icon: <GitBranch size={20} />, title: 'Feature Selection', desc: 'Correlation-based filtering and Random Forest feature importance ranking', color: 'amber' },
    { icon: <Cpu size={20} />, title: 'Model Training', desc: 'Linear Regression, Random Forest, and LSTM (Deep Learning) with 80/20 time-series split', color: 'purple' },
    { icon: <Zap size={20} />, title: 'K-Fold Validation', desc: 'TimeSeriesSplit (5-fold) cross-validation preserving temporal order', color: 'red' },
  ];

  const techStack = [
    { category: 'Frontend', items: ['React 18', 'Vite', 'Plotly.js', 'Lucide Icons', 'Axios'] },
    { category: 'Backend', items: ['Flask', 'Flask-CORS', 'Python 3.x'] },
    { category: 'Machine Learning', items: ['scikit-learn', 'MLPRegressor (Deep Learning)', 'MinMaxScaler', 'TimeSeriesSplit'] },
    { category: 'Data & Storage', items: ['yfinance', 'pandas', 'NumPy', 'SQLite', 'ta (Technical Analysis)'] },
  ];

  return (
    <div className="page-container">
      <h1 className="page-title">About TeslaPulse</h1>
      <p className="page-subtitle">A full-stack ML-powered Tesla stock price prediction platform</p>

      {/* ML Pipeline */}
      <div className="glass-card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header"><h3 className="card-title">ML Pipeline</h3></div>
        <div style={{ display: 'grid', gap: '1rem' }}>
          {pipeline.map((step, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }} className="animate-fade-in-up">
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' }}>
                <div className={`card-icon ${step.color}`} style={{ flexShrink: 0 }}>{step.icon}</div>
                {i < pipeline.length - 1 && (
                  <div style={{ width: '2px', height: '24px', background: 'var(--border-color)' }} />
                )}
              </div>
              <div style={{ paddingTop: '0.25rem' }}>
                <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.9375rem', marginBottom: '0.125rem' }}>
                  Step {i + 1}: {step.title}
                </div>
                <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{step.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="glass-card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header"><h3 className="card-title">Evaluation Metrics</h3></div>
        <table className="data-table">
          <thead>
            <tr><th>Metric</th><th>Formula</th><th>Interpretation</th></tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>RMSE</td>
              <td className="mono" style={{ fontSize: '0.8125rem' }}>√(Σ(yᵢ - ŷᵢ)² / n)</td>
              <td>Root Mean Squared Error — lower is better, penalises large errors</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>MAE</td>
              <td className="mono" style={{ fontSize: '0.8125rem' }}>Σ|yᵢ - ŷᵢ| / n</td>
              <td>Mean Absolute Error — average absolute deviation, lower is better</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>R²</td>
              <td className="mono" style={{ fontSize: '0.8125rem' }}>1 - SS_res / SS_tot</td>
              <td>Coefficient of determination — 1.0 is perfect, higher is better</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>MAPE</td>
              <td className="mono" style={{ fontSize: '0.8125rem' }}>Σ|(yᵢ - ŷᵢ)/yᵢ| / n × 100</td>
              <td>Mean Absolute Percentage Error — percentage-based, lower is better</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Tech Stack */}
      <div className="glass-card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header"><h3 className="card-title">Technology Stack</h3></div>
        <div className="grid-2">
          {techStack.map((group, i) => (
            <div key={i} style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--border-radius-sm)' }}>
              <div style={{ fontWeight: 700, color: 'var(--accent-blue)', fontSize: '0.8125rem', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.75rem' }}>
                {group.category}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
                {group.items.map(item => (
                  <span key={item} style={{
                    padding: '0.25rem 0.625rem',
                    background: 'rgba(59,130,246,0.08)',
                    border: '1px solid rgba(59,130,246,0.15)',
                    borderRadius: '100px',
                    fontSize: '0.75rem',
                    color: 'var(--text-secondary)',
                  }}>{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Deployment Guide */}
      <div className="glass-card">
        <div className="card-header"><h3 className="card-title"><Globe size={14} style={{ display: 'inline', marginRight: 6 }} />Deployment Guide</h3></div>
        <div className="grid-2">
          <div style={{ padding: '1rem', background: 'rgba(16,185,129,0.05)', borderRadius: 'var(--border-radius-sm)', border: '1px solid rgba(16,185,129,0.1)' }}>
            <div style={{ fontWeight: 700, color: 'var(--accent-green)', marginBottom: '0.5rem' }}>
              <Server size={14} style={{ display: 'inline', marginRight: 6 }} />Frontend — Vercel / Netlify
            </div>
            <ol style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', paddingLeft: '1.25rem', lineHeight: 2 }}>
              <li>Push code to GitHub</li>
              <li>Connect repo to Vercel/Netlify</li>
              <li>Set build command: <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: 4 }}>npm run build</code></li>
              <li>Set output dir: <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: 4 }}>dist</code></li>
              <li>Add env var: <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: 4 }}>VITE_API_URL</code></li>
            </ol>
          </div>
          <div style={{ padding: '1rem', background: 'rgba(139,92,246,0.05)', borderRadius: 'var(--border-radius-sm)', border: '1px solid rgba(139,92,246,0.1)' }}>
            <div style={{ fontWeight: 700, color: 'var(--accent-purple)', marginBottom: '0.5rem' }}>
              <Server size={14} style={{ display: 'inline', marginRight: 6 }} />Backend — Render / Heroku
            </div>
            <ol style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', paddingLeft: '1.25rem', lineHeight: 2 }}>
              <li>Push backend/ to GitHub</li>
              <li>Create new Web Service on Render</li>
              <li>Set start command: <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: 4 }}>gunicorn app:app</code></li>
              <li>Set Python version in runtime</li>
              <li>Configure CORS for frontend URL</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
