from flask import Blueprint, render_template, request, redirect, session
from .models import db, User, Expense
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect('/login')

# ---------- Register ----------
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing = User.query.filter_by(username=username).first()
        if not existing:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html')

# ---------- Login ----------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user_id'] = user.id
            return redirect('/dashboard')
    return render_template('login.html')

# ---------- Logout ----------
@main.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- Dashboard ----------
@main.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    user = User.query.get(user_id)
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template('dashboard.html', user=user, expenses=expenses, total=total)

# ---------- Add Expense ----------
@main.route('/add', methods=['GET', 'POST'])
def add_expense():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        note = request.form['note']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        expense = Expense(amount=amount, category=category, note=note, date=date, user_id=user_id)
        db.session.add(expense)
        db.session.commit()
        return redirect('/dashboard')
    
    return render_template('add_expense.html')
