from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import pdfplumber
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business_valuation.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    company_name = db.Column(db.String(120))
    valuations = db.relationship('Valuation', backref='user', lazy=True)

class Valuation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    revenue = db.Column(db.Float)
    ebitda = db.Column(db.Float)
    fcf = db.Column(db.Float)
    growth_rate = db.Column(db.Float)
    wacc = db.Column(db.Float)
    pe_ratio = db.Column(db.Float)
    ps_ratio = db.Column(db.Float)
    valuation_result = db.Column(db.JSON)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            company_name=company_name
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/valuation', methods=['GET', 'POST'])
@login_required
def valuation():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        valuation = Valuation(
            user_id=current_user.id,
            revenue=float(data.get('revenue', 0)),
            ebitda=float(data.get('ebitda', 0)),
            fcf=float(data.get('fcf', 0)),
            growth_rate=float(data.get('growth_rate', 0)),
            wacc=float(data.get('wacc', 0)),
            pe_ratio=float(data.get('pe_ratio', 0)),
            ps_ratio=float(data.get('ps_ratio', 0))
        )
        
        # Calculate valuation (simplified example)
        result = {
            'enterprise_value': valuation.revenue * valuation.ps_ratio,
            'equity_value': valuation.ebitda * valuation.pe_ratio,
            'dcf_value': calculate_dcf_value(valuation)
        }
        
        valuation.valuation_result = result
        db.session.add(valuation)
        db.session.commit()
        
        return jsonify(result)
    
    return render_template('valuation_form.html')

@app.route('/upload_tax_return', methods=['POST'])
@login_required
def upload_tax_return():
    if 'tax_return' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['tax_return']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Process PDF and extract data
        extracted_data = extract_tax_return_data(file)
        return jsonify(extracted_data)

def extract_tax_return_data(file):
    extracted_data = {}
    try:
        with pdfplumber.open(file) as pdf:
            # This is a simplified example - you would need to implement
            # proper PDF parsing logic based on tax return format
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            
            # Example parsing logic (would need to be customized)
            if 'TOTAL REVENUE' in text:
                # Extract revenue data
                pass
            if 'NET INCOME' in text:
                # Extract income data
                pass
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
    
    return extracted_data

def calculate_dcf_value(valuation):
    # Simplified DCF calculation
    try:
        future_fcf = valuation.fcf * (1 + valuation.growth_rate)
        terminal_value = future_fcf / (valuation.wacc - valuation.growth_rate)
        present_value = terminal_value / (1 + valuation.wacc)
        return present_value
    except:
        return 0

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        db.create_all()
    app.run(debug=True)
