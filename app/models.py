from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'
    FORMAT = "%Y-%m-%d"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, date, amount, category, description):
        self.date = datetime.strptime(date, Transaction.FORMAT)
        self.amount = float(amount)
        self.category = category
        self.description = description

    def __repr__(self):
        return f"Transaction({self.date}, {self.amount}, {self.category}, {self.description})"

def add_entry(transaction):
    db.session.add(transaction)
    db.session.commit()

def get_transactions(start_date, end_date):
    start_date = datetime.strptime(start_date, Transaction.FORMAT)
    end_date = datetime.strptime(end_date, Transaction.FORMAT)

    transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
    
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expense = sum(t.amount for t in transactions if t.category == 'Expense')
    balance = total_income - total_expense
    
    return transactions, total_income, total_expense, balance
