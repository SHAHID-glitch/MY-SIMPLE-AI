#!/usr/bin/env python3
"""
Hugging Face Spaces deployment for Groq AI Assistant
Serves both Flask API and React frontend
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, 
    static_folder='static/dist',
    static_url_path='/static',
    template_folder='templates'
)
CORS(app)

# Configure Groq API
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Store conversation history
conversations = {}

@app.route('/')
def index():
    """Serve React frontend from dist folder"""
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat"""
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        if not GROQ_API_KEY:
            return jsonify({'error': 'Groq API key not configured'}), 500
        
        # Initialize conversation if needed
        if user_id not in conversations:
            conversations[user_id] = []
        
        # Add user message to history
        conversations[user_id].append({
            'role': 'user',
            'content': user_message
        })
        
        # Generate response using Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        ai_message = response.choices[0].message.content.strip()
        
        # Add AI message to history
        conversations[user_id].append({
            'role': 'assistant',
            'content': ai_message
        })
        
        return jsonify({
            'response': ai_message,
            'success': True
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status and configuration"""
    return jsonify({
        'status': 'running',
        'groq_configured': bool(GROQ_API_KEY),
        'model': 'llama-3.3-70b-versatile'
    })

# Serve other static files
@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return app.send_static_file(path)

@app.route('/assets/<path:path>')
def send_assets(path):
    """Serve Vite build assets from /assets"""
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

# Fallback to React for all unmatched routes (SPA routing)
@app.route('/<path:path>')
def catch_all(path):
    """Serve React app for SPA routing"""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False)
