from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import time
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') or os.environ.get('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    logger.info("Gemini API configured successfully")
else:
    logger.warning("Google API key not found in environment variables")

# In-memory conversation store (simple, non-persistent)
conversation_store = {}
# Keep last N turns (user+assistant pairs)
HISTORY_LIMIT = 12

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Receive a user message, maintain session history, and return Gemini response."""
    start_time = time.time()

    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400

        if not GOOGLE_API_KEY:
            return jsonify({'success': False, 'error': 'Gemini API key not configured. Please check your .env file'}), 500

        # Get session ID (or create a new one)
        session_id = data.get('session_id', str(uuid.uuid4()))

        # Initialize conversation for new session
        if session_id not in conversation_store:
            conversation_store[session_id] = []

        conversation = conversation_store[session_id]

        # Add user message to conversation
        conversation.append({
            "role": "user",
            "parts": [user_message]
        })

        # Trim history if too long (keep only last HISTORY_LIMIT messages)
        if len(conversation) > HISTORY_LIMIT:
            conversation = conversation[-HISTORY_LIMIT:]
            conversation_store[session_id] = conversation

        # Create model
        model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

        # Generate response
        response = model.generate_content(
            conversation,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
            )
        )

        ai_response = response.text

        # Add AI response to conversation
        conversation.append({
            "role": "model",
            "parts": [ai_response]
        })

        elapsed = time.time() - start_time
        logger.info(f"Chat response generated in {elapsed:.2f}s")

        return jsonify({
            'success': True,
            'response': ai_response,
            'session_id': session_id,
            'message_count': len(conversation)
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status"""
    is_configured = GOOGLE_API_KEY is not None and GOOGLE_API_KEY != ''
    
    return jsonify({
        'status': 'ok',
        'api_configured': is_configured,
        'active_sessions': len(conversation_store)
    })

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history for a session"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id and session_id in conversation_store:
            del conversation_store[session_id]
            return jsonify({'success': True, 'message': 'Conversation cleared'})
        
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
