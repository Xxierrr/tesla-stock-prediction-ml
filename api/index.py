"""
Vercel Serverless Entry Point
Routes all /api/* requests to Flask backend app.
"""
import sys
import os
import traceback

# Add backend directory to Python path so imports work
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend')
sys.path.insert(0, backend_dir)

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Root API endpoint
@app.route("/api", methods=["GET", "OPTIONS"])
@app.route("/api/", methods=["GET", "OPTIONS"])
def api_root():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({
        "message": "TeslaPulse API is running",
        "version": "1.0",
        "endpoints": ["/api/health", "/api/stock-data", "/api/realtime", "/api/eda"]
    }), 200

# Health check
@app.route("/api/health", methods=["GET", "OPTIONS"])
def health():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({
        "status": "ok",
        "service": "TeslaPulse API",
        "message": "Backend is healthy"
    }), 200

# Stock data
@app.route("/api/stock-data", methods=["GET", "OPTIONS"])
def stock_data():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.data_service import get_stock_data_json
        start = request.args.get("start")
        end = request.args.get("end")
        data = get_stock_data_json(start, end)
        if "error" in data or not data.get("dates"):
            return jsonify({
                "success": False,
                "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]},
                "message": data.get("message", "No data available")
            }), 200
        return jsonify({"success": True, "data": data, "count": len(data.get("dates", []))}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]},
            "error": str(e), "message": "Failed to fetch stock data"
        }), 200

# Real-time price
@app.route("/api/realtime", methods=["GET", "OPTIONS"])
def realtime():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.data_service import get_realtime_price
        data = get_realtime_price()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        traceback.print_exc()
        fallback = {
            "symbol": "TSLA", "price": 449.72, "change": 0.00,
            "changePercent": 0.00, "previousClose": 449.72, "status": "fallback"
        }
        return jsonify({"success": True, "data": fallback, "note": "Using fallback data"}), 200

# EDA
@app.route("/api/eda", methods=["GET", "OPTIONS"])
def eda():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.eda_service import get_eda_summary
        start = request.args.get("start")
        end = request.args.get("end")
        result = get_eda_summary(start, end)
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e), "message": "Failed to generate EDA"}), 200

# Train
@app.route("/api/train", methods=["POST", "OPTIONS"])
def train():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.model_service import train_all_models
        body = request.get_json(silent=True) or {}
        results = train_all_models(body.get("start"), body.get("end"))
        return jsonify({"success": True, "data": results}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e), "message": "Failed to train models"}), 200

# Predict
@app.route("/api/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.model_service import predict_with_model
        body = request.get_json(silent=True) or {}
        result = predict_with_model(body.get("model", "random_forest"), body.get("start"), body.get("end"))
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e), "message": "Failed to generate predictions"}), 200

# Model comparison
@app.route("/api/models/compare", methods=["GET", "OPTIONS"])
def compare_models():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.db_service import get_latest_model_results
        results = get_latest_model_results()
        return jsonify({"success": True, "data": results}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e), "message": "Failed to compare models"}), 200

# Prediction history
@app.route("/api/predictions/history", methods=["GET", "OPTIONS"])
def prediction_history():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.db_service import get_prediction_history
        limit = request.args.get("limit", 50, type=int)
        history = get_prediction_history(limit)
        return jsonify({"success": True, "data": history}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e), "message": "Failed to fetch prediction history"}), 200
