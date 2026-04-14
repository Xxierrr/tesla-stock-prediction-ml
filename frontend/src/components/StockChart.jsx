import React from 'react';
import Plot from './Plot';

const CHART_LAYOUT = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { family: 'Inter, sans-serif', color: '#4b5563', size: 12 },
  margin: { t: 40, r: 20, b: 50, l: 60 },
  xaxis: { gridcolor: '#f3f4f6', linecolor: '#e5e7eb', rangeslider: { visible: false } },
  yaxis: { gridcolor: '#f3f4f6', linecolor: '#e5e7eb', title: 'Price (USD)', tickprefix: '$' },
  legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1, font: { size: 11 } },
  hovermode: 'x unified',
  dragmode: 'zoom',
};

export default function StockChart({ data, showVolume = true, title = 'TSLA Stock Price' }) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No chart data available</div>;
  }

  try {
    const dates = data.map(d => d.Date).filter(d => d != null);
    if (dates.length === 0) return <div style={{ padding: '2rem', textAlign: 'center' }}>Invalid date data</div>;

    const traces = [];

    if (data[0].Open != null && data[0].High != null && data[0].Low != null && data[0].Close != null) {
      traces.push({
        type: 'candlestick',
        x: dates,
        open: data.map(d => d.Open),
        high: data.map(d => d.High),
        low: data.map(d => d.Low),
        close: data.map(d => d.Close),
        name: 'OHLC',
        increasing: { line: { color: '#10b981' } },
        decreasing: { line: { color: '#ef4444' } },
      });
    }

    const maColors = { MA_20: '#3b82f6', MA_50: '#f59e0b', MA_200: '#8b5cf6' };
    for (const [key, color] of Object.entries(maColors)) {
      if (data[0][key] != null) {
        traces.push({
          type: 'scatter',
          mode: 'lines',
          x: dates,
          y: data.map(d => d[key]),
          name: key.replace('_', ' '),
          line: { color, width: 1.5 },
        });
      }
    }

    if (traces.length === 0) return <div style={{ padding: '2rem', textAlign: 'center' }}>No valid chart data</div>;

    const layout = { ...CHART_LAYOUT, title: { text: title, font: { size: 16, color: '#f1f5f9' }, x: 0.01, xanchor: 'left' } };

    if (showVolume && data[0].Volume != null) {
      const volumes = data.map(d => d.Volume).filter(v => v != null);
      if (volumes.length > 0) {
        traces.push({
          type: 'bar',
          x: dates,
          y: data.map(d => d.Volume || 0),
          name: 'Volume',
          marker: { color: data.map(d => (d.Close || 0) >= (d.Open || 0) ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)') },
          yaxis: 'y2',
        });
        layout.yaxis2 = { overlaying: 'y', side: 'right', showgrid: false, showticklabels: false, range: [0, Math.max(...volumes) * 4] };
      }
    }

    return (
      <div className="chart-container">
        <Plot data={traces} layout={layout} config={{ responsive: true, displayModeBar: true, displaylogo: false }} style={{ width: '100%', height: '500px' }} />
      </div>
    );
  } catch (error) {
    console.error('StockChart error:', error);
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--accent-red)' }}>Error rendering chart</div>;
  }
}
