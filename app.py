import os
import logging
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db, User, Member, Due, Expense, Investment
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "aidat-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    "pool_recycle": 300,
    "connect_args": {
        "sslmode": "require"
    }
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    
    # İlk admin kullanıcısını oluştur (eğer yoksa)
    if not User.query.filter_by(username='admin').first():
        admin_user = User()
        admin_user.username = 'admin'
        admin_user.email = 'admin@example.com'
        admin_user.is_admin = True
        admin_user.set_password('admin123')  # Varsayılan şifre
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Admin kullanıcısı oluşturuldu: admin / admin123")

@app.route('/')
def index():
    """Ana sayfa - giriş kontrolü"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Kullanıcı adı ve şifre gerekli.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Çıkış yap"""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Ana dashboard"""
    # Özet bilgiler
    total_members = Member.query.filter_by(is_active=True).count()
    total_dues_this_month = db.session.query(db.func.sum(Due.amount)).filter(
        Due.due_date >= datetime.now().replace(day=1).date(),
        Due.is_paid == True
    ).scalar() or 0
    
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    total_investments = db.session.query(db.func.sum(Investment.amount)).scalar() or 0
    
    # Son işlemler
    recent_dues = Due.query.filter_by(is_paid=True).order_by(Due.payment_date.desc()).limit(5).all()
    recent_expenses = Expense.query.order_by(Expense.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_members=total_members,
                         total_dues_this_month=total_dues_this_month,
                         total_expenses=total_expenses,
                         total_investments=total_investments,
                         recent_dues=recent_dues,
                         recent_expenses=recent_expenses)

@app.route('/members')
@login_required
def members():
    """Üyeler sayfası"""
    members_list = Member.query.filter_by(is_active=True).order_by(Member.name).all()
    return render_template('members.html', members=members_list)

@app.route('/members/add', methods=['GET', 'POST'])
@login_required
def add_member():
    """Yeni üye ekleme"""
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        join_date_str = request.form.get('join_date')
        if not join_date_str:
            flash('Katılım tarihi gerekli.', 'danger')
            return render_template('add_member.html')
        join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
        
        if not name or not surname or not join_date:
            flash('Ad, soyad ve katılım tarihi gerekli.', 'danger')
            return render_template('add_member.html')
        
        new_member = Member()
        new_member.name = name
        new_member.surname = surname
        new_member.phone = phone
        new_member.email = email
        new_member.address = address
        new_member.join_date = join_date
        
        db.session.add(new_member)
        db.session.commit()
        
        flash(f'{name} {surname} başarıyla eklendi.', 'success')
        return redirect(url_for('members'))
    
    return render_template('add_member.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)