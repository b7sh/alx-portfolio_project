from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # Importing necessary models


db = SQLAlchemy() # Initialize SQLAlchemy, the ORM used to interact with the database

class Transaction(db.Model):
    """
    This class defines the 'Transaction' model, representing a financial transaction in the database.
    It is mapped to the 'transactions' table in the MySQL database.
    """
    __tablename__ = 'transactions' # The name of the table in the database
    FORMAT = "%Y-%m-%d"  # Date format to be used when parsing date strings

    # Define the columns for the 'transactions' table
    id = db.Column(db.Integer, primary_key=True) # Primary key for each transaction
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, date, amount, category, description):
        """
        Constructor method that initializes a Transaction object.
        It converts the string date into a `datetime` object and ensures the amount is stored as a float.
        """
        self.date = datetime.strptime(date, Transaction.FORMAT)
        self.amount = float(amount)
        self.category = category
        self.description = description

    def __repr__(self):
        """
        Method to represent a Transaction object in a readable format.
        This is useful for debugging and logging purposes.
        """
        return f"Transaction({self.date}, {self.amount}, {self.category}, {self.description})"


def add_entry(transaction):
    """
    Function to add a transaction to the database.
    It takes a Transaction object as an argument, adds it to the session, and commits the session to save it.
    """
    db.session.add(transaction)
    db.session.commit()

def get_transactions(start_date, end_date):
    """
    Function to retrieve transactions within a specified date range.
    It filters the transactions between 'start_date' and 'end_date', and calculates the total income, 
    total expense, and balance (income - expenses) within that period.
    """
    # Convert the string datetime into a datetime object
    start_date = datetime.strptime(start_date, Transaction.FORMAT)
    end_date = datetime.strptime(end_date, Transaction.FORMAT)

    # Query the transactions table for records within the date range
    transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()

    # Calculate total income, total expense, and balance
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expense = sum(t.amount for t in transactions if t.category == 'Expense')
    balance = total_income - total_expense
    
    return transactions, total_income, total_expense, balance  # Return the filtered transactions and financial summary
