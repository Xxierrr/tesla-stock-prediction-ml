"""Utility functions for metrics calculation."""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def calculate_rmse(y_true, y_pred):
    """Calculate Root Mean Squared Error."""
    return round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4)


def calculate_mae(y_true, y_pred):
    """Calculate Mean Absolute Error."""
    return round(float(mean_absolute_error(y_true, y_pred)), 4)


def calculate_r2(y_true, y_pred):
    """Calculate R² Score."""
    return round(float(r2_score(y_true, y_pred)), 4)


def calculate_all_metrics(y_true, y_pred):
    """Calculate all metrics at once."""
    return {
        "rmse": calculate_rmse(y_true, y_pred),
        "mae": calculate_mae(y_true, y_pred),
        "r2": calculate_r2(y_true, y_pred),
    }


def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = y_true != 0
    return round(float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100), 4)
