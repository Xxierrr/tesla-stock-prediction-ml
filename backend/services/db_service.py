"""Database service — SQLite storage for prediction history."""

import sqlite3
import json
import os
from datetime import datetime
from config import DB_PATH


def _get_connection():
    """Get SQLite connection, creating DB and tables if needed."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            metrics TEXT,
            predicted_values TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS model_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            rmse REAL,
            mae REAL,
            r2 REAL,
            training_time REAL,
            kfold_scores TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_prediction(model_name, start_date, end_date, metrics, predicted_values):
    """Save a prediction result to the database."""
    conn = _get_connection()
    try:
        conn.execute(
            """INSERT INTO predictions (model_name, start_date, end_date, metrics, predicted_values, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                model_name,
                start_date,
                end_date,
                json.dumps(metrics),
                json.dumps(predicted_values[:100] if len(predicted_values) > 100 else predicted_values),
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def save_model_result(model_name, rmse, mae, r2, training_time, kfold_scores=None):
    """Save model training results."""
    conn = _get_connection()
    try:
        conn.execute(
            """INSERT INTO model_results (model_name, rmse, mae, r2, training_time, kfold_scores, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                model_name,
                rmse,
                mae,
                r2,
                training_time,
                json.dumps(kfold_scores) if kfold_scores else None,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_prediction_history(limit=50):
    """Retrieve past predictions."""
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_latest_model_results():
    """Get the most recent result for each model."""
    conn = _get_connection()
    try:
        rows = conn.execute("""
            SELECT m1.* FROM model_results m1
            INNER JOIN (
                SELECT model_name, MAX(created_at) as max_date
                FROM model_results GROUP BY model_name
            ) m2 ON m1.model_name = m2.model_name AND m1.created_at = m2.max_date
            ORDER BY m1.r2 DESC
        """).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            if d.get("kfold_scores"):
                d["kfold_scores"] = json.loads(d["kfold_scores"])
            results.append(d)
        return results
    finally:
        conn.close()
