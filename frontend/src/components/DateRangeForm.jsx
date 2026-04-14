/**
 * DateRangeForm — Input form for custom date range selection.
 */
import React, { useState } from 'react';
import { Calendar, Play } from 'lucide-react';

export default function DateRangeForm({ onSubmit, loading = false, buttonText = 'Fetch Data' }) {
  const [start, setStart] = useState('2020-01-01');
  const [end, setEnd] = useState('2026-01-01');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(start, end);
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <div className="form-group">
        <label htmlFor="start-date-input">Start Date</label>
        <input
          type="date"
          className="input"
          value={start}
          onChange={(e) => setStart(e.target.value)}
          id="start-date-input"
        />
      </div>
      <div className="form-group">
        <label htmlFor="end-date-input">End Date</label>
        <input
          type="date"
          className="input"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          id="end-date-input"
        />
      </div>
      <button type="submit" className="btn" disabled={loading} id="submit-date-range">
        {loading ? 'Processing...' : buttonText}
      </button>
    </form>
  );
}
