/**
 * Dashboard — Main overview page with real-time price, stock chart, and quick stats.
 */
import React, { useState, useEffect } from 'react';
import { fetchStockData } from '../services/api';
import RealTimePrice from '../components/RealTimePrice';
import StockChart from '../components/StockChart';
import DateRangeForm from '../components/DateRangeForm';
import Loader from '../components/Loader';
import { BarChart3, TrendingUp, DollarSign, Activity } from 'lucide-react';

export default function Dashboard() {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async (start, end) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchStockData(start, end);
      if (res.success) {
        setStockData(res.data);
      } else {
        setError(res.error || 'Failed to fetch data');
      }
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  useEffect(() => { loadData(); }, []);

  // Compute quick stats
  const stats = stockData ? (() => {
    const closes = stockData.map(d => d.Close);
    const latest = closes[closes.length - 1];
    const first = closes[0];
    const max = Math.max(...closes);
    const min = Math.min(...closes);
    const totalVol = stockData.reduce((s, d) => s + d.Volume, 0);
    const change = ((latest - first) / first * 100);
    return { latest, max, min, totalVol, change, count: stockData.length };
  })() : null;

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">Tesla (TSLA) stock overview and historical data analysis</p>

      <div style={{ display: 'flex', gap: '2rem' }}>
        {/* Left Side: Controls */}
        <div style={{ width: '300px', flexShrink: 0 }}>
          <div className="panel">
            <div className="panel-header">Data Source Range</div>
            <DateRangeForm onSubmit={loadData} loading={loading} buttonText="Load Data" />
          </div>
          <div className="panel">
             <div className="panel-header">Live Price</div>
             <RealTimePrice compact />
          </div>
        </div>

        {/* Right Side: Content */}
        <div style={{ flex: 1 }}>
          {error && (
            <div className="panel" style={{ color: 'var(--accent-red)' }}>
              ⚠️ {error}
            </div>
          )}

          {loading ? (
            <Loader message="Fetching Tesla stock data..." />
          ) : stockData ? (
            <>
              {/* Quick Stats */}
              <div className="grid-4" style={{ marginBottom: '1.5rem' }}>
                <div className="metric">
                  <div className="metric-label">Latest Close</div>
                  <div className="metric-value blue">${stats.latest.toFixed(2)}</div>
                </div>
                <div className="metric">
                  <div className="metric-label">Period Change</div>
                  <div className={`metric-value ${stats.change >= 0 ? 'green' : 'red'}`}>
                    {stats.change >= 0 ? '+' : ''}{stats.change.toFixed(2)}%
                  </div>
                </div>
                <div className="metric">
                  <div className="metric-label">All-Time High</div>
                  <div className="metric-value">${stats.max.toFixed(2)}</div>
                </div>
                <div className="metric">
                  <div className="metric-label">Data Points</div>
                  <div className="metric-value">{stats.count.toLocaleString()}</div>
                </div>
              </div>

              {/* Stock Chart */}
              <div className="panel" style={{ padding: '0' }}>
                <div className="panel-header" style={{ padding: '1.25rem', borderBottom: 'none', marginBottom: 0 }}>Historical Price Chart</div>
                <StockChart data={stockData} title="" />
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
