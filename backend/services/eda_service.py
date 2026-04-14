"""EDA service — Compute exploratory data analysis statistics."""

import numpy as np
import pandas as pd
from services.data_service import get_stock_data
from services.feature_engineering import add_technical_indicators, clean_data


def get_eda_summary(start_date=None, end_date=None):
    """
    Compute comprehensive EDA statistics for TSLA stock data.
    
    Returns dict with:
        - summary_stats: describe() output
        - correlation_matrix: feature correlations
        - price_with_ma: closing price + moving averages time series
        - volume_trend: monthly volume aggregations
        - daily_returns: distribution data
    """
    df = get_stock_data(start_date, end_date)
    df_enriched = add_technical_indicators(df)
    df_enriched = clean_data(df_enriched)
    
    result = {}
    
    # 1. Summary statistics
    numeric_cols = df_enriched.select_dtypes(include=[np.number]).columns.tolist()
    summary = df_enriched[numeric_cols].describe()
    result["summary_stats"] = summary.round(4).to_dict()
    
    # 2. Correlation matrix
    corr = df_enriched[numeric_cols].corr()
    result["correlation_matrix"] = {
        "columns": corr.columns.tolist(),
        "values": corr.round(4).values.tolist()
    }
    
    # 3. Price with moving averages (time series)
    ma_cols = ["Close", "MA_20", "MA_50", "MA_200"]
    available_ma = [c for c in ma_cols if c in df_enriched.columns]
    price_ma = df_enriched[["Date"] + available_ma].copy()
    price_ma["Date"] = price_ma["Date"].dt.strftime("%Y-%m-%d")
    result["price_with_ma"] = price_ma.to_dict(orient="records")
    
    # 4. Volume trend (monthly aggregation)
    df_vol = df_enriched[["Date", "Volume"]].copy()
    df_vol["Month"] = df_vol["Date"].dt.to_period("M").astype(str)
    monthly_vol = df_vol.groupby("Month")["Volume"].sum().reset_index()
    result["volume_trend"] = monthly_vol.to_dict(orient="records")
    
    # 5. Daily returns distribution
    if "Daily_Return" in df_enriched.columns:
        returns = df_enriched["Daily_Return"].dropna()
        hist, bin_edges = np.histogram(returns, bins=50)
        result["returns_distribution"] = {
            "counts": hist.tolist(),
            "bin_edges": np.round(bin_edges, 6).tolist(),
            "mean": round(float(returns.mean()), 6),
            "std": round(float(returns.std()), 6),
            "skew": round(float(returns.skew()), 4),
            "kurtosis": round(float(returns.kurtosis()), 4),
        }
    
    # 6. OHLCV data for candlestick chart
    ohlcv = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
    ohlcv["Date"] = ohlcv["Date"].dt.strftime("%Y-%m-%d")
    result["ohlcv"] = ohlcv.to_dict(orient="records")
    
    # 7. RSI over time
    if "RSI_14" in df_enriched.columns:
        rsi_data = df_enriched[["Date", "RSI_14"]].copy()
        rsi_data["Date"] = rsi_data["Date"].dt.strftime("%Y-%m-%d")
        result["rsi"] = rsi_data.to_dict(orient="records")
    
    # 8. Basic info
    result["info"] = {
        "total_records": len(df),
        "date_range": {
            "start": df["Date"].min().strftime("%Y-%m-%d"),
            "end": df["Date"].max().strftime("%Y-%m-%d"),
        },
        "columns": df.columns.tolist(),
        "enriched_columns": df_enriched.columns.tolist(),
    }
    
    return result
