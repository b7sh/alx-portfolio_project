from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Define the Transaction model
class Transaction(db.Model):
    __tablename__ = 'transactions'  # Specifies the table name in the database
    FORMAT = "%Y-%m-%d"  # Date format for transactions

    # Define the table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the transaction
    date = db.Column(db.Date, nullable=False)  # Transaction date (cannot be null)
    amount = db.Column(db.Float, nullable=False)  # Transaction amount (cannot be null)
    category = db.Column(db.String(255), nullable=False)  # Transaction category (Income/Expense)
    description = db.Column(db.String(255), nullable=False)  # Transaction description (cannot be null)

    def __init__(self, date, amount, category, description):
        """
        Constructor method for initializing a transaction instance.
        The date is converted from string to a datetime object.
        The amount is converted to a float.
        """
        self.date = datetime.strptime(date, Transaction.FORMAT)
        self.amount = float(amount)
        self.category = category
        self.description = description

    def __repr__(self):
        """
        String representation of the Transaction object.
        This is useful for debugging and logging purposes.
        """
        return f"Transaction({self.date}, {self.amount}, {self.category}, {self.description})"

# Function to add a new transaction entry to the database
def add_entry(transaction):
    """
    Adds a new transaction to the database.
    Commits the session to save the data.
    """
    db.session.add(transaction)
    db.session.commit()

# Function to retrieve transactions within a date range
def get_transactions(start_date, end_date):
    """
    Retrieves all transactions between the specified start and end dates.
    It calculates the total income, total expense, and balance from the transactions.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, Transaction.FORMAT)
    end_date = datetime.strptime(end_date, Transaction.FORMAT)

    # Query the database to get transactions in the specified date range
    transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()

    # Calculate total income and total expense
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expense = sum(t.amount for t in transactions if t.category == 'Expense')

    # Calculate the balance (income - expenses)
    balance = total_income - total_expense

    return transactions, total_income, total_expense, balance

# Function to delete a transaction by its ID
def delete_transaction(transaction_id):
    """
    Deletes a transaction from the database by its ID.
    Commits the session to apply the deletion.
    """
    # Retrieve the transaction by its ID and delete it from the database
    transaction = Transaction.query.get(transaction_id)
    db.session.delete(transaction)
    db.session.commit()

# Function to edit an existing transaction
def edit_transaction(transaction):
    """
    Updates the database with changes to an existing transaction.
    Commits the session to save the updated data.
    """
    db.session.commit()
