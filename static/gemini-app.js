class GeminiChat {
    constructor() {
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.apiStatus = document.getElementById('api-status');
        this.messageCount = document.getElementById('message-count');
        
        this.isProcessing = false;
        this.messageCounter = 0;
        
        this.initEventListeners();
        this.checkAPIStatus();
        this.updateTime();
        this.autoResizeTextarea();
    }
    
    initEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.userInput.addEventListener('input', () => this.autoResizeTextarea());
    }
    
    autoResizeTextarea() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
    }
    
    async checkAPIStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            const statusText = this.apiStatus.querySelector('.status-text');
            if (data.success && data.groq_configured) {
                this.apiStatus.classList.add('connected');
                if (statusText) statusText.textContent = 'API Connected';
            } else {
                this.apiStatus.classList.remove('connected');
                if (statusText) statusText.textContent = 'API Not Configured';
            }
        } catch (error) {
            const statusText = this.apiStatus.querySelector('.status-text');
            if (statusText) statusText.textContent = 'API Status Unknown';
        }
    }
    
    async sendMessage() {
        if (this.isProcessing) return;
        
        const message = this.userInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.autoResizeTextarea();
        this.messageCounter++;
        this.updateMessageCount();
        
        this.setProcessingState(true);
        
        try {
            const response = await this.getAIResponse(message);
            this.addMessage(response, 'ai');
            this.messageCounter++;
            this.updateMessageCount();
        } catch (error) {
            console.error('Error:', error);
            this.addMessage(`❌ Error: ${error.message}. Please try again.`, 'ai', true);
        } finally {
            this.setProcessingState(false);
            this.userInput.focus();
        }
    }
    
    async getAIResponse(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.response;
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    }
    
    addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message-3d ${isError ? 'error-message' : ''}`;
        
        // Create avatar
        const avatarContainer = document.createElement('div');
        avatarContainer.className = 'message-avatar';
        const avatar = document.createElement('div');
        avatar.className = `avatar-3d ${sender}-avatar`;
        avatar.textContent = sender === 'user' ? '👤' : '🤖';
        avatarContainer.appendChild(avatar);
        
        // Create message content
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content-3d';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        
        // Format text with line breaks
        messageText.innerHTML = text.replace(/\n/g, '<br>');
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);
        
        messageDiv.appendChild(avatarContainer);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Smooth scroll to bottom
        this.chatMessages.scrollTo({
            top: this.chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    setProcessingState(isProcessing) {
        this.isProcessing = isProcessing;
        this.sendBtn.disabled = isProcessing;
        this.userInput.disabled = isProcessing;
        
        const buttonText = this.sendBtn.querySelector('.button-text');
        const buttonLoader = this.sendBtn.querySelector('.button-loader');
        
        if (isProcessing) {
            buttonText.style.display = 'none';
            buttonLoader.style.display = 'inline';
        } else {
            buttonText.style.display = 'inline';
            buttonLoader.style.display = 'none';
        }
    }
    
    updateMessageCount() {
        this.messageCount.textContent = `${this.messageCounter} messages`;
    }
    
    updateTime() {
        const currentTime = document.getElementById('current-time');
        if (currentTime) {
            currentTime.textContent = new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }
    }
}

// Initialize the chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    new GeminiChat();
});
