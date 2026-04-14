"""TeslaPulse Flask API - Production Ready"""
import sys, os, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from config import FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

def safe_route(fallback=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"ERROR: {str(e)}")
                traceback.print_exc()
                res = {"success": False, "error": "Something went wrong", "details": str(e)}
                if fallback: res.update(fallback)
                return jsonify(res), 500
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@app.route("/", methods=["GET", "OPTIONS"])
def root():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({"message": "Backend is working 🚀"})

@app.route("/api", methods=["GET", "OPTIONS"])
def api_root():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({"message": "API is working ✅"})

@app.route("/api/health", methods=["GET", "OPTIONS"])
def health():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "ok", "service": "TeslaPulse API"})

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
            return jsonify({"success": False, "data": {"dates": [], "open": [], "high": [], "low": [], "close": [], "volume": [], "records": []}, "message": data.get("message", "No data available")})
        return jsonify({"success": True, "data": data, "count": len(data.get("dates", []))})
    except Exception as e:
        print(f"stock_data failed: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "data": {"dates": [], "open": [], "high": [], "low": [], "close": [], "volume": [], "records": []}, "error": str(e)}), 500

@app.route("/api/eda", methods=["GET", "OPTIONS"])
@safe_route()
def eda():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    from services.eda_service import get_eda_summary
    start = request.args.get("start")
    end = request.args.get("end")
    result = get_eda_summary(start, end)
    return jsonify({"success": True, "data": result})

@app.route("/api/train", methods=["POST", "OPTIONS"])
@safe_route()
def train():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    from services.model_service import train_all_models
    body = request.get_json(silent=True) or {}
    start = body.get("start")
    end = body.get("end")
    results = train_all_models(start, end)
    return jsonify({"success": True, "data": results})

@app.route("/api/predict", methods=["POST", "OPTIONS"])
@safe_route()
def predict():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    from services.model_service import predict_with_model
    body = request.get_json(silent=True) or {}
    model_name = body.get("model", "random_forest")
    start = body.get("start")
    end = body.get("end")
    result = predict_with_model(model_name, start, end)
    return jsonify({"success": True, "data": result})

@app.route("/api/models/compare", methods=["GET", "OPTIONS"])
@safe_route()
def compare_models():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    from services.db_service import get_latest_model_results
    results = get_latest_model_results()
    return jsonify({"success": True, "data": results})

@app.route("/api/realtime", methods=["GET", "OPTIONS"])
def realtime():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        from services.data_service import get_realtime_price
        data = get_realtime_price()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        print(f"Realtime failed: {str(e)}")
        traceback.print_exc()
        fallback = {"symbol": "TSLA", "price": 449.72, "change": 0.00, "changePercent": 0.00, "previousClose": 449.72, "status": "fallback"}
        return jsonify({"success": True, "data": fallback})

@app.route("/api/predictions/history", methods=["GET", "OPTIONS"])
@safe_route()
def prediction_history():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    from services.db_service import get_prediction_history
    limit = request.args.get("limit", 50, type=int)
    history = get_prediction_history(limit)
    return jsonify({"success": True, "data": history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
