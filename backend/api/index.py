"""
Vercel serverless function entry point for Flask app.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

# Vercel expects a handler
handler = app
