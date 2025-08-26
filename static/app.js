// KumTanesi Chat Application JavaScript

class KumTanesiChat {
    constructor() {
        this.chatMessages = document.getElementById('chat-messages');
        this.chatForm = document.getElementById('chat-form');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        
        this.init();
    }
    
    init() {
        // Form submit handler
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Load existing conversation history
        this.loadConversationHistory();
        
        // Focus on input
        this.messageInput.focus();
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            this.showNotification('Lütfen bir mesaj yazın.', 'warning');
            return;
        }
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input and disable form
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.setFormState(false);
        
        // Show loading
        this.showTypingIndicator();
        this.loadingModal.show();
        
        try {
            // Send message to server
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Remove typing indicator
                this.removeTypingIndicator();
                
                // Add agent response
                this.addMessage('assistant', data.response);
                
                // Update character count
                document.getElementById('char-count').textContent = '0';
            } else {
                throw new Error(data.error || 'Bilinmeyen bir hata oluştu');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addMessage('assistant', 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.', true);
            this.showNotification('Mesaj gönderilemedi: ' + error.message, 'danger');
        } finally {
            // Hide loading and enable form
            this.loadingModal.hide();
            this.setFormState(true);
            this.messageInput.focus();
        }
    }
    
    addMessage(role, content, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString('tr-TR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const avatar = role === 'user' 
            ? '<i class="fas fa-user"></i>'
            : '<i class="fas fa-robot"></i>';
        
        const bubbleClass = isError ? 'message-bubble error-message' : 'message-bubble';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${avatar}
            </div>
            <div class="message-content">
                <div class="${bubbleClass}">
                    <p class="mb-0">${this.formatMessage(content)}</p>
                </div>
                <small class="message-time">${timeString}</small>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatMessage(text) {
        // Basic text formatting
        return text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message agent-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="d-flex align-items-center">
                        <span class="me-2">KumTanesi yazıyor</span>
                        <div class="spinner-border spinner-border-sm" role="status">
                            <span class="visually-hidden">Yazıyor...</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    setFormState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendBtn.disabled = !enabled;
        
        if (enabled) {
            this.sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
        } else {
            this.sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showNotification(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        // Add to page
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1200';
            document.body.appendChild(toastContainer);
        }
        
        toastContainer.appendChild(toast);
        
        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
    
    async loadConversationHistory() {
        try {
            const response = await fetch('/get_history');
            const data = await response.json();
            
            if (data.history && data.history.length > 0) {
                // Clear welcome message except the first one
                const messages = this.chatMessages.querySelectorAll('.message:not(:first-child)');
                messages.forEach(msg => msg.remove());
                
                // Add historical messages
                data.history.forEach(msg => {
                    if (msg.role !== 'system') {
                        this.addMessage(msg.role, msg.content);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading conversation history:', error);
        }
    }
}

// Global functions
async function clearHistory() {
    if (!confirm('Konuşma geçmişini temizlemek istediğinizden emin misiniz?')) {
        return;
    }
    
    try {
        const response = await fetch('/clear_history', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear chat messages except welcome message
            const chatMessages = document.getElementById('chat-messages');
            const messages = chatMessages.querySelectorAll('.message:not(:first-child)');
            messages.forEach(msg => msg.remove());
            
            // Show success notification
            window.chat.showNotification('Konuşma geçmişi temizlendi.', 'success');
        }
    } catch (error) {
        console.error('Error clearing history:', error);
        window.chat.showNotification('Geçmiş temizlenemedi.', 'danger');
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chat = new KumTanesiChat();
});
