from flask import Flask, render_template, request, redirect, url_for
from models import db, Transaction, add_entry, get_transactions  # Importing necessary models and helper functions


app = Flask(__name__)

# Configure the MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Boshy%40*500@localhost:3306/finance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the Flask app
db.init_app(app)


@app.before_request
def create_tables():
    """
    This function runs before every request.
    It ensures that all database tables are created before handling any requests.
    """
    db.create_all()

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
    This route handles adding a new transaction.
    If the request method is 'POST', it processes the form data and adds the transaction to the database.
    If the request method is 'GET', it renders the form page for adding a transaction.
    """
    if request.method == "POST":
        # Get data from the user
        date = request.form["date"]
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        # Create a new Transaction object using the form data
        transaction = Transaction(date, amount, category, description)
        # Use the add_entry function to add the transaction to the database
        add_entry(transaction)
        return redirect(url_for("index"))
    return render_template("add_transaction.html")

@app.route("/transactions", methods=["GET"])
def transactions():
    """
    This route displays all transactions or filters them based on a date range.
    If 'start_date' and 'end_date' are provided, it fetches transactions within that range.
    Otherwise, it shows an empty transaction list.
    """
    # Retrieve the start and end date from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date and end_date:
        # Get transactions, income, expenses, and balance for the given date range
        transactions, total_income, total_expense, balance = get_transactions(start_date, end_date)
        # Render the transactions.html template with the filtered data
        return render_template("transactions.html",
                                transactions=transactions, 
                                total_income=total_income, 
                                total_expense=total_expense, 
                                balance=balance)
    # If no date range is provided, render the transactions page with no transactions
    return render_template("transactions.html", transactions=None)


if __name__ == "__main__":
    app.run(debug=True) # Run the app in debug mode
