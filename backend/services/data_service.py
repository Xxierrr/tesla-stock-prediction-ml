"""Data service — Fetch and cache Tesla stock data via yfinance."""

import os
import pandas as pd
import yfinance as yf
from config import TICKER, DATA_DIR, DEFAULT_START_DATE, DEFAULT_END_DATE


def get_stock_data(start_date=None, end_date=None, force_refresh=False):
    """
    Fetch TSLA historical stock data.
    Caches to CSV to avoid repeated API calls.
    
    Returns:
        pd.DataFrame with columns: Date, Open, High, Low, Close, Volume
    """
    start = start_date or DEFAULT_START_DATE
    end = end_date or DEFAULT_END_DATE
    
    cache_file = os.path.join(DATA_DIR, f"{TICKER}_{start}_{end}.csv")
    
    if not force_refresh and os.path.exists(cache_file):
        df = pd.read_csv(cache_file, parse_dates=["Date"])
        return df
    
    # Download from Yahoo Finance
    raw = yf.download(TICKER, start=start, end=end, progress=False)
    
    if raw.empty:
        raise ValueError(f"No data returned for {TICKER} between {start} and {end}")
    
    # Flatten multi-level columns if present
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    
    # Reset index to get Date as a column
    df = raw.reset_index()
    
    # Ensure standard column names
    df = df.rename(columns={
        "Adj Close": "Adj_Close"
    })
    
    # Keep only needed columns
    keep_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    available = [c for c in keep_cols if c in df.columns]
    df = df[available].copy()
    
    # Clean
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df = df.dropna()
    
    # Cache
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(cache_file, index=False)
    
    return df


def get_realtime_price():
    """Get the latest TSLA price info."""
    ticker = yf.Ticker(TICKER)
    info = ticker.fast_info
    
    try:
        history = ticker.history(period="2d")
        if len(history) >= 2:
            prev_close = float(history["Close"].iloc[-2])
            current = float(history["Close"].iloc[-1])
            change = current - prev_close
            change_pct = (change / prev_close) * 100
        else:
            current = float(info.last_price) if hasattr(info, 'last_price') else 0
            prev_close = float(info.previous_close) if hasattr(info, 'previous_close') else current
            change = current - prev_close
            change_pct = (change / prev_close * 100) if prev_close != 0 else 0
    except Exception:
        current = float(info.last_price) if hasattr(info, 'last_price') else 0
        change = 0
        change_pct = 0
        prev_close = current
    
    return {
        "symbol": TICKER,
        "price": round(current, 2),
        "change": round(change, 2),
        "changePercent": round(change_pct, 2),
        "previousClose": round(prev_close, 2),
    }


def get_stock_data_json(start_date=None, end_date=None):
    """Return stock data as JSON-serializable dict."""
    df = get_stock_data(start_date, end_date)
    df_out = df.copy()
    df_out["Date"] = df_out["Date"].dt.strftime("%Y-%m-%d")
    return df_out.to_dict(orient="records")
