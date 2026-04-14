/**
 * RealTimePrice — Live TSLA price ticker with pulse animation.
 */
import React, { useState, useEffect, useRef } from 'react';
import { getRealtimePrice } from '../services/api';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function RealTimePrice({ compact = false }) {
  const [price, setPrice] = useState(null);
  const [flash, setFlash] = useState(false);
  const prevPrice = useRef(null);

  useEffect(() => {
    let mounted = true;

    const fetch = async () => {
      try {
        const res = await getRealtimePrice();
        if (mounted && res.success) {
          if (prevPrice.current && prevPrice.current !== res.data.price) {
            setFlash(true);
            setTimeout(() => setFlash(false), 600);
          }
          prevPrice.current = res.data.price;
          setPrice(res.data);
        }
      } catch (e) {
        console.error('Realtime price error:', e);
      }
    };

    fetch();
    const interval = setInterval(fetch, 30000);
    return () => { mounted = false; clearInterval(interval); };
  }, []);

  if (!price) {
    return (
      <div className="price-badge">
        <div className="price-dot" />
        <span className="price" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Loading...</span>
      </div>
    );
  }

  const isUp = price.change >= 0;

  if (compact) {
    return (
      <div className="price-badge" style={flash ? { animation: 'priceFlash 0.6s ease' } : {}}>
        <div className="price-dot" style={{ background: isUp ? 'var(--accent-green)' : 'var(--accent-red)' }} />
        <span className="price">${price.price.toFixed(2)}</span>
        <span className={`change ${isUp ? 'up' : 'down'}`}>
          {isUp ? '+' : ''}{price.changePercent.toFixed(2)}%
        </span>
      </div>
    );
  }

  return (
    <div className="glass-card" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', padding: '1.25rem 1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div className="price-dot" style={{ background: isUp ? 'var(--accent-green)' : 'var(--accent-red)' }} />
        <div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>TSLA</div>
          <div style={{
            fontSize: '1.75rem',
            fontWeight: 800,
            fontFamily: 'var(--font-mono)',
            ...(flash ? { animation: 'priceFlash 0.6s ease' } : {})
          }}>
            ${price.price.toFixed(2)}
          </div>
        </div>
      </div>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.375rem',
        padding: '0.375rem 0.75rem',
        borderRadius: '100px',
        background: isUp ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)',
        color: isUp ? 'var(--accent-green)' : 'var(--accent-red)',
        fontWeight: 700,
        fontSize: '0.875rem',
        fontFamily: 'var(--font-mono)'
      }}>
        {isUp ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
        {isUp ? '+' : ''}{price.change.toFixed(2)} ({isUp ? '+' : ''}{price.changePercent.toFixed(2)}%)
      </div>
    </div>
  );
}
