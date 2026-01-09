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

# Embedded HTML template (since templates folder may not deploy to Vercel)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini AI Assistant - 3D Experience</title>
    <link rel="stylesheet" href="/static/gemini-style.css">
</head>
<body>
    <div class="background-3d">
        <div class="sphere sphere-1"></div>
        <div class="sphere sphere-2"></div>
        <div class="sphere sphere-3"></div>
        <div class="particles" id="particles"></div>
    </div>
    <div class="container">
        <header class="header-3d">
            <div class="logo-container">
                <div class="logo-3d">
                    <div class="logo-face front">🧠</div>
                    <div class="logo-face back">✨</div>
                </div>
            </div>
            <h1 class="title-3d">
                <span class="title-letter" style="--i:0">G</span>
                <span class="title-letter" style="--i:1">e</span>
                <span class="title-letter" style="--i:2">m</span>
                <span class="title-letter" style="--i:3">i</span>
                <span class="title-letter" style="--i:4">n</span>
                <span class="title-letter" style="--i:5">i</span>
                <span class="title-letter" style="--i:6"> </span>
                <span class="title-letter" style="--i:7">A</span>
                <span class="title-letter" style="--i:8">I</span>
            </h1>
            <p class="subtitle-3d">Powered by Google Gemini 2.0 Flash</p>
            <div class="api-status-3d" id="api-status">
                <span class="status-dot"></span>
                <span class="status-text">Checking API...</span>
            </div>
        </header>
        <div class="chat-container-3d">
            <div id="chat-messages" class="chat-messages-3d">
                <div class="message ai-message-3d">
                    <div class="message-avatar">
                        <div class="avatar-3d ai-avatar">🤖</div>
                    </div>
                    <div class="message-content-3d">
                        <div class="message-text">Hello! I'm your AI assistant powered by Google Gemini. How can I help you today? 🚀</div>
                        <div class="message-time" id="current-time"></div>
                    </div>
                </div>
            </div>
            <div class="input-area-3d">
                <div class="input-container-3d">
                    <div class="input-glow"></div>
                    <textarea id="user-input" placeholder="Ask me anything... ✨" autocomplete="off" rows="1"></textarea>
                    <button id="send-btn" class="send-button-3d" aria-label="Send message">
                        <span class="button-text">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                            </svg>
                        </span>
                        <span class="button-loader" style="display: none;">
                            <div class="spinner-3d"></div>
                        </span>
                    </button>
                </div>
                <div class="input-hint-3d">
                    <span>💡 Press <kbd>Enter</kbd> to send</span>
                    <span>•</span>
                    <span><kbd>Shift</kbd> + <kbd>Enter</kbd> for new line</span>
                </div>
            </div>
        </div>
        <footer class="footer-3d">
            <div class="footer-content-3d">
                <div class="footer-item">
                    <span class="footer-icon">🤖</span>
                    <span>Gemini 2.0 Flash</span>
                </div>
                <div class="footer-item">
                    <span class="footer-icon">💬</span>
                    <span id="message-count">0 messages</span>
                </div>
                <div class="footer-item">
                    <span class="footer-icon">⚡</span>
                    <span>Ultra Fast</span>
                </div>
            </div>
        </footer>
    </div>
    <script src="/static/gemini-app.js"></script>
    <script>
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 20 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particlesContainer.appendChild(particle);
        }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return HTML_TEMPLATE, 200, {'Content-Type': 'text/html'}

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
