from flask import jsonify

def handler(event, context):
    """Vercel serverless handler for /api/health"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": jsonify({
            "status": "ok",
            "service": "TeslaPulse API"
        }).get_data(as_text=True)
    }
