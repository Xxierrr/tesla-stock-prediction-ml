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
    try:
        from datetime import datetime
        
        start = start_date or DEFAULT_START_DATE
        end = end_date or DEFAULT_END_DATE
        
        # Validate and cap end date to today
        today = datetime.now().strftime("%Y-%m-%d")
        if end > today:
            print(f"End date {end} is in the future, capping to today {today}")
            end = today
        
        cache_file = os.path.join(DATA_DIR, f"{TICKER}_{start}_{end}.csv")
        
        # Try cache first
        if not force_refresh and os.path.exists(cache_file):
            try:
                df = pd.read_csv(cache_file, parse_dates=["Date"])
                if not df.empty:
                    print(f"Loaded {len(df)} rows from cache")
                    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)
                    return df
            except Exception as e:
                print(f"Cache read failed: {e}")
        
        # Download from Yahoo Finance
        print(f"Fetching TSLA data from {start} to {end}")
        ticker = yf.Ticker(TICKER)
        raw = ticker.history(start=start, end=end)
        
        if raw.empty:
            print(f"No data returned from yfinance for {start} to {end}")
            # Return empty dataframe with correct structure
            return pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])
        
        print(f"Fetched {len(raw)} rows from yfinance")
        
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
        df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)
        df = df.sort_values("Date").reset_index(drop=True)
        df = df.dropna()
        
        print(f"Cleaned data: {len(df)} rows")
        
        # Try to cache (may fail on Vercel read-only filesystem)
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            df.to_csv(cache_file, index=False)
        except Exception as e:
            print(f"Cache write failed (expected on Vercel): {e}")
        
        return df
    
    except Exception as e:
        print(f"get_stock_data failed: {e}")
        import traceback
        traceback.print_exc()
        # Return empty dataframe with correct structure
        return pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])


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
    """Return stock data as JSON-serializable dict with fallback."""
    try:
        df = get_stock_data(start_date, end_date)
        
        if df.empty:
            return {
                "dates": [],
                "open": [],
                "high": [],
                "low": [],
                "close": [],
                "volume": [],
                "message": "No data available"
            }
        
        df_out = df.copy()
        df_out["Date"] = df_out["Date"].dt.strftime("%Y-%m-%d")
        
        # Return structured format
        result = {
            "dates": df_out["Date"].tolist(),
            "close": df_out["Close"].tolist() if "Close" in df_out.columns else [],
            "open": df_out["Open"].tolist() if "Open" in df_out.columns else [],
            "high": df_out["High"].tolist() if "High" in df_out.columns else [],
            "low": df_out["Low"].tolist() if "Low" in df_out.columns else [],
            "volume": df_out["Volume"].tolist() if "Volume" in df_out.columns else [],
        }
        
        # Also include records format for compatibility
        result["records"] = df_out.to_dict(orient="records")
        
        return result
    
    except Exception as e:
        print(f"get_stock_data_json failed: {e}")
        return {
            "dates": [],
            "open": [],
            "high": [],
            "low": [],
            "close": [],
            "volume": [],
            "records": [],
            "error": str(e),
            "message": "Failed to fetch data"
        }
