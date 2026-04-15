"""
Vercel Serverless Entry Point
Routes all /api/* requests to Flask backend app.
"""
import sys
import os

# Add backend directory to Python path so imports work
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend')
sys.path.insert(0, backend_dir)

# Import Flask app - Vercel auto-detects this as a WSGI app
from app import app

# Vercel needs the app variable exported at module level
# It will automatically use it as the WSGI handler
