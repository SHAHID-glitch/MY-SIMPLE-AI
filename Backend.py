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

app = Flask(__name__)
CORS(app)

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

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

        # Session handling (simple cookie-based)
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())

        history = conversation_store.get(session_id, [])

        # Append user turn
        history.append({'role': 'user', 'content': user_message})
        # Trim history to limit (keep most recent turns)
        if len(history) > HISTORY_LIMIT * 2:
            history = history[-(HISTORY_LIMIT * 2):]

        # Get AI response using history
        ai_response = get_gemini_response(history)

        # Append assistant reply to history and save
        history.append({'role': 'assistant', 'content': ai_response})
        conversation_store[session_id] = history

        response_time = time.time() - start_time
        logger.info(f"Chat request processed in {response_time:.2f}s (session={session_id})")

        resp = make_response(jsonify({'success': True, 'response': ai_response, 'processing_time': f"{response_time:.2f}s"}))
        # set session cookie (httpOnly)
        resp.set_cookie('session_id', session_id, httponly=True, samesite='Lax')
        return resp

    except Exception as e:
        logger.exception("Error in chat endpoint")
        return jsonify({'success': False, 'error': str(e)}), 500

def get_gemini_response(history):
    """Get response from Google Gemini using recent conversation history.

    history: list of {'role': 'user'|'assistant', 'content': str}
    Returns assistant reply (string).
    """
    try:
        if not GOOGLE_API_KEY:
            return "⚠️ API key not configured. Please check your .env file."

        system_instruction = (
            "You are a helpful, friendly, and knowledgeable AI assistant."
            " Answer the user's questions concisely and clearly. Provide examples when helpful."
        )

        # Build a single prompt from system instruction + recent history
        convo_text = system_instruction + "\n\nConversation:\n"
        for turn in history:
            role = turn.get('role')
            content = turn.get('content', '')
            if role == 'user':
                convo_text += f"User: {content}\n"
            else:
                convo_text += f"Assistant: {content}\n"

        convo_text += "Assistant:"

        # Use the latest Gemini 2.5 Flash model (WITH models/ prefix - this is correct!)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
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
        return f"⚠️ Gemini API error: {str(e)}"


@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation history for this session."""
    try:
        session_id = request.cookies.get('session_id')
        if session_id and session_id in conversation_store:
            del conversation_store[session_id]

        resp = make_response(jsonify({'success': True, 'message': 'Conversation reset'}))
        resp.set_cookie('session_id', '', expires=0)
        return resp
    except Exception as e:
        logger.exception('Error resetting conversation')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check API status and configuration"""
    try:
        status_info = {
            'success': True,
            'gemini_configured': bool(GOOGLE_API_KEY),
            'service': 'Google Gemini 2.5 Flash',
            'timestamp': time.time()
        }
        
        # Test Gemini connection if API key is configured
        if GOOGLE_API_KEY:
            try:
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                test_response = model.generate_content("Hello")
                status_info['gemini_working'] = True
                status_info['test_response'] = "Connection successful"
            except Exception as e:
                status_info['gemini_working'] = False
                status_info['gemini_error'] = str(e)
        
        return jsonify(status_info)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/models', methods=['GET'])
def list_models():
    """List available Gemini models"""
    try:
        if not GOOGLE_API_KEY:
            return jsonify({
                'success': False,
                'error': 'API key not configured'
            })
        
        models = [
            {
                'name': 'gemini-pro',
                'description': 'Google Gemini Pro - Best for text generation',
                'max_tokens': 32768
            }
        ]
        
        return jsonify({
            'success': True,
            'models': models
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, port=5000, host='0.0.0.0')