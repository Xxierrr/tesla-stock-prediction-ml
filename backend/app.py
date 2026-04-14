"""
TeslaPulse — Flask API for Tesla Stock Price Prediction.

Endpoints:
    GET  /api/stock-data          Fetch historical TSLA data
    GET  /api/eda                 EDA statistics & visualisation data
    POST /api/train               Train all ML models
    POST /api/predict             Run predictions with a specific model
    GET  /api/models/compare      Compare saved model metrics
    GET  /api/realtime            Current TSLA price
    GET  /api/predictions/history Past prediction records
"""

import sys
import os

# Ensure project root is on path so services/ and utils/ are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import FLASK_PORT, FLASK_DEBUG
from services.data_service import get_stock_data_json, get_realtime_price
from services.eda_service import get_eda_summary
from services.model_service import train_all_models, predict_with_model
from services.db_service import get_prediction_history, get_latest_model_results

app = Flask(__name__)
CORS(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "TeslaPulse API"})


# ---------------------------------------------------------------------------
# Stock Data
# ---------------------------------------------------------------------------

@app.route("/api/stock-data", methods=["GET"])
def stock_data():
    """Fetch historical TSLA data. Query params: start, end."""
    try:
        start = request.args.get("start")
        end = request.args.get("end")
        data = get_stock_data_json(start, end)
        return jsonify({"success": True, "data": data, "count": len(data)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# EDA
# ---------------------------------------------------------------------------

@app.route("/api/eda", methods=["GET"])
def eda():
    """Return EDA statistics and chart data."""
    try:
        start = request.args.get("start")
        end = request.args.get("end")
        result = get_eda_summary(start, end)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Train Models
# ---------------------------------------------------------------------------

@app.route("/api/train", methods=["POST"])
def train():
    """Train all ML models. Body JSON: { start, end } (optional)."""
    try:
        body = request.get_json(silent=True) or {}
        start = body.get("start")
        end = body.get("end")
        results = train_all_models(start, end)
        return jsonify({"success": True, "data": results})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Predict
# ---------------------------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def predict():
    """Run prediction with a trained model. Body: { model, start, end }."""
    try:
        body = request.get_json(silent=True) or {}
        model_name = body.get("model", "random_forest")
        start = body.get("start")
        end = body.get("end")
        result = predict_with_model(model_name, start, end)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Model Comparison
# ---------------------------------------------------------------------------

@app.route("/api/models/compare", methods=["GET"])
def compare_models():
    """Return latest saved metrics for each trained model."""
    try:
        results = get_latest_model_results()
        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Real-time Price
# ---------------------------------------------------------------------------

@app.route("/api/realtime", methods=["GET"])
def realtime():
    """Get current TSLA price."""
    try:
        data = get_realtime_price()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Prediction History
# ---------------------------------------------------------------------------

@app.route("/api/predictions/history", methods=["GET"])
def prediction_history():
    """Get past predictions from the database."""
    try:
        limit = request.args.get("limit", 50, type=int)
        history = get_prediction_history(limit)
        return jsonify({"success": True, "data": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
