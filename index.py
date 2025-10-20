from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
import google.generativeai as genai
import os
import logging
import time
import uuid
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get base directory for templates/static
BASE_DIR = Path(__file__).resolve().parent

# Initialize Flask app
app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))
CORS(app)

# Configure Gemini - Vercel provides environment variables
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("Gemini API configured successfully")
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
else:
    logger.warning("GOOGLE_API_KEY not found in environment")

# In-memory conversation store
conversation_store = {}
HISTORY_LIMIT = 12

@app.route('/')
def home():
    try:
        # Read the template file directly and replace Flask template tags
        template_path = BASE_DIR / 'templates' / 'index.html'
        if not template_path.exists():
            return jsonify({'error': 'Template not found', 'path': str(template_path)}), 500
        
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace Flask template tags with static paths
        html_content = html_content.replace(
            "{{ url_for('static', filename='gemini-style.css') }}", 
            "/static/gemini-style.css"
        )
        html_content = html_content.replace(
            "{{ url_for('static', filename='gemini-app.js') }}", 
            "/static/gemini-app.js"
        )
        
        return html_content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        return jsonify({'error': 'Template error', 'details': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    start_time = time.time()

    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400

        if not GOOGLE_API_KEY:
            return jsonify({'success': False, 'error': 'API key not configured'}), 500

        # Session handling
        session_id = request.cookies.get('session_id') or str(uuid.uuid4())

        history = conversation_store.get(session_id, [])
        history.append({'role': 'user', 'content': user_message})

        if len(history) > HISTORY_LIMIT * 2:
            history = history[-(HISTORY_LIMIT * 2):]

        # Get AI response
        ai_response = get_gemini_response(history)

        history.append({'role': 'assistant', 'content': ai_response})
        conversation_store[session_id] = history

        response_time = time.time() - start_time

        resp = make_response(jsonify({
            'success': True, 
            'response': ai_response, 
            'processing_time': f"{response_time:.2f}s"
        }))
        resp.set_cookie('session_id', session_id, httponly=True, samesite='Lax')
        return resp

    except Exception as e:
        logger.exception("Error in chat endpoint")
        return jsonify({'success': False, 'error': str(e)}), 500

def get_gemini_response(history):
    """Get response from Gemini"""
    try:
        if not GOOGLE_API_KEY:
            return "⚠️ API key not configured"

        system_instruction = "You are a helpful AI assistant. Answer questions concisely and clearly."
        
        convo_text = system_instruction + "\n\nConversation:\n"
        for turn in history:
            role = turn.get('role')
            content = turn.get('content', '')
            if role == 'user':
                convo_text += f"User: {content}\n"
            else:
                convo_text += f"Assistant: {content}\n"
        
        convo_text += "Assistant:"

        model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
        
        response = model.generate_content(
            convo_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95,
                top_k=64,
                max_output_tokens=2048,
            )
        )

        return response.text.strip()

    except Exception as e:
        logger.exception("Gemini API error")
        return f"⚠️ Error: {str(e)}"

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check API status"""
    try:
        return jsonify({
            'success': True,
            'gemini_configured': bool(GOOGLE_API_KEY),
            'service': 'Google Gemini 2.0 Flash',
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation"""
    try:
        session_id = request.cookies.get('session_id')
        if session_id and session_id in conversation_store:
            del conversation_store[session_id]

        resp = make_response(jsonify({'success': True, 'message': 'Conversation reset'}))
        resp.set_cookie('session_id', '', expires=0)
        return resp
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel will use 'app' as the WSGI application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
