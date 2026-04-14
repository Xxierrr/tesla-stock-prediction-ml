import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask import jsonify
import traceback

def handler(event, context):
    """Vercel serverless handler for /api/eda"""
    try:
        from services.eda_service import get_eda_summary
        
        start = event.get('query', {}).get('start')
        end = event.get('query', {}).get('end')
        
        result = get_eda_summary(start, end)
        
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
                "data": result
            }).get_data(as_text=True)
        }
    except Exception as e:
        print(f"EDA failed: {str(e)}")
        traceback.print_exc()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": jsonify({
                "success": False,
                "error": str(e)
            }).get_data(as_text=True)
        }
