from flask import Flask, render_template, request, redirect, url_for
from models import db, Transaction, add_entry, get_transactions

app = Flask(__name__)

# Configure the MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Boshy%40*500@localhost:3306/finance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        date = request.form["date"]
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        transaction = Transaction(date, amount, category, description)
        add_entry(transaction)
        return redirect(url_for("index"))
    return render_template("add_transaction.html")

@app.route("/transactions", methods=["GET"])
def transactions():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date and end_date:
        transactions, total_income, total_expense, balance = get_transactions(start_date, end_date)
        return render_template("transactions.html", transactions=transactions, total_income=total_income, total_expense=total_expense, balance=balance)
    return render_template("transactions.html", transactions=None)


if __name__ == "__main__":
    app.run(debug=True)
