from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

app = Flask(__name__)
CORS(app)

@app.route("/api")
def home():
    return jsonify({"message": "API working"})

@app.route("/api/stock-data")
def stock():
    try:
        from services.data_service import get_stock_data_json
        start = request.args.get("start")
        end = request.args.get("end")
        data = get_stock_data_json(start, end)
        if "error" in data or not data.get("dates"):
            return jsonify({"success": False, "data": {"dates": [], "open": [], "high": [], "low": [], "close": [], "volume": [], "records": []}, "message": data.get("message", "No data available")})
        return jsonify({"success": True, "data": data, "count": len(data.get("dates", []))})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "data": {"dates": [], "open": [], "high": [], "low": [], "close": [], "volume": [], "records": []}})

@app.route("/api/realtime")
def realtime():
    try:
        from services.data_service import get_realtime_price
        data = get_realtime_price()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": True, "data": {"symbol": "TSLA", "price": 449.72, "change": 0.00, "changePercent": 0.00, "previousClose": 449.72, "status": "fallback"}})

@app.route("/api/eda")
def eda():
    try:
        from services.eda_service import get_eda_summary
        start = request.args.get("start")
        end = request.args.get("end")
        result = get_eda_summary(start, end)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "TeslaPulse API"})

# REQUIRED FOR VERCEL
def handler(request):
    return app(request)
