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

# Get base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize Flask app
app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))
CORS(app)

# Configure Gemini - Vercel provides environment variables
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    logger.info("Gemini API configured successfully")
else:
    logger.warning("Google API key not found in environment variables")

# In-memory conversation store
conversation_store = {}
HISTORY_LIMIT = 12

@app.route('/')
def home():
    return render_template('index.html')

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
            return jsonify({'success': False, 'error': 'Gemini API key not configured'}), 500

        # Session handling
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())

        history = conversation_store.get(session_id, [])
        history.append({'role': 'user', 'content': user_message})

        if len(history) > HISTORY_LIMIT * 2:
            history = history[-(HISTORY_LIMIT * 2):]

        # Get AI response
        ai_response = get_gemini_response(history)

        history.append({'role': 'assistant', 'content': ai_response})
        conversation_store[session_id] = history

        response_time = time.time() - start_time
        logger.info(f"Chat processed in {response_time:.2f}s")

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

# Export app for Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


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

# Export app for Vercel
# Vercel will automatically use this as the handler
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
