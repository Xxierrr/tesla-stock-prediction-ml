/**
 * PredictionPanel — Display actual vs predicted price chart with metrics.
 */
import React from 'react';
import Plot from './Plot';
import { Target, TrendingUp, Award } from 'lucide-react';

export default function PredictionPanel({ results, activeModel = null }) {
  if (!results) return null;

  // Determine which model result to show
  const modelKeys = ['linear_regression', 'random_forest', 'lstm'];
  const modelKey = activeModel || modelKeys[0];
  const model = results[modelKey];

  if (!model || !model.predictions) return null;

  const { dates, actual, predicted } = model.predictions;
  const { metrics } = model;

  const traces = [
    { type: 'scatter', mode: 'lines', x: dates, y: actual, name: 'Actual Price', line: { color: '#94a3b8', width: 2 } },
    { type: 'scatter', mode: 'lines', x: dates, y: predicted, name: 'Predicted Price', line: { color: '#2563eb', width: 2, dash: 'dot' } }
  ];

  const layout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { family: 'Inter, sans-serif', color: '#4b5563', size: 12 },
    margin: { t: 40, r: 20, b: 50, l: 60 },
    title: { text: `${model.model_name} — Actual vs Predicted`, font: { size: 15, color: '#1f2937' }, x: 0.01, xanchor: 'left' },
    xaxis: { gridcolor: '#f3f4f6', linecolor: '#e5e7eb' },
    yaxis: { gridcolor: '#f3f4f6', linecolor: '#e5e7eb', title: 'Price (USD)', tickprefix: '$' },
    legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
    hovermode: 'x unified',
  };

  return (
    <div>
      {/* Metric cards */}
      <div className="grid-4" style={{ marginBottom: '1.5rem' }}>
        <div className="metric">
          <div className="metric-label">RMSE</div>
          <div className="metric-value blue">{metrics.rmse.toFixed(2)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">MAE</div>
          <div className="metric-value blue">{metrics.mae.toFixed(2)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">R² Score</div>
          <div className={`metric-value ${metrics.r2 >= 0.8 ? 'green' : 'red'}`}>
            {metrics.r2.toFixed(4)}
          </div>
        </div>
        <div className="metric">
          <div className="metric-label">MAPE</div>
          <div className="metric-value blue">{metrics.mape ? metrics.mape.toFixed(2) + '%' : 'N/A'}</div>
        </div>
      </div>

      {/* Chart */}
      <div className="panel" style={{ padding: '0' }}>
        <div className="panel-header" style={{ padding: '1.25rem', borderBottom: 'none', marginBottom: 0 }}>Prediction Chart</div>
        <Plot
          data={traces}
          layout={layout}
          config={{ responsive: true, displayModeBar: true, displaylogo: false }}
          style={{ width: '100%', height: '450px' }}
        />
      </div>
    </div>
  );
}
