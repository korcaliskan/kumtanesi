/**
 * KumTanesi Chat Interface
 * Handles real-time chat interactions with the AI agent
 */

class KumTanesiChat {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendBtn = document.getElementById('sendBtn');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.clearHistoryBtn = document.getElementById('clearHistoryBtn');
        
        this.initializeEventListeners();
        this.focusInput();
    }
    
    initializeEventListeners() {
        // Chat form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Clear history button
        this.clearHistoryBtn.addEventListener('click', () => {
            this.clearChatHistory();
        });
        
        // Auto-resize input (optional enhancement)
        this.messageInput.addEventListener('input', () => {
            this.adjustInputHeight();
        });
        
        // Enter key handling
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            this.showError('Lütfen bir mesaj yazın.');
            return;
        }
        
        if (message.length > 1000) {
            this.showError('Mesaj çok uzun. Lütfen 1000 karakterden az yazın.');
            return;
        }
        
        // Clear any existing errors
        this.clearErrors();
        
        // Remove welcome message if exists
        this.removeWelcomeMessage();
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input and disable form
        this.messageInput.value = '';
        this.setFormState(false);
        this.showLoading(true);
        
        try {
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                // Add assistant response
                this.addMessage('assistant', data.response);
            } else {
                // Show error message
                this.showError(data.error || 'Bir hata oluştu. Lütfen tekrar deneyin.');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.showError('Bağlantı hatası. İnternet bağlantınızı kontrol edin.');
        } finally {
            // Re-enable form and hide loading
            this.setFormState(true);
            this.showLoading(false);
            this.focusInput();
        }
    }
    
    addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role} p-3 mb-3`;
        
        const now = new Date();
        const timeStr = now.toLocaleTimeString('tr-TR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const icon = role === 'user' # thoughts
I need to create a Flask web application called "KumTanesi" with AI agent support and a conversational interface. The application should have Turkish language support, use Bootstrap for styling, integrate with OpenAI API for intelligent responses, and provide a chat interface for user-agent interactions. I'll create a minimal directory structure with Flask backend, HTML templates, and necessary static files.

# useful_guidelines_from_blueprints
From the flask_website blueprint:
- Listen on port 5000 when starting a server
- Set the secret_key exactly like this: `app.secret_key = os.environ.get("SESSION_SECRET")`
- Use Bootstrap for UI components
- Create a beautiful, functional, and production-ready design
- Debug mode for Flask is enabled

From the python_openai blueprint:
- The newest OpenAI model is "gpt-5" which was released August 7, 2025
- Use the OpenAI client with proper API key from environment variables

From the styling_replit blueprint:
- Always use Bootstrap CSS for styling
- Use the Replit-themed bootstrap CSS file: `https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css`
- Use default bootstrap classes and minimal custom styling

# directory_structure
```json
[
    {"path": "main.py", "status": "new"},
    {"path": "app.py", "status": "new"},
    {"path": "models.py", "status": "new"},
    {"path": "agent.py", "status": "new"},
    {"path": "templates/index.html", "status": "new"},
    {"path": "templates/base.html", "status": "new"},
    {"path": "static/style.css", "status": "new"},
    {"path": "static/app.js", "status": "new"}
]
