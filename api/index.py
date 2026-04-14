"""
Vercel Serverless Entry Point for Flask API
"""
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import Flask app
from app import app

# Export for Vercel (this is what Vercel calls)
# Vercel expects either 'app' or 'handler'
handler = app
