from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Transaction, add_entry, get_transactions, delete_transaction, edit_transaction
from datetime import datetime

# Create an instance of the Flask class for your web application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for security

# Configure the MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Boshy%40*500@localhost:3306/finance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications for performance

# Initialize the app with SQLAlchemy
db.init_app(app)

def create_tables():
    """
    This function ensures that all the necessary database tables are created
    before handling any requests by invoking db.create_all() once before the first request.
    """
    pass
    # db.create_all()

@app.route("/")
def index():
    """
    This route handles the home page of the application.
    It renders the 'index.html' template, which will be the main page of the app.
    """
    return render_template("index.html")

@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    """
    This route handles adding a new transaction. It accepts both GET and POST requests.
    - GET: Displays the form to add a new transaction.
    - POST: Processes the form data and adds the transaction to the database.
    """
    if request.method == "POST":
        # Retrieve form data from the HTML form
        date = request.form["date"]
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]

        # Create a new transaction object and add it to the database
        transaction = Transaction(date, amount, category, description)
        add_entry(transaction)

        # Show a success message to the user
        flash('Transaction added successfully!', 'success')

        # Redirect the user to the transactions page
        return redirect(url_for("transactions"))

    # Render the 'add_transaction.html' template for GET requests
    return render_template("add_transaction.html")

@app.route("/transactions", methods=["GET"])
def transactions():
    """
    This route handles displaying transactions with an optional filter by date range.
    It renders the 'transactions.html' template and shows the list of transactions, income, expenses, and balance.
    """
    # Retrieve optional date range from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Validate date range
    if start_date and end_date:
        if datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'):
            flash('Start date cannot be later than end date!', 'danger')
            return redirect(url_for('transactions'))

        # Get filtered transactions and financial summary
        transactions, total_income, total_expense, balance = get_transactions(start_date, end_date)
        return render_template("transactions.html", transactions=transactions, total_income=total_income, total_expense=total_expense, balance=balance)

    # Render 'transactions.html' without filtering if no date range is provided
    return render_template("transactions.html", transactions=None)

@app.route("/delete_transaction/<int:id>", methods=["POST"])
def delete_transaction_view(id):
    """
    This route handles deleting a transaction. It accepts POST requests and
    deletes the transaction with the given ID from the database.
    """
    delete_transaction(id)
    
    # Show a success message to the user
    flash('Transaction deleted successfully!', 'success')

    # Redirect to the transactions page
    return redirect(url_for('transactions'))

@app.route("/edit_transaction/<int:id>", methods=["GET", "POST"])
def edit_transaction_view(id):
    """
    This route handles editing a transaction. It accepts both GET and POST requests.
    - GET: Displays the form to edit a transaction with the given ID.
    - POST: Processes the form data and updates the transaction in the database.
    """
    # Retrieve the transaction by its ID or show 404 error if not found
    transaction = Transaction.query.get_or_404(id)

    if request.method == "POST":
        # Update the transaction object with form data
        transaction.date = datetime.strptime(request.form["date"], '%Y-%m-%d')
        transaction.amount = float(request.form["amount"])
        transaction.category = request.form["category"]
        transaction.description = request.form["description"]

        # Commit the updated transaction to the database
        db.session.commit()

        # Show a success message to the user
        flash('Transaction updated successfully!', 'success')

        # Redirect to the transactions page
        return redirect(url_for('transactions'))

    # Render the 'edit_transaction.html' template for GET requests
    return render_template("edit_transaction.html", transaction=transaction)

# Entry point for running the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)  # Enable debug mode for easier development
