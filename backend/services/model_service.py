"""Model service — Train, evaluate, and predict with ML models."""

import os
import time
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler

from config import (
    MODELS_DIR, TEST_SIZE, N_SPLITS, RANDOM_STATE,
    LSTM_SEQUENCE_LENGTH, LSTM_EPOCHS, LSTM_BATCH_SIZE,
    RF_N_ESTIMATORS, RF_MAX_DEPTH,
)
from services.data_service import get_stock_data
from services.feature_engineering import (
    prepare_data_pipeline, get_feature_columns, get_feature_importance_data,
)
from utils.metrics import calculate_all_metrics, calculate_mape
from utils.preprocessing import create_sequences, split_time_series
from services.db_service import save_model_result, save_prediction


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_models_dir():
    os.makedirs(MODELS_DIR, exist_ok=True)


def _save_model(model, name):
    _ensure_models_dir()
    path = os.path.join(MODELS_DIR, f"{name}.pkl")
    joblib.dump(model, path)
    return path


def _load_model(name):
    path = os.path.join(MODELS_DIR, f"{name}.pkl")
    if os.path.exists(path):
        return joblib.load(path)
    return None


def _save_scaler(scaler, name):
    _ensure_models_dir()
    path = os.path.join(MODELS_DIR, f"{name}_scaler.pkl")
    joblib.dump(scaler, path)


def _load_scaler(name):
    path = os.path.join(MODELS_DIR, f"{name}_scaler.pkl")
    if os.path.exists(path):
        return joblib.load(path)
    return None


# ---------------------------------------------------------------------------
# Data preparation
# ---------------------------------------------------------------------------

def prepare_training_data(start_date=None, end_date=None):
    """
    Full pipeline: fetch → engineer features → split.
    Returns train/test DataFrames plus metadata.
    """
    df = get_stock_data(start_date, end_date)
    df = prepare_data_pipeline(df)

    feature_info = get_feature_importance_data(df)
    top_features = feature_info["top_features"]

    # Use top correlated features (at most 10)
    feature_cols = [f for f in top_features if f in df.columns]
    if not feature_cols:
        feature_cols = get_feature_columns(df)

    train_df, test_df = split_time_series(df, TEST_SIZE)

    return {
        "df": df,
        "train_df": train_df,
        "test_df": test_df,
        "feature_cols": feature_cols,
        "feature_info": feature_info,
    }


# ---------------------------------------------------------------------------
# Model 1 – Linear Regression
# ---------------------------------------------------------------------------

def train_linear_regression(data):
    """Train a Linear Regression model."""
    t0 = time.time()

    X_train = data["train_df"][data["feature_cols"]].values
    y_train = data["train_df"]["Close"].values
    X_test = data["test_df"][data["feature_cols"]].values
    y_test = data["test_df"]["Close"].values

    scaler = MinMaxScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_s, y_train)

    y_pred = model.predict(X_test_s)
    metrics = calculate_all_metrics(y_test, y_pred)
    metrics["mape"] = calculate_mape(y_test, y_pred)

    # K-Fold
    kfold_scores = _kfold_validate(model, X_train_s, y_train)

    train_time = round(time.time() - t0, 3)

    _save_model(model, "linear_regression")
    _save_scaler(scaler, "linear_regression")

    save_model_result("Linear Regression", metrics["rmse"], metrics["mae"],
                      metrics["r2"], train_time, kfold_scores)

    dates = data["test_df"]["Date"].dt.strftime("%Y-%m-%d").tolist()

    return {
        "model_name": "Linear Regression",
        "metrics": metrics,
        "kfold_scores": kfold_scores,
        "training_time": train_time,
        "predictions": {
            "dates": dates,
            "actual": y_test.tolist(),
            "predicted": y_pred.tolist(),
        },
    }


# ---------------------------------------------------------------------------
# Model 2 – Random Forest
# ---------------------------------------------------------------------------

def train_random_forest(data):
    """Train a Random Forest Regressor."""
    t0 = time.time()

    X_train = data["train_df"][data["feature_cols"]].values
    y_train = data["train_df"]["Close"].values
    X_test = data["test_df"][data["feature_cols"]].values
    y_test = data["test_df"]["Close"].values

    scaler = MinMaxScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = RandomForestRegressor(
        n_estimators=RF_N_ESTIMATORS,
        max_depth=RF_MAX_DEPTH,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train_s, y_train)

    y_pred = model.predict(X_test_s)
    metrics = calculate_all_metrics(y_test, y_pred)
    metrics["mape"] = calculate_mape(y_test, y_pred)

    kfold_scores = _kfold_validate(model, X_train_s, y_train)

    train_time = round(time.time() - t0, 3)

    _save_model(model, "random_forest")
    _save_scaler(scaler, "random_forest")

    # Feature importance from the RF model
    feat_imp = dict(zip(data["feature_cols"],
                        model.feature_importances_.tolist()))

    dates = data["test_df"]["Date"].dt.strftime("%Y-%m-%d").tolist()

    save_model_result("Random Forest", metrics["rmse"], metrics["mae"],
                      metrics["r2"], train_time, kfold_scores)

    return {
        "model_name": "Random Forest",
        "metrics": metrics,
        "kfold_scores": kfold_scores,
        "training_time": train_time,
        "feature_importance": feat_imp,
        "predictions": {
            "dates": dates,
            "actual": y_test.tolist(),
            "predicted": y_pred.tolist(),
        },
    }


# ---------------------------------------------------------------------------
# Model 3 – LSTM (via MLPRegressor as a deep-learning proxy)
#
# NOTE: TensorFlow/Keras does not yet support Python 3.14.
# We use sklearn's MLPRegressor with sequence-flattened features
# to emulate a deep neural network approach.  When TF support
# lands for 3.14 this can be swapped to a true LSTM.
# ---------------------------------------------------------------------------

def train_lstm(data):
    """Train an MLP-based deep learning model on sequential features."""
    t0 = time.time()

    close_col_idx = None
    feature_cols = data["feature_cols"]
    all_cols = feature_cols + ["Close"]

    train_vals = data["train_df"][all_cols].values
    test_vals = data["test_df"][all_cols].values

    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_vals)
    test_scaled = scaler.transform(test_vals)

    close_idx = len(feature_cols)  # last column is Close

    # Create sequences
    seq_len = min(LSTM_SEQUENCE_LENGTH, len(train_scaled) - 1)
    X_train_seq, y_train_seq = create_sequences(
        train_scaled[:, :close_idx], train_scaled[:, close_idx], seq_len
    )
    X_test_seq, y_test_seq = create_sequences(
        test_scaled[:, :close_idx], test_scaled[:, close_idx], seq_len
    )

    # Flatten sequences for MLP: (samples, seq_len * n_features)
    n_train = X_train_seq.shape[0]
    n_test = X_test_seq.shape[0]
    n_feat_flat = X_train_seq.shape[1] * X_train_seq.shape[2]
    X_train_flat = X_train_seq.reshape(n_train, n_feat_flat)
    X_test_flat = X_test_seq.reshape(n_test, n_feat_flat)

    model = MLPRegressor(
        hidden_layer_sizes=(128, 64, 32),
        activation="relu",
        solver="adam",
        max_iter=LSTM_EPOCHS * 5,
        random_state=RANDOM_STATE,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        batch_size=min(LSTM_BATCH_SIZE, n_train),
    )
    model.fit(X_train_flat, y_train_seq)

    y_pred_scaled = model.predict(X_test_flat)

    # Inverse-transform predictions
    dummy = np.zeros((len(y_pred_scaled), scaler.n_features_in_))
    dummy[:, close_idx] = y_pred_scaled
    y_pred = scaler.inverse_transform(dummy)[:, close_idx]

    dummy_actual = np.zeros((len(y_test_seq), scaler.n_features_in_))
    dummy_actual[:, close_idx] = y_test_seq
    y_actual = scaler.inverse_transform(dummy_actual)[:, close_idx]

    metrics = calculate_all_metrics(y_actual, y_pred)
    metrics["mape"] = calculate_mape(y_actual, y_pred)

    # K-Fold on flattened sequences
    kfold_scores = _kfold_validate(model, X_train_flat, y_train_seq)

    train_time = round(time.time() - t0, 3)

    _save_model(model, "lstm_mlp")
    _save_scaler(scaler, "lstm_mlp")

    # Dates corresponding to test sequences
    test_dates = data["test_df"]["Date"].dt.strftime("%Y-%m-%d").tolist()
    test_dates = test_dates[seq_len:]

    save_model_result("LSTM (Deep Learning)", metrics["rmse"], metrics["mae"],
                      metrics["r2"], train_time, kfold_scores)

    return {
        "model_name": "LSTM (Deep Learning)",
        "metrics": metrics,
        "kfold_scores": kfold_scores,
        "training_time": train_time,
        "predictions": {
            "dates": test_dates,
            "actual": y_actual.tolist(),
            "predicted": y_pred.tolist(),
        },
    }


# ---------------------------------------------------------------------------
# K-Fold Cross Validation (Time Series Split)
# ---------------------------------------------------------------------------

def _kfold_validate(model, X, y):
    """
    Perform K-Fold cross validation using TimeSeriesSplit.
    Returns list of R² scores per fold.
    """
    tscv = TimeSeriesSplit(n_splits=N_SPLITS)
    scores = []
    for train_idx, val_idx in tscv.split(X):
        X_tr, X_val = X[train_idx], X[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]

        # Clone-like refit
        from sklearn.base import clone
        m = clone(model)
        m.fit(X_tr, y_tr)
        y_p = m.predict(X_val)
        fold_metrics = calculate_all_metrics(y_val, y_p)
        scores.append(fold_metrics)

    return scores


# ---------------------------------------------------------------------------
# Train all models
# ---------------------------------------------------------------------------

def train_all_models(start_date=None, end_date=None):
    """Train all three models and return comparative results."""
    data = prepare_training_data(start_date, end_date)

    results = {}

    # Linear Regression
    results["linear_regression"] = train_linear_regression(data)

    # Random Forest
    results["random_forest"] = train_random_forest(data)

    # LSTM / Deep Learning
    results["lstm"] = train_lstm(data)

    # Summary comparison
    results["comparison"] = {
        "models": [],
        "best_model": None,
    }

    best_r2 = -float("inf")
    for key in ["linear_regression", "random_forest", "lstm"]:
        r = results[key]
        results["comparison"]["models"].append({
            "name": r["model_name"],
            "rmse": r["metrics"]["rmse"],
            "mae": r["metrics"]["mae"],
            "r2": r["metrics"]["r2"],
            "mape": r["metrics"]["mape"],
            "training_time": r["training_time"],
        })
        if r["metrics"]["r2"] > best_r2:
            best_r2 = r["metrics"]["r2"]
            results["comparison"]["best_model"] = r["model_name"]

    results["feature_info"] = data["feature_info"]
    results["data_info"] = {
        "total_samples": len(data["df"]),
        "train_samples": len(data["train_df"]),
        "test_samples": len(data["test_df"]),
        "features_used": data["feature_cols"],
    }

    return results


# ---------------------------------------------------------------------------
# Predict with a saved model
# ---------------------------------------------------------------------------

def predict_with_model(model_name, start_date=None, end_date=None):
    """Load a trained model and run predictions on new data."""
    name_map = {
        "linear_regression": "linear_regression",
        "random_forest": "random_forest",
        "lstm": "lstm_mlp",
    }

    model_key = name_map.get(model_name)
    if not model_key:
        raise ValueError(f"Unknown model: {model_name}")

    model = _load_model(model_key)
    scaler = _load_scaler(model_key)

    if model is None:
        raise ValueError(f"Model '{model_name}' not trained yet. Train first.")

    data = prepare_training_data(start_date, end_date)

    if model_name in ("linear_regression", "random_forest"):
        X = data["test_df"][data["feature_cols"]].values
        y_true = data["test_df"]["Close"].values
        X_s = scaler.transform(X)
        y_pred = model.predict(X_s)
        dates = data["test_df"]["Date"].dt.strftime("%Y-%m-%d").tolist()
    else:
        # LSTM / MLP
        feature_cols = data["feature_cols"]
        all_cols = feature_cols + ["Close"]
        test_vals = data["test_df"][all_cols].values
        test_scaled = scaler.transform(test_vals)
        close_idx = len(feature_cols)
        seq_len = min(LSTM_SEQUENCE_LENGTH, len(test_scaled) - 1)
        X_seq, y_seq = create_sequences(
            test_scaled[:, :close_idx], test_scaled[:, close_idx], seq_len
        )
        X_flat = X_seq.reshape(X_seq.shape[0], -1)
        y_pred_scaled = model.predict(X_flat)

        dummy = np.zeros((len(y_pred_scaled), scaler.n_features_in_))
        dummy[:, close_idx] = y_pred_scaled
        y_pred = scaler.inverse_transform(dummy)[:, close_idx]

        dummy_a = np.zeros((len(y_seq), scaler.n_features_in_))
        dummy_a[:, close_idx] = y_seq
        y_true = scaler.inverse_transform(dummy_a)[:, close_idx]

        dates = data["test_df"]["Date"].dt.strftime("%Y-%m-%d").tolist()[seq_len:]

    metrics = calculate_all_metrics(y_true, y_pred)

    # Save prediction to DB
    save_prediction(
        model_name, start_date or "default", end_date or "default",
        metrics, y_pred.tolist()
    )

    return {
        "model_name": model_name,
        "metrics": metrics,
        "predictions": {
            "dates": dates,
            "actual": y_true.tolist(),
            "predicted": y_pred.tolist(),
        },
    }
