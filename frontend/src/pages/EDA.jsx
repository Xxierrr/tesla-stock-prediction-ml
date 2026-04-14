/**
 * EDA — Exploratory Data Analysis page.
 */
import React, { useState, useEffect } from 'react';
import { fetchEDA } from '../services/api';
import EDACharts from '../components/EDACharts';
import DateRangeForm from '../components/DateRangeForm';
import Loader from '../components/Loader';

export default function EDA() {
  const [edaData, setEdaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadEDA = async (start, end) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchEDA(start, end);
      if (res.success && res.data) {
        setEdaData(res.data);
      } else {
        setError(res.error || res.message || 'Failed to fetch EDA data');
        setEdaData(null);
      }
    } catch (e) {
      console.error('EDA load error:', e);
      setError(e.message || 'Failed to load EDA data');
      setEdaData(null);
    }
    setLoading(false);
  };

  useEffect(() => { loadEDA(); }, []);

  return (
    <div>
      <h1 className="page-title">Exploratory Data Analysis</h1>
      <p className="page-subtitle">Visualize trends, correlations, and statistical properties of TSLA stock data</p>

      <div style={{ display: 'flex', gap: '2rem' }}>
        {/* Left Side: Controls */}
        <div style={{ width: '300px', flexShrink: 0 }}>
          <div className="panel">
            <div className="panel-header">Analysis Range</div>
             <DateRangeForm onSubmit={loadEDA} loading={loading} buttonText="Analyze" />
          </div>
        </div>

        {/* Right Side: Content */}
        <div style={{ flex: 1 }}>
          {error && (
            <div className="panel" style={{ color: 'var(--accent-red)', padding: '1.5rem' }}>
              ⚠️ {error}
            </div>
          )}

          {loading ? (
            <Loader message="Running exploratory data analysis..." />
          ) : edaData ? (
            <EDACharts edaData={edaData} />
          ) : !error ? (
            <div className="panel" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              No data available. Please select a date range and click "Analyze".
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
