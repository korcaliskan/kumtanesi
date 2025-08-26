from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Kullanıcı modeli - sistem girişi için"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Şifreyi hash'leyerek kaydet"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Şifreyi kontrol et"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Member(db.Model):
    """Üye modeli - aidat ödeyen kişiler"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    join_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    dues = db.relationship('Due', backref='member', lazy=True, cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.name} {self.surname}"
    
    @property
    def total_paid(self):
        """Toplam ödenen aidat miktarı"""
        return sum(float(due.amount) for due in self.dues if due.is_paid)
    
    def __repr__(self):
        return f'<Member {self.full_name}>'

class Due(db.Model):
    """Aidat modeli - aylık ödemeler"""
    __tablename__ = 'dues'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)  # Ödeme tarihi
    payment_date = db.Column(db.Date)  # Gerçek ödeme tarihi
    is_paid = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50))  # Nakit, Banka, vs.
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def is_overdue(self):
        """Ödeme gecikmiş mi?"""
        if self.is_paid:
            return False
        return datetime.now().date() > self.due_date
    
    def __repr__(self):
        return f'<Due Member {self.member_id} - {self.amount}TL>'

class Expense(db.Model):
    """Gider modeli - aidatlarla yapılan harcamalar"""
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100))  # Kategori (Bakım, Temizlik, vs.)
    receipt_number = db.Column(db.String(50))
    vendor = db.Column(db.String(200))  # Satıcı/Tedarikçi
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.title} - {self.amount}TL>'

class Investment(db.Model):
    """Yatırım modeli - aidatlarla yapılan yatırımlar"""
    __tablename__ = 'investments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    investment_date = db.Column(db.Date, nullable=False)
    investment_type = db.Column(db.String(100))  # Tür (Döviz, Altın, vs.)
    current_value = db.Column(db.Numeric(10, 2))  # Güncel değer
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def profit_loss(self):
        """Kar/Zarar hesapla"""
        if self.current_value:
            return self.current_value - self.amount
        return 0
    
    def __repr__(self):
        return f'<Investment {self.title} - {self.amount}TL>'