/**
 * EDACharts — Exploratory Data Analysis visualizations.
 */
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
  if (!edaData) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

      {/* 1. Closing Price with Moving Averages */}
      {edaData.price_with_ma && (
        <div className="glass-card" style={{ padding: '1rem' }}>
          <Plot
            data={[
              {
                type: 'scatter', mode: 'lines',
                x: edaData.price_with_ma.map(d => d.Date),
                y: edaData.price_with_ma.map(d => d.Close),
                name: 'Close', line: { color: '#f1f5f9', width: 1.5 },
              },
              ...(edaData.price_with_ma[0]?.MA_20 !== undefined ? [{
                type: 'scatter', mode: 'lines',
                x: edaData.price_with_ma.map(d => d.Date),
                y: edaData.price_with_ma.map(d => d.MA_20),
                name: 'MA 20', line: { color: '#3b82f6', width: 1.5 },
              }] : []),
              ...(edaData.price_with_ma[0]?.MA_50 !== undefined ? [{
                type: 'scatter', mode: 'lines',
                x: edaData.price_with_ma.map(d => d.Date),
                y: edaData.price_with_ma.map(d => d.MA_50),
                name: 'MA 50', line: { color: '#f59e0b', width: 1.5 },
              }] : []),
              ...(edaData.price_with_ma[0]?.MA_200 !== undefined ? [{
                type: 'scatter', mode: 'lines',
                x: edaData.price_with_ma.map(d => d.Date),
                y: edaData.price_with_ma.map(d => d.MA_200),
                name: 'MA 200', line: { color: '#8b5cf6', width: 1.5 },
              }] : []),
            ]}
            layout={{
              ...BASE_LAYOUT,
              title: { text: 'Closing Price with Moving Averages', font: { size: 15, color: '#f1f5f9' }, x: 0.01 },
              xaxis: { gridcolor: 'rgba(148,163,184,0.08)' },
              yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Price (USD)', tickprefix: '$' },
              legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%', height: '420px' }}
          />
        </div>
      )}

      {/* 2. Correlation Heatmap */}
      {edaData.correlation_matrix && (
        <div className="glass-card" style={{ padding: '1rem' }}>
          <Plot
            data={[{
              type: 'heatmap',
              z: edaData.correlation_matrix.values,
              x: edaData.correlation_matrix.columns,
              y: edaData.correlation_matrix.columns,
              colorscale: [
                [0, '#1e1b4b'],
                [0.25, '#3730a3'],
                [0.5, '#6366f1'],
                [0.75, '#818cf8'],
                [1, '#c7d2fe'],
              ],
              zmin: -1, zmax: 1,
              text: edaData.correlation_matrix.values.map(row => row.map(v => v.toFixed(2))),
              texttemplate: '%{text}',
              textfont: { size: 9 },
              hoverongaps: false,
            }]}
            layout={{
              ...BASE_LAYOUT,
              title: { text: 'Feature Correlation Heatmap', font: { size: 15, color: '#f1f5f9' }, x: 0.01 },
              margin: { t: 40, r: 20, b: 100, l: 100 },
              xaxis: { tickangle: -45, tickfont: { size: 9 } },
              yaxis: { tickfont: { size: 9 } },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%', height: '500px' }}
          />
        </div>
      )}

      <div className="grid-2">
        {/* 3. Volume Trend */}
        {edaData.volume_trend && (
          <div className="glass-card" style={{ padding: '1rem' }}>
            <Plot
              data={[{
                type: 'bar',
                x: edaData.volume_trend.map(d => d.Month),
                y: edaData.volume_trend.map(d => d.Volume),
                marker: {
                  color: edaData.volume_trend.map((_, i) =>
                    `rgba(59, 130, 246, ${0.3 + (i / edaData.volume_trend.length) * 0.7})`
                  ),
                },
                name: 'Volume',
              }]}
              layout={{
                ...BASE_LAYOUT,
                title: { text: 'Monthly Trading Volume', font: { size: 14, color: '#f1f5f9' }, x: 0.01 },
                xaxis: { gridcolor: 'rgba(148,163,184,0.08)', tickangle: -45, tickfont: { size: 9 } },
                yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Volume' },
                showlegend: false,
              }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: '350px' }}
            />
          </div>
        )}

        {/* 4. Daily Returns Distribution */}
        {edaData.returns_distribution && (
          <div className="glass-card" style={{ padding: '1rem' }}>
            <Plot
              data={[{
                type: 'bar',
                x: edaData.returns_distribution.bin_edges.slice(0, -1).map((v, i) =>
                  ((v + edaData.returns_distribution.bin_edges[i+1]) / 2).toFixed(4)
                ),
                y: edaData.returns_distribution.counts,
                marker: {
                  color: edaData.returns_distribution.bin_edges.slice(0, -1).map((v, i) => {
                    const mid = (v + edaData.returns_distribution.bin_edges[i+1]) / 2;
                    return mid >= 0 ? 'rgba(16, 185, 129, 0.6)' : 'rgba(239, 68, 68, 0.6)';
                  }),
                },
                name: 'Frequency',
              }]}
              layout={{
                ...BASE_LAYOUT,
                title: { text: 'Daily Returns Distribution', font: { size: 14, color: '#f1f5f9' }, x: 0.01 },
                xaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Daily Return' },
                yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'Frequency' },
                showlegend: false,
                annotations: [{
                  x: 0.98, y: 0.95, xref: 'paper', yref: 'paper',
                  text: `μ=${edaData.returns_distribution.mean.toFixed(4)}<br>σ=${edaData.returns_distribution.std.toFixed(4)}<br>Skew=${edaData.returns_distribution.skew.toFixed(2)}`,
                  showarrow: false, align: 'right',
                  font: { size: 10, color: '#94a3b8', family: 'JetBrains Mono' },
                  bgcolor: 'rgba(15,23,42,0.8)', borderpad: 6, borderwidth: 1, bordercolor: 'rgba(148,163,184,0.1)',
                }],
              }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: '350px' }}
            />
          </div>
        )}
      </div>

      {/* 5. RSI */}
      {edaData.rsi && (
        <div className="glass-card" style={{ padding: '1rem' }}>
          <Plot
            data={[
              {
                type: 'scatter', mode: 'lines',
                x: edaData.rsi.map(d => d.Date),
                y: edaData.rsi.map(d => d.RSI_14),
                name: 'RSI 14', line: { color: '#06b6d4', width: 1.5 },
                fill: 'tozeroy', fillcolor: 'rgba(6,182,212,0.05)',
              },
            ]}
            layout={{
              ...BASE_LAYOUT,
              title: { text: 'Relative Strength Index (RSI-14)', font: { size: 14, color: '#f1f5f9' }, x: 0.01 },
              xaxis: { gridcolor: 'rgba(148,163,184,0.08)' },
              yaxis: { gridcolor: 'rgba(148,163,184,0.08)', title: 'RSI', range: [0, 100] },
              shapes: [
                { type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 70, y1: 70, line: { color: 'rgba(239,68,68,0.4)', dash: 'dash', width: 1 } },
                { type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 30, y1: 30, line: { color: 'rgba(16,185,129,0.4)', dash: 'dash', width: 1 } },
              ],
              showlegend: false,
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* 6. Summary Stats */}
      {edaData.info && (
        <div className="glass-card">
          <div className="card-header"><h3 className="card-title">Dataset Summary</h3></div>
          <div className="grid-3 stagger">
            <div style={{ textAlign: 'center' }}>
              <div className="metric-label">Total Records</div>
              <div className="metric-value neutral">{edaData.info.total_records.toLocaleString()}</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div className="metric-label">Date Range</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.875rem', color: 'var(--text-primary)' }}>
                {edaData.info.date_range.start} → {edaData.info.date_range.end}
              </div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div className="metric-label">Enriched Features</div>
              <div className="metric-value neutral">{edaData.info.enriched_columns.length}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
