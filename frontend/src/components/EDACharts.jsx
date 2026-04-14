import React from 'react';
import Plot from './Plot';

const BASE_LAYOUT = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { family: 'Inter, sans-serif', color: '#4b5563', size: 12 },
  margin: { t: 40, r: 20, b: 50, l: 60 },
  hovermode: 'x unified',
};

export default function EDACharts({ edaData }) {
  if (!edaData || typeof edaData !== 'object') {
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No EDA data available</div>;
  }

  try {
    const priceMA = Array.isArray(edaData.price_with_ma) ? edaData.price_with_ma : [];
    const volumeTrend = Array.isArray(edaData.volume_trend) ? edaData.volume_trend : [];
    const rsiData = Array.isArray(edaData.rsi) ? edaData.rsi : [];
    const returnsDist = edaData.returns_distribution || null;
    const corrMatrix = edaData.correlation_matrix || null;

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        {/* Price with MA */}
        {priceMA.length > 0 && (
          <div className="glass-card" style={{ padding: '1rem' }}>
            <Plot
              data={[
                { type: 'scatter', mode: 'lines', x: priceMA.map(d => d.Date), y: priceMA.map(d => d.Close), name: 'Close', line: { color: '#f1f5f9', width: 1.5 } },
                ...(priceMA[0]?.MA_20 != null ? [{ type: 'scatter', mode: 'lines', x: priceMA.map(d => d.Date), y: priceMA.map(d => d.MA_20), name: 'MA 20', line: { color: '#3b82f6', width: 1.5 } }] : []),
                ...(priceMA[0]?.MA_50 != null ? [{ type: 'scatter', mode: 'lines', x: priceMA.map(d => d.Date), y: priceMA.map(d => d.MA_50), name: 'MA 50', line: { color: '#f59e0b', width: 1.5 } }] : []),
                ...(priceMA[0]?.MA_200 != null ? [{ type: 'scatter', mode: 'lines', x: priceMA.map(d => d.Date), y: priceMA.map(d => d.MA_200), name: 'MA 200', line: { color: '#8b5cf6', width: 1.5 } }] : []),
              ]}
              layout={{ ...BASE_LAYOUT, title: { text: 'Closing Price with Moving Averages', font: { size: 15, color: '#f1f5f9' }, x: 0.01 }, xaxis: { gridcolor: 'rgba(148,163,184,0.08)' }, yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Price (USD)', tickprefix: '$' }, legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 } }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: '420px' }}
            />
          </div>
        )}

        {/* Correlation Heatmap */}
        {corrMatrix && Array.isArray(corrMatrix.values) && Array.isArray(corrMatrix.columns) && (
          <div className="glass-card" style={{ padding: '1rem' }}>
            <Plot
              data={[{ type: 'heatmap', z: corrMatrix.values, x: corrMatrix.columns, y: corrMatrix.columns, colorscale: [[0, '#1e1b4b'], [0.25, '#3730a3'], [0.5, '#6366f1'], [0.75, '#818cf8'], [1, '#c7d2fe']], zmin: -1, zmax: 1, text: corrMatrix.values.map(row => Array.isArray(row) ? row.map(v => (v || 0).toFixed(2)) : []), texttemplate: '%{text}', textfont: { size: 9 }, hoverongaps: false }]}
              layout={{ ...BASE_LAYOUT, title: { text: 'Feature Correlation Heatmap', font: { size: 15, color: '#f1f5f9' }, x: 0.01 }, margin: { t: 40, r: 20, b: 100, l: 100 }, xaxis: { tickangle: -45, tickfont: { size: 9 } }, yaxis: { tickfont: { size: 9 } } }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        )}

        <div className="grid-2">
          {/* Volume Trend */}
          {volumeTrend.length > 0 && (
            <div className="glass-card" style={{ padding: '1rem' }}>
              <Plot
                data={[{ type: 'bar', x: volumeTrend.map(d => d.Month), y: volumeTrend.map(d => d.Volume), marker: { color: volumeTrend.map((_, i) => `rgba(59, 130, 246, ${0.3 + (i / volumeTrend.length) * 0.7})`) }, name: 'Volume' }]}
                layout={{ ...BASE_LAYOUT, title: { text: 'Monthly Trading Volume', font: { size: 14, color: '#f1f5f9' }, x: 0.01 }, xaxis: { gridcolor: 'rgba(148,163,184,0.08)', tickangle: -45, tickfont: { size: 9 } }, yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Volume' }, showlegend: false }}
                config={{ responsive: true, displayModeBar: false }}
                style={{ width: '100%', height: '350px' }}
              />
            </div>
          )}

          {/* Returns Distribution */}
          {returnsDist && Array.isArray(returnsDist.bin_edges) && Array.isArray(returnsDist.counts) && (
            <div className="glass-card" style={{ padding: '1rem' }}>
              <Plot
                data={[{ type: 'bar', x: returnsDist.bin_edges.slice(0, -1).map((v, i) => ((v + returnsDist.bin_edges[i+1]) / 2).toFixed(4)), y: returnsDist.counts, marker: { color: returnsDist.bin_edges.slice(0, -1).map((v, i) => { const mid = (v + returnsDist.bin_edges[i+1]) / 2; return mid >= 0 ? 'rgba(16, 185, 129, 0.6)' : 'rgba(239, 68, 68, 0.6)'; }) }, name: 'Frequency' }]}
                layout={{ ...BASE_LAYOUT, title: { text: 'Daily Returns Distribution', font: { size: 14, color: '#f1f5f9' }, x: 0.01 }, xaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Daily Return' }, yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Frequency' }, showlegend: false, annotations: [{ x: 0.98, y: 0.95, xref: 'paper', yref: 'paper', text: `μ=${(returnsDist.mean || 0).toFixed(4)}<br>σ=${(returnsDist.std || 0).toFixed(4)}<br>Skew=${(returnsDist.skew || 0).toFixed(2)}`, showarrow: false, align: 'right', font: { size: 10, color: '#94a3b8', family: 'JetBrains Mono' }, bgcolor: 'rgba(15,23,42,0.8)', borderpad: 6, borderwidth: 1, bordercolor: 'rgba(148,163,184,0.1)' }] }}
                config={{ responsive: true, displayModeBar: false }}
                style={{ width: '100%', height: '350px' }}
              />
            </div>
          )}
        </div>

        {/* RSI */}
        {rsiData.length > 0 && (
          <div className="glass-card" style={{ padding: '1rem' }}>
            <Plot
              data={[{ type: 'scatter', mode: 'lines', x: rsiData.map(d => d.Date), y: rsiData.map(d => d.RSI_14), name: 'RSI 14', line: { color: '#06b6d4', width: 1.5 }, fill: 'tozeroy', fillcolor: 'rgba(6,182,212,0.05)' }]}
              layout={{ ...BASE_LAYOUT, title: { text: 'Relative Strength Index (RSI-14)', font: { size: 14, color: '#f1f5f9' }, x: 0.01 }, xaxis: { gridcolor: 'rgba(148,163,184,0.08)' }, yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'RSI', range: [0, 100] }, shapes: [{ type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 70, y1: 70, line: { color: 'rgba(239,68,68,0.4)', dash: 'dash', width: 1 } }, { type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 30, y1: 30, line: { color: 'rgba(16,185,129,0.4)', dash: 'dash', width: 1 } }], showlegend: false }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: '300px' }}
            />
          </div>
        )}

        {/* Summary */}
        {edaData.info && (
          <div className="glass-card">
            <div className="card-header"><h3 className="card-title">Dataset Summary</h3></div>
            <div className="grid-3 stagger">
              <div style={{ textAlign: 'center' }}>
                <div className="metric-label">Total Records</div>
                <div className="metric-value neutral">{(edaData.info.total_records || 0).toLocaleString()}</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div className="metric-label">Date Range</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.875rem', color: 'var(--text-primary)' }}>
                  {edaData.info.date_range?.start || 'N/A'} → {edaData.info.date_range?.end || 'N/A'}
                </div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div className="metric-label">Enriched Features</div>
                <div className="metric-value neutral">{Array.isArray(edaData.info.enriched_columns) ? edaData.info.enriched_columns.length : 0}</div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  } catch (error) {
    console.error('EDACharts error:', error);
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--accent-red)' }}>Error rendering EDA charts</div>;
  }
}
