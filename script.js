class GeminiAIChat {
    constructor() {
        this.messageCount = 0;
        this.isProcessing = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.updateCurrentTime();
        this.checkAPIStatus();
        
        // Update time every minute
        setInterval(() => this.updateCurrentTime(), 60000);
    }
    
    initializeElements() {
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.apiStatus = document.getElementById('api-status');
        this.messageCountElement = document.getElementById('message-count');
        this.currentTimeElement = document.getElementById('current-time');
    }
    
    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.userInput.addEventListener('input', () => {
            this.userInput.style.height = 'auto';
            this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
        });
        
        // Focus input on load
        setTimeout(() => this.userInput.focus(), 500);
    }
    
    updateCurrentTime() {
        const now = new Date();
        this.currentTimeElement.textContent = now.toLocaleTimeString([], { 
            hour: '2-digit', minute: '2-digit' 
        });
    }
    
    async checkAPIStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.success && data.gemini_configured) {
                this.apiStatus.textContent = '🟢 Gemini API Connected';
                this.apiStatus.classList.add('connected');
            } else {
                this.apiStatus.textContent = '🔴 Gemini API Not Configured';
            }
        } catch (error) {
            this.apiStatus.textContent = '🔴 API Check Failed';
            console.error('API status check failed:', error);
        }
    }
    
    async sendMessage() {
        if (this.isProcessing) return;
        
        const message = this.userInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.userInput.style.height = 'auto';
        
        this.setProcessingState(true);
        
        try {
            const response = await this.getAIResponse(message);
            this.addMessage(response, 'ai');
            this.incrementMessageCount();
        } catch (error) {
            console.error('Error:', error);
            this.addMessage(
                "Sorry, I encountered an error. Please check your API key and try again.", 
                'ai'
            );
        } finally {
            this.setProcessingState(false);
        }
    }
    
    async getAIResponse(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                timestamp: new Date().toISOString()
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            return data.response;
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { 
            hour: '2-digit', minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="message-bubble">${this.escapeHtml(text)}</div>
            <div class="message-info">
                <span class="message-sender">${sender === 'user' ? 'You' : 'Gemini AI'}</span>
                <span class="message-time">${timestamp}</span>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Add typing indicator for AI messages
        if (sender === 'user') {
            this.showTypingIndicator();
        }
    }
    
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message ai-message';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <span style="font-size: 0.9rem; color: #666;">Gemini is thinking...</span>
            </div>
        `;
        
        this.chatMessages.appendChild(indicator);
        this.scrollToBottom();
    }
    
    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    setProcessingState(processing) {
        this.isProcessing = processing;
        this.userInput.disabled = processing;
        this.sendBtn.disabled = processing;
        
        const buttonText = this.sendBtn.querySelector('.button-text');
        const buttonLoader = this.sendBtn.querySelector('.button-loader');
        
        if (processing) {
            buttonText.style.display = 'none';
            buttonLoader.style.display = 'inline';
            this.sendBtn.style.minWidth = '100px';
        } else {
            buttonText.style.display = 'inline';
            buttonLoader.style.display = 'none';
            this.removeTypingIndicator();
        }
    }
    
    incrementMessageCount() {
        this.messageCount++;
        this.messageCountElement.textContent = `Messages: ${this.messageCount}`;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GeminiAIChat();
});