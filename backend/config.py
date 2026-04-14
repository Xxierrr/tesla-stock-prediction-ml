"""Configuration constants for the TeslaPulse backend."""

import os

# Stock ticker
TICKER = "TSLA"

# Default date range (5 years of data)
DEFAULT_START_DATE = "2020-01-01"
DEFAULT_END_DATE = "2026-01-01"

# Data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DB_PATH = os.path.join(BASE_DIR, "data", "predictions.db")

# Feature engineering
MOVING_AVERAGES = [20, 50, 200]
RSI_PERIOD = 14

# Model training
TEST_SIZE = 0.2
N_SPLITS = 5  # K-Fold splits
RANDOM_STATE = 42

# LSTM config
LSTM_SEQUENCE_LENGTH = 60
LSTM_EPOCHS = 50
LSTM_BATCH_SIZE = 32

# Random Forest config
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = 15

# Flask
FLASK_PORT = 5000
FLASK_DEBUG = True
