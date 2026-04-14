"""Preprocessing utilities for ML models."""

import numpy as np
from sklearn.preprocessing import MinMaxScaler


def create_sequences(data, target, sequence_length=60):
    """
    Create sequences for LSTM-style models.

    Args:
        data: numpy array of features (n_samples, n_features)
        target: numpy array of target values (n_samples,)
        sequence_length: number of time steps per sequence

    Returns:
        X: (n_sequences, sequence_length, n_features)
        y: (n_sequences,)
    """
    X, y = [], []
    for i in range(sequence_length, len(data)):
        X.append(data[i - sequence_length:i])
        y.append(target[i])
    return np.array(X), np.array(y)


def scale_data(train_data, test_data=None):
    """
    Scale data using MinMaxScaler.

    Returns:
        scaled_train, scaled_test (or None), scaler
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(train_data)

    scaled_test = None
    if test_data is not None:
        scaled_test = scaler.transform(test_data)

    return scaled_train, scaled_test, scaler


def inverse_scale(scaler, data, column_index=0):
    """
    Inverse transform scaled predictions.
    Handles single-column inverse by creating a placeholder array.
    """
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    # If scaler was fit on multiple features, create a dummy array
    if scaler.n_features_in_ > 1:
        dummy = np.zeros((len(data), scaler.n_features_in_))
        dummy[:, column_index] = data[:, 0]
        inverted = scaler.inverse_transform(dummy)
        return inverted[:, column_index]
    else:
        return scaler.inverse_transform(data).flatten()


def split_time_series(df, test_size=0.2):
    """
    Split time series data maintaining temporal order (no shuffle).

    Returns:
        train_df, test_df
    """
    split_idx = int(len(df) * (1 - test_size))
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    return train_df, test_df
