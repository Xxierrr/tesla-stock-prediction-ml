from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import pandas as pd
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Load CSV data once at startup
DATA_PATH = os.path.join(os.path.dirname(__file__), 'Tesla Dataset.csv')
try:
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')  # Ensure sorted by date
except Exception as e:
    print(f"Error loading CSV: {e}")
    df = None

@app.route("/api")
@app.route("/api/")
def api_root():
    return jsonify({"message": "TeslaPulse API", "status": "running", "version": "1.0"}), 200

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "TeslaPulse API"}), 200

@app.route("/api/stock-data")
def stock_data():
    if df is None:
        return jsonify({"success": False, "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]}, "message": "No data"}), 200
    
    try:
        start = request.args.get("start", "2020-01-01")
        end = request.args.get("end", "2025-01-01")
        
        # Filter data
        mask = (df['Date'] >= start) & (df['Date'] <= end)
        filtered = df[mask].copy()
        
        if filtered.empty:
            return jsonify({"success": False, "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]}, "message": "No data for range"}), 200
        
        # Format response
        data = {
            "dates": filtered['Date'].dt.strftime('%Y-%m-%d').tolist(),
            "open": filtered['Open'].tolist(),
            "high": filtered['High'].tolist(),
            "low": filtered['Low'].tolist(),
            "close": filtered['Close'].tolist(),
            "volume": filtered['Volume'].tolist(),
            "records": filtered.to_dict('records')
        }
        
        return jsonify({"success": True, "data": data, "count": len(data["dates"])}), 200
    except Exception as e:
        return jsonify({"success": False, "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]}, "error": str(e)}), 200

@app.route("/api/realtime")
def realtime():
    if df is None or df.empty:
        return jsonify({"success": True, "data": {"symbol": "TSLA", "price": 449.72, "change": 0.00, "changePercent": 0.00, "previousClose": 449.72}}), 200
    
    try:
        # Get last two rows for price and change
        last_close = float(df.iloc[-1]['Close'])
        prev_close = float(df.iloc[-2]['Close']) if len(df) > 1 else last_close
        change = last_close - prev_close
        change_pct = (change / prev_close * 100) if prev_close != 0 else 0.0
        
        data = {
            "symbol": "TSLA",
            "price": round(last_close, 2),
            "change": round(change, 2),
            "changePercent": round(change_pct, 2),
            "previousClose": round(prev_close, 2)
        }
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": True, "data": {"symbol": "TSLA", "price": 449.72, "change": 0.00, "changePercent": 0.00, "previousClose": 449.72}}), 200

@app.route("/api/eda")
def eda():
    if df is None or df.empty:
        return jsonify({"success": False, "error": "No data available"}), 200
    
    try:
        start = request.args.get("start", "2020-01-01")
        end = request.args.get("end", "2025-01-01")
        
        mask = (df['Date'] >= start) & (df['Date'] <= end)
        filtered = df[mask].copy()
        
        if filtered.empty:
            return jsonify({"success": False, "error": "No data for range"}), 200
        
        # Basic statistics
        stats = {
            "mean": float(filtered['Close'].mean()),
            "median": float(filtered['Close'].median()),
            "std": float(filtered['Close'].std()),
            "min": float(filtered['Close'].min()),
            "max": float(filtered['Close'].max()),
            "count": len(filtered)
        }
        
        result = {
            "statistics": stats,
            "dates": filtered['Date'].dt.strftime('%Y-%m-%d').tolist(),
            "close": filtered['Close'].tolist(),
            "volume": filtered['Volume'].tolist()
        }
        
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200

@app.route("/api/train", methods=["POST"])
def train():
    return jsonify({"success": True, "data": {"message": "Training not available in static mode"}}), 200

@app.route("/api/predict", methods=["POST"])
def predict():
    return jsonify({"success": True, "data": {"message": "Predictions not available in static mode"}}), 200

@app.route("/api/models/compare")
def compare_models():
    return jsonify({"success": True, "data": []}), 200

@app.route("/api/predictions/history")
def prediction_history():
    return jsonify({"success": True, "data": []}), 200

# Export app for Vercel
# Vercel will automatically detect this as a WSGI app
if __name__ != "__main__":
    # Production mode (Vercel)
    application = app
else:
    # Development mode
    app.run(debug=True)
