import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask import jsonify
from flask_cors import CORS
import traceback

def handler(event, context):
    """Vercel serverless handler for /api/realtime"""
    try:
        from services.data_service import get_realtime_price
        
        data = get_realtime_price()
        
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
                "data": data
            }).get_data(as_text=True)
        }
    except Exception as e:
        print(f"Realtime failed: {str(e)}")
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
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": jsonify({
                "success": True,
                "data": fallback
            }).get_data(as_text=True)
        }
