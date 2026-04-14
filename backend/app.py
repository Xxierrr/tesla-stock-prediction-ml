"""
TeslaPulse Flask API - Vercel Serverless Compatible
"""
import sys
import os
import traceback

# Ensure backend modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Root API endpoint
@app.route("/api", methods=["GET", "OPTIONS"])
def api_root():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({
        "message": "TeslaPulse API is running",
        "version": "1.0",
        "endpoints": [
            "/api/health",
            "/api/stock-data",
            "/api/realtime",
            "/api/eda"
        ]
    }), 200

# Health check endpoint
@app.route("/api/health", methods=["GET", "OPTIONS"])
def health():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    return jsonify({
        "status": "ok",
        "service": "TeslaPulse API",
        "message": "Backend is healthy"
    }), 200

# Stock data endpoint
@app.route("/api/stock-data", methods=["GET", "OPTIONS"])
def stock_data():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.data_service import get_stock_data_json
        
        start = request.args.get("start")
        end = request.args.get("end")
        
        print(f"Fetching stock data: start={start}, end={end}")
        
        data = get_stock_data_json(start, end)
        
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
                "message": data.get("message", "No data available")
            }), 200
        
        return jsonify({
            "success": True,
            "data": data,
            "count": len(data.get("dates", []))
        }), 200
        
    except Exception as e:
        print(f"Error in stock_data: {str(e)}")
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
            "error": str(e),
            "message": "Failed to fetch stock data"
        }), 200

# Real-time price endpoint
@app.route("/api/realtime", methods=["GET", "OPTIONS"])
def realtime():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.data_service import get_realtime_price
        
        data = get_realtime_price()
        
        return jsonify({
            "success": True,
            "data": data
        }), 200
        
    except Exception as e:
        print(f"Error in realtime: {str(e)}")
        traceback.print_exc()
        
        # Return fallback data
        fallback = {
            "symbol": "TSLA",
            "price": 449.72,
            "change": 0.00,
            "changePercent": 0.00,
            "previousClose": 449.72,
            "status": "fallback"
        }
        
        return jsonify({
            "success": True,
            "data": fallback,
            "note": "Using fallback data due to API error"
        }), 200

# EDA endpoint
@app.route("/api/eda", methods=["GET", "OPTIONS"])
def eda():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.eda_service import get_eda_summary
        
        start = request.args.get("start")
        end = request.args.get("end")
        
        result = get_eda_summary(start, end)
        
        return jsonify({
            "success": True,
            "data": result
        }), 200
        
    except Exception as e:
        print(f"Error in eda: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to generate EDA"
        }), 200

# Train models endpoint
@app.route("/api/train", methods=["POST", "OPTIONS"])
def train():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.model_service import train_all_models
        
        body = request.get_json(silent=True) or {}
        start = body.get("start")
        end = body.get("end")
        
        results = train_all_models(start, end)
        
        return jsonify({
            "success": True,
            "data": results
        }), 200
        
    except Exception as e:
        print(f"Error in train: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to train models"
        }), 200

# Predict endpoint
@app.route("/api/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.model_service import predict_with_model
        
        body = request.get_json(silent=True) or {}
        model_name = body.get("model", "random_forest")
        start = body.get("start")
        end = body.get("end")
        
        result = predict_with_model(model_name, start, end)
        
        return jsonify({
            "success": True,
            "data": result
        }), 200
        
    except Exception as e:
        print(f"Error in predict: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to generate predictions"
        }), 200

# Model comparison endpoint
@app.route("/api/models/compare", methods=["GET", "OPTIONS"])
def compare_models():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.db_service import get_latest_model_results
        
        results = get_latest_model_results()
        
        return jsonify({
            "success": True,
            "data": results
        }), 200
        
    except Exception as e:
        print(f"Error in compare_models: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to compare models"
        }), 200

# Prediction history endpoint
@app.route("/api/predictions/history", methods=["GET", "OPTIONS"])
def prediction_history():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        from services.db_service import get_prediction_history
        
        limit = request.args.get("limit", 50, type=int)
        history = get_prediction_history(limit)
        
        return jsonify({
            "success": True,
            "data": history
        }), 200
        
    except Exception as e:
        print(f"Error in prediction_history: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed tYou are an expert full-stack engineer specializing in deploying Flask (Python) + React (Vite) apps on Vercel.

I am getting a Vercel error:

404: NOT_FOUND

This happens when I open:

* /
* /api
* /api/stock-data

---

### MY PROJECT STRUCTURE:

root/
api/
index.py
backend/
app.py
services/
**init**.py
frontend/
dist/
src/
vercel.json

---

### PROBLEM:

Vercel is not serving:

* frontend (React app)
* backend (Flask API)

So all routes return 404.

---

### YOUR TASK:

Fix EVERYTHING so that:

1. `/api/*` routes go to Flask backend
2. `/` serves React app from `/frontend/dist`
3. No 404 errors occur
4. Flask is properly exposed as WSGI for Vercel
5. Python imports work correctly (`backend.app`)
6. Routing works in Vercel (modern config only)
7. No deprecated config like `"builds"` or `"functions"`

---

### REQUIREMENTS:

* Use ONLY modern Vercel routing (`routes`)
* Do NOT use `"builds"` or `"functions"`
* Ensure `/api/index.py` works as entry point
* Ensure frontend fallback works (`index.html`)
* Assume Vite build already exists in `/frontend/dist`

---

### OUTPUT FORMAT:

Return ONLY final working code for:

1. vercel.json
2. api/index.py
3. required changes in backend/app.py

No explanation. No extra text.

---

### EXPECTED RESULT:

After deployment, these must work:

* https://my-app.vercel.app/
* https://my-app.vercel.app/api
* https://my-app.vercel.app/api/stock-data
* https://my-app.vercel.app/api/realtime

Frontend should load and API should return data.
o fetch prediction history"
        }), 200

# DO NOT include app.run() for Vercel serverless
# Vercel will handle running the app
