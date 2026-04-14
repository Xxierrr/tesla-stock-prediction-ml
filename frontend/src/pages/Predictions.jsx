/**
 * Predictions — Train models, view predictions, compare performance.
 */
import React, { useState } from 'react';
import { trainModels } from '../services/api';
import DateRangeForm from '../components/DateRangeForm';
import PredictionPanel from '../components/PredictionPanel';
import ModelComparison from '../components/ModelComparison';
import Loader from '../components/Loader';
import { BrainCircuit, Layers } from 'lucide-react';

export default function Predictions() {
  const [results, setResults] = useState(null);
  const [activeModel, setActiveModel] = useState('linear_regression');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('predictions');

  const handleTrain = async (start, end) => {
    setLoading(true);
    setError(null);
    try {
      const res = await trainModels(start, end);
      if (res.success && res.data) {
        setResults(res.data);
      } else {
        setError(res.error || res.message || 'Failed to train models');
        setResults(null);
      }
    } catch (e) {
      console.error('Train error:', e);
      setError(e.message || 'Failed to train models');
      setResults(null);
    }
    setLoading(false);
  };

  const modelOptions = [
    { key: 'linear_regression', label: 'Linear Regression', tag: 'lr' },
    { key: 'random_forest', label: 'Random Forest', tag: 'rf' },
    { key: 'lstm', label: 'LSTM (Deep Learning)', tag: 'lstm' },
  ];

  return (
    <div>
      <h1 className="page-title">Model Training & Predictions</h1>
      <p className="page-subtitle">Train ML models on Tesla stock data and compare performance</p>

      <div style={{ display: 'flex', gap: '2rem' }}>
        {/* Left Side: Controls */}
        <div style={{ width: '300px', flexShrink: 0 }}>
          <div className="panel">
            <div className="panel-header">Train Models</div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              Trains Linear Regression, Random Forest, and LSTM with K-Fold validation
            </div>
            <DateRangeForm onSubmit={handleTrain} loading={loading} buttonText="Train Models" />
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
            <Loader message="Training models... This may take a minute. Please wait." />
          ) : results ? (
            <>
              {/* Tabs */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
                <div className="tabs">
                  <button className={`tab ${activeTab === 'predictions' ? 'active' : ''}`} onClick={() => setActiveTab('predictions')}>
                    Predictions
                  </button>
                  <button className={`tab ${activeTab === 'comparison' ? 'active' : ''}`} onClick={() => setActiveTab('comparison')}>
                    Comparison
                  </button>
                </div>

                {activeTab === 'predictions' && (
                  <div className="tabs" style={{ marginBottom: 0 }}>
                    {modelOptions.map(m => (
                      <button
                        key={m.key}
                        className={`tab ${activeModel === m.key ? 'active' : ''}`}
                        onClick={() => setActiveModel(m.key)}
                        style={{ padding: '0.25rem 0.75rem', fontSize: '0.8125rem' }}
                      >
                        {m.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Content */}
              {activeTab === 'predictions' ? (
                <PredictionPanel results={results} activeModel={activeModel} />
              ) : (
                <ModelComparison results={results} />
              )}
            </>
          ) : (
            <div style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              <p>Select a date range and click "Train Models" to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
