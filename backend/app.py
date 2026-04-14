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

# Configure CORS properly for production
# Allow requests from your frontend domain
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://tesla-stock-prediction-ml-487y.vercel.app",
            "https://tesla-stock-prediction-ml.vercel.app",
            "http://localhost:5173",  # For local development
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "https://tesla-stock-prediction-ml-487y.vercel.app",
        "https://tesla-stock-prediction-ml.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    
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
    return jsonify({"message": "Backend is working 🚀", "cors": "enabled"})

@app.route("/api", methods=["GET", "OPTIONS"])
def api_root():
    return jsonify({"message": "API is working ✅", "cors": "enabled"})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "TeslaPulse API"})

@app.route("/api/stock-data", methods=["GET"])
def stock_data():
    """Fetch historical TSLA data with fallback."""
    try:
        from services.data_service import get_stock_data_json
        start = request.args.get("start")
        end = request.args.get("end")
        
        data = get_stock_data_json(start, end)
        
        # Check if data fetch failed
        if "error" in data or not data.get("dates"):
            return jsonify({
                "success": False,
                "data": {
                    "dates": [],
                    "open": [],
                    "high": [],
                    "low": [],
                    "close": [],
                    "volume": [],
                    "records": []
                },
                "message": data.get("message", "No data available"),
                "note": "Using fallback empty dataset"
            })
        
        return jsonify({
            "success": True,
            "data": data,
            "count": len(data.get("dates", []))
        })
    
    except Exception as e:
        print(f"stock_data endpoint failed: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "data": {
                "dates": [],
                "open": [],
                "high": [],
                "low": [],
                "close": [],
                "volume": [],
                "records": []
            },
            "error": "Something went wrong",
            "details": str(e),
            "message": "Failed to load stock data"
        }), 500

@app.route("/api/eda", methods=["GET"])
@safe_route()
def eda():
    from services.eda_service import get_eda_summary
    start = request.args.get("start")
    end = request.args.get("end")
    result = get_eda_summary(start, end)
    return jsonify({"success": True, "data": result})

@app.route("/api/train", methods=["POST"])
@safe_route()
def train():
    from services.model_service import train_all_models
    body = request.get_json(silent=True) or {}
    start = body.get("start")
    end = body.get("end")
    results = train_all_models(start, end)
    return jsonify({"success": True, "data": results})

@app.route("/api/predict", methods=["POST"])
@safe_route()
def predict():
    from services.model_service import predict_with_model
    body = request.get_json(silent=True) or {}
    model_name = body.get("model", "random_forest")
    start = body.get("start")
    end = body.get("end")
    result = predict_with_model(model_name, start, end)
    return jsonify({"success": True, "data": result})

@app.route("/api/models/compare", methods=["GET"])
@safe_route()
def compare_models():
    from services.db_service import get_latest_model_results
    results = get_latest_model_results()
    return jsonify({"success": True, "data": results})

@app.route("/api/realtime", methods=["GET"])
def realtime():
    """Get current TSLA price with fallback."""
    try:
        from services.data_service import get_realtime_price
        data = get_realtime_price()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        print(f"Realtime API failed: {str(e)}")
        traceback.print_exc()
        # Fallback data
        fallback = {
            "symbol": "TSLA",
            "price": 449.72,
            "change": 0.00,
            "changePercent": 0.00,
            "previousClose": 449.72,
            "status": "fallback"
        }
        return jsonify({"success": True, "data": fallback, "note": "Using fallback data"})

@app.route("/api/predictions/history", methods=["GET"])
@safe_route()
def prediction_history():
    from services.db_service import get_prediction_history
    limit = request.args.get("limit", 50, type=int)
    history = get_prediction_history(limit)
    return jsonify({"success": True, "data": history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
