class MultiAIChat {
    constructor() {
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.modelSelect = document.getElementById('model-select');
        this.refreshBtn = document.getElementById('refresh-models');
        this.statusElement = document.getElementById('status');
        this.modelInfoElement = document.getElementById('model-info');
        
        this.isProcessing = false;
        this.currentProvider = 'huggingface';
        
        this.initEventListeners();
        this.showWelcomeMessage();
        this.checkAPIStatus();
    }
    
    initEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.modelSelect.addEventListener('change', (e) => {
            this.currentProvider = e.target.value;
            this.updateModelInfo();
            this.addSystemMessage(`Switched to ${this.getProviderName()} model`);
        });
        
        this.refreshBtn.addEventListener('click', () => this.checkAPIStatus());
    }
    
    showWelcomeMessage() {
        const welcomeMsg = "Hello! I'm your multi-AI assistant. I can use Hugging Face models or Google Gemini. Choose your preferred provider above!";
        this.addMessage(welcomeMsg, 'ai', 'system');
    }
    
    async sendMessage() {
        if (this.isProcessing) return;
        
        const message = this.userInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.userInput.value = '';
        
        this.setProcessingState(true);
        this.setStatus('Processing...');
        
        try {
            const response = await this.getAIResponse(message, this.currentProvider);
            this.addMessage(response, 'ai', this.currentProvider);
            this.setStatus('Ready');
        } catch (error) {
            console.error('Error:', error);
            this.addMessage(`Sorry, I encountered an error: ${error.message}`, 'ai', 'error');
            this.setStatus('Error - check console');
        } finally {
            this.setProcessingState(false);
        }
    }
    
    async getAIResponse(message, provider) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                provider: provider
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.response;
        } else {
            throw new Error(data.error);
        }
    }
    
    addMessage(text, sender, provider = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        let badge = '';
        if (provider && provider !== 'system' && provider !== 'error') {
            const badgeClass = provider === 'google' ? 'google-badge' : 'huggingface-badge';
            badge = `<span class="provider-badge ${badgeClass}">${this.getProviderName(provider)}</span>`;
        }
        
        messageDiv.innerHTML = `
            <div class="message-text">${this.escapeHtml(text)} ${badge}</div>
            <div class="message-time">${timestamp}</div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    addSystemMessage(text) {
        this.addMessage(text, 'ai', 'system');
    }
    
    setProcessingState(processing) {
        this.isProcessing = processing;
        this.userInput.disabled = processing;
        this.sendBtn.disabled = processing;
        this.modelSelect.disabled = processing;
        this.sendBtn.textContent = processing ? 'Processing...' : 'Send';
        
        if (processing) {
            this.showTypingIndicator();
        } else {
            this.removeTypingIndicator();
        }
    }
    
    setStatus(status) {
        this.statusElement.textContent = status;
    }
    
    updateModelInfo() {
        this.modelInfoElement.textContent = `Using: ${this.getProviderName()}`;
    }
    
    getProviderName(provider = null) {
        const prov = provider || this.currentProvider;
        const names = {
            'huggingface': 'Hugging Face',
            'google': 'Google Gemini'
        };
        return names[prov] || prov;
    }
    
    async checkAPIStatus() {
        try {
            this.setStatus('Checking APIs...');
            const response = await fetch('/api/models');
            const data = await response.json();
            
            if (data.success) {
                this.setStatus('APIs connected');
                console.log('Available models:', data.models);
            } else {
                this.setStatus('API check failed');
            }
        } catch (error) {
            this.setStatus('API check error');
            console.error('API status check failed:', error);
        }
    }
    
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'message ai-message typing';
        indicator.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
        `;
        
        this.chatMessages.appendChild(indicator);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    new MultiAIChat();
});