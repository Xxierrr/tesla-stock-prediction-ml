import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask import Flask, jsonify, request
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

def handler(event, context):
    """Vercel serverless handler for /api/stock-data"""
    try:
        from services.data_service import get_stock_data_json
        
        # Get query parameters
        start = event.get('query', {}).get('start')
        end = event.get('query', {}).get('end')
        
        data = get_stock_data_json(start, end)
        
        if "error" in data or not data.get("dates"):
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": jsonify({
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
                }).get_data(as_text=True)
            }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": jsonify({
                "success": True,
                "data": data,
                "count": len(data.get("dates", []))
            }).get_data(as_text=True)
        }
    except Exception as e:
        print(f"stock_data failed: {str(e)}")
        traceback.print_exc()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": jsonify({
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
                "error": str(e)
            }).get_data(as_text=True)
        }
