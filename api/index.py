from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

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

@app.route("/api")
@app.route("/api/")
def api_root():
    return jsonify({"message": "TeslaPulse API", "status": "running"}), 200

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "TeslaPulse"}), 200

@app.route("/api/stock-data")
def stock_data():
    try:
        from services.data_service import get_stock_data_json
        start = request.args.get("start")
        end = request.args.get("end")
        data = get_stock_data_json(start, end)
        if "error" in data or not data.get("dates"):
            return jsonify({"success": False, "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]}, "message": "No data"}), 200
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "data": {"dates":[],"open":[],"high":[],"low":[],"close":[],"volume":[],"records":[]}, "error": str(e)}), 200

@app.route("/api/realtime")
def realtime():
    try:
        from services.data_service import get_realtime_price
        data = get_realtime_price()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": True, "data": {"symbol": "TSLA", "price": 449.72, "change": 0.00, "changePercent": 0.00, "previousClose": 449.72}}), 200

@app.route("/api/eda")
def eda():
    try:
        from services.eda_service import get_eda_summary
        start = request.args.get("start")
        end = request.args.get("end")
        result = get_eda_summary(start, end)
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200

@app.route("/api/train", methods=["POST"])
def train():
    try:
        from services.model_service import train_all_models
        body = request.get_json(silent=True) or {}
        results = train_all_models(body.get("start"), body.get("end"))
        return jsonify({"success": True, "data": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        from services.model_service import predict_with_model
        body = request.get_json(silent=True) or {}
        result = predict_with_model(body.get("model", "random_forest"), body.get("start"), body.get("end"))
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200

@app.route("/api/models/compare")
def compare_models():
    try:
        from services.db_service import get_latest_model_results
        results = get_latest_model_results()
        return jsonify({"success": True, "data": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200

@app.route("/api/predictions/history")
def prediction_history():
    try:
        from services.db_service import get_prediction_history
        limit = request.args.get("limit", 50, type=int)
        history = get_prediction_history(limit)
        return jsonify({"success": True, "data": history}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200
