Money Track App
Overview
The Money Track App is a simple web application built using Python and Flask that helps users track their income and expenses efficiently. It features a user-friendly interface for adding and viewing transactions, along with a summary displaying the total income, expenses, and the balance. The app is connected to a MySQL database for persistent data storage and supports basic CRUD operations.

Features
Add Transactions: Record your income and expenses with detailed information, including date, amount, category, and description.
Transaction History: View a list of all transactions filtered by date range.
Summary: Check the total income, expenses, and balance, automatically calculated based on the transaction data.
Delete Transactions: Remove incorrect or old transactions easily.
Contact Section: Connect with the developer on GitHub and Twitter for updates and feedback.
Technologies Used
Backend: Python (Flask Framework)
Frontend: HTML, Bootstrap
Database: MySQL
Other Tools: SQLAlchemy (ORM for database interaction)
Setup Instructions
Clone the repository:
bash
Copy code
git clone https://github.com/b7sh/the_porfolio
Navigate to the project directory:
bash
Copy code
cd money-track-app
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Set up the MySQL database. Create a new database and update the database configuration in the project code.

Run the Flask app:

bash
Copy code
python app.py
Open your browser and navigate to http://127.0.0.1:5000 to access the Money Track App.
Usage
Add a Transaction: Fill in the form to add a new transaction to the list.
View Transactions: Check the transaction history filtered by date.
Delete Transaction: Remove any transaction using the delete button.
Contact
GitHub: b7sh
Twitter (X): @b7sh_b7sh
