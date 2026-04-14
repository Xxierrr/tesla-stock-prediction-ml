"""Feature engineering — Create technical indicators and normalize data."""

import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, SMAIndicator
from sklearn.preprocessing import MinMaxScaler
from config import MOVING_AVERAGES, RSI_PERIOD


def add_technical_indicators(df):
    """
    Add technical analysis features to the stock DataFrame.
    
    Features added:
        - MA_20, MA_50, MA_200 (Simple Moving Averages)
        - RSI_14 (Relative Strength Index)
        - BB_upper, BB_lower, BB_mid (Bollinger Bands)
        - MACD, MACD_signal, MACD_diff
        - Daily_Return, Volatility_20
    """
    df = df.copy()
    close = df["Close"]
    
    # Simple Moving Averages
    for period in MOVING_AVERAGES:
        sma = SMAIndicator(close=close, window=period)
        df[f"MA_{period}"] = sma.sma_indicator()
    
    # RSI
    rsi = RSIIndicator(close=close, window=RSI_PERIOD)
    df["RSI_14"] = rsi.rsi()
    
    # Bollinger Bands
    bb = BollingerBands(close=close, window=20, window_dev=2)
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()
    df["BB_mid"] = bb.bollinger_mavg()
    
    # MACD
    macd = MACD(close=close)
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["MACD_diff"] = macd.macd_diff()
    
    # Daily returns
    df["Daily_Return"] = close.pct_change()
    
    # 20-day rolling volatility
    df["Volatility_20"] = close.pct_change().rolling(window=20).std()
    
    # Price range
    df["High_Low_Range"] = df["High"] - df["Low"]
    df["Open_Close_Range"] = df["Close"] - df["Open"]
    
    return df


def clean_data(df):
    """Handle missing values after feature engineering."""
    df = df.copy()
    
    # Forward fill, then drop any remaining NaN rows
    df = df.ffill()
    df = df.dropna()
    df = df.reset_index(drop=True)
    
    return df


def get_feature_columns(df):
    """Get list of feature columns (exclude Date and target)."""
    exclude = ["Date", "Close"]
    return [c for c in df.columns if c not in exclude]


def normalize_features(df, feature_cols, scaler=None):
    """
    Normalize features using MinMaxScaler.
    
    Returns:
        normalized DataFrame, fitted scaler
    """
    df = df.copy()
    
    if scaler is None:
        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])
    else:
        df[feature_cols] = scaler.transform(df[feature_cols])
    
    return df, scaler


def prepare_data_pipeline(df):
    """
    Full data preparation pipeline:
    1. Add technical indicators
    2. Clean data
    3. Return enriched DataFrame
    """
    df = add_technical_indicators(df)
    df = clean_data(df)
    return df


def get_feature_importance_data(df):
    """
    Return feature info for the frontend.
    """
    feature_cols = get_feature_columns(df)
    
    # Compute correlations with Close price
    correlations = {}
    for col in feature_cols:
        corr = df[col].corr(df["Close"])
        correlations[col] = round(float(corr), 4) if not np.isnan(corr) else 0.0
    
    # Sort by absolute correlation
    sorted_features = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    return {
        "features": [f[0] for f in sorted_features],
        "correlations": {f[0]: f[1] for f in sorted_features},
        "top_features": [f[0] for f in sorted_features[:10]]
    }
