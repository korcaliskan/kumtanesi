import os
import logging
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
from agent import KumTanesiAgent

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "kumtanesi-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize the AI agent
agent = KumTanesiAgent()

@app.route('/')
def index():
    """Ana sayfa - KumTanesi chat arayüzü"""
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Kullanıcı mesajını işle ve agent yanıtı döndür"""
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Lütfen bir mesaj yazın.'
            }), 400
        
        # Session'da konuşma geçmişini başlat
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        # Kullanıcı mesajını geçmişe ekle
        session['conversation_history'].append({
            'role': 'user',
            'content': user_message
        })
        
        # Agent'tan yanıt al
        agent_response = agent.get_response(user_message, session['conversation_history'])
        
        # Agent yanıtını geçmişe ekle
        session['conversation_history'].append({
            'role': 'assistant',
            'content': agent_response
        })
        
        # Son 20 mesajı tut (bellek yönetimi)
        if len(session['conversation_history']) > 20:
            session['conversation_history'] = session['conversation_history'][-20:]
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'response': agent_response
        })
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.'
        }), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Konuşma geçmişini temizle"""
    session['conversation_history'] = []
    session.modified = True
    return jsonify({'success': True, 'message': 'Konuşma geçmişi temizlendi.'})

@app.route('/get_history')
def get_history():
    """Konuşma geçmişini döndür"""
    history = session.get('conversation_history', [])
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
