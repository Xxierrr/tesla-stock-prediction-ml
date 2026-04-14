/**
 * ModelComparison — Side-by-side model performance comparison.
 */
import React from 'react';
import Plot from './Plot';
import { Trophy, Clock } from 'lucide-react';

export default function ModelComparison({ results }) {
  if (!results || typeof results !== 'object' || !results.comparison) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No comparison data available</div>;
  }

  try {
    const { models, best_model } = results.comparison;
    if (!Array.isArray(models) || models.length === 0) {
      return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No models to compare</div>;
    }

    const modelColors = {
      'Linear Regression': '#3b82f6',
      'Random Forest': '#10b981',
      'LSTM (Deep Learning)': '#8b5cf6',
    };

    const metricNames = ['RMSE', 'MAE', 'R²', 'MAPE'];
    const metricKeys = ['rmse', 'mae', 'r2', 'mape'];

    const barTraces = models.map(m => ({
      type: 'bar',
      name: m.name || 'Unknown',
      x: metricNames,
      y: metricKeys.map(k => m[k] || 0),
      marker: { color: modelColors[m.name] || '#64748b', borderRadius: 4 },
      text: metricKeys.map(k => (m[k] || 0).toFixed(3)),
      textposition: 'outside',
      textfont: { size: 10, color: '#4b5563' },
    }));

    const barLayout = {
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: { family: 'Inter, sans-serif', color: '#4b5563', size: 12 },
      margin: { t: 30, r: 20, b: 50, l: 50 },
      barmode: 'group',
      xaxis: { gridcolor: '#f3f4f6' },
      yaxis: { gridcolor: '#f3f4f6', title: 'Score' },
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02 },
      bargap: 0.3,
    };

    return (
      <div>
        {best_model && (
        <div className="glass-card" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          marginBottom: '1.5rem',
          borderColor: 'rgba(245, 158, 11, 0.3)',
        }}>
          <div className="card-icon amber"><Trophy size={20} /></div>
          <div>
            <div style={{ fontSize: '0.75rem', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              Best Performing Model
            </div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#d97706' }}>
              {best_model}
            </div>
          </div>
        </div>
      )}

      {/* Comparison Table */}
      <div className="glass-card" style={{ marginBottom: '1.5rem', overflow: 'auto' }}>
        <div className="card-header">
          <h3 className="card-title">Model Performance Comparison</h3>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Model</th>
              <th>RMSE ↓</th>
              <th>MAE ↓</th>
              <th>R² ↑</th>
              <th>MAPE ↓</th>
              <th>Train Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {models.map((m, i) => (
              <tr key={i}>
                <td>
                  <span className={`model-tag ${m.name && m.name.includes('Linear') ? 'lr' : m.name && m.name.includes('Random') ? 'rf' : 'lstm'}`}>
                    {m.name || 'Unknown'}
                  </span>
                </td>
                <td className="mono">{(m.rmse || 0).toFixed(4)}</td>
                <td className="mono">{(m.mae || 0).toFixed(4)}</td>
                <td className="mono" style={{ color: (m.r2 || 0) >= 0.8 ? 'var(--accent-green)' : (m.r2 || 0) >= 0.5 ? 'var(--accent-amber)' : 'var(--accent-red)' }}>
                  {(m.r2 || 0).toFixed(4)}</td>
                <td className="mono">{m.mape ? m.mape.toFixed(2) + '%' : 'N/A'}</td>
                <td className="mono" style={{ color: 'var(--text-muted)' }}>
                  <Clock size={12} style={{ display: 'inline', marginRight: 4 }} />
                  {m.training_time || 0}s
                </td>
                <td>
                  {m.name === best_model ? (
                    <span className="model-tag best"><Trophy size={12} /> Best</span>
                  ) : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Bar Chart */}
      <div className="glass-card" style={{ padding: '1rem' }}>
        <Plot
          data={barTraces}
          layout={barLayout}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '400px' }}
        />
      </div>

      {/* K-Fold Results */}
      {results.linear_regression?.kfold_scores && (
        <div className="glass-card" style={{ marginTop: '1.5rem' }}>
          <div className="card-header">
            <h3 className="card-title">K-Fold Cross Validation (5-Fold TimeSeriesSplit)</h3>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Model</th>
                {[1,2,3,4,5].map(i => <th key={i}>Fold {i} R²</th>)}
                <th>Mean R²</th>
              </tr>
            </thead>
            <tbody>
              {['linear_regression', 'random_forest', 'lstm'].map(key => {
                const m = results[key];
                if (!m || !Array.isArray(m.kfold_scores)) return null;
                const scores = m.kfold_scores.map(s => s.r2 || 0);
                const mean = scores.length > 0 ? scores.reduce((a,b) => a+b, 0) / scores.length : 0;
                return (
                  <tr key={key}>
                    <td><span className={`model-tag ${key === 'linear_regression' ? 'lr' : key === 'random_forest' ? 'rf' : 'lstm'}`}>{m.model_name || key}</span></td>
                    {scores.map((s, i) => <td key={i} className="mono">{s.toFixed(4)}</td>)}
                    <td className="mono" style={{ fontWeight: 700, color: 'var(--accent-blue)' }}>{mean.toFixed(4)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
      </div>
    );
  } catch (error) {
    console.error('ModelComparison error:', error);
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--accent-red)' }}>Error rendering model comparison</div>;
  }
}
