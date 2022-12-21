# export API_KEY=pk_a30eefda623d4ec4b2dc12d70dc0f2b0
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Lines 51 - 57 ensure that the index displays and uses the most recently updated stock prices
    stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

    for stock in stocks:
        currentSymbol = stock["symbol"]
        stockInfo = lookup(currentSymbol)
        stockPrice = float(stockInfo["price"])
        db.execute("UPDATE transactions SET price = ? WHERE symbol = ?", stockPrice, currentSymbol)

    # Get the all the shares owned
    sharesOwned = db.execute(
        "SELECT symbol,name,SUM(shares) AS shares,price FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

    # Get the cash that the user has in the bank
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Determine the total value of all the user's owned stocks
    total = 0
    for element in sharesOwned:
        total += element["price"] * element["shares"]

    # Determine the total networth of the user (stock value plus cash in the bank)
    total += cash

    return render_template("index.html", sharesOwned=sharesOwned, usd=usd, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        symbolData = lookup(symbol)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        money = cash[0]
        # CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id int, symbol text, name text, shares int, price real, date timestamp);
        # CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id int, symbol text, name text, shares int, price real, date timestamp);

        # Render apology if no symbol is provided
        if not symbol:
            return apology("Missing Symbol")

        # Render apology if the number of shares is not provided
        if not shares:
            return apology("Missing Shares")

        # Render apology is symbol does not exist
        if not symbolData:
            return apology("Invalid Symbol")

        # Check that shares are numeric and no fractions are entered. Check that shares are positive integers
        if not shares.isnumeric():
            return apology("Error")

        elif not float(shares).is_integer() or int(shares) < 0:
            return apology("Error")

        newBalance = float(money["cash"]) - (int(shares) * float(symbolData["price"]))

        # Render apology if user cannot afford to buy the request shares
        if newBalance < 0:
            return apology("Error: Cannot Afford")

        # Update the cash that the user has left after the purchase
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newBalance, session["user_id"])

        # Record transaction in the transactions table in SQL and make a copy to keep track of the history (in the index, the transactions table will be updated to show most recent stock value. The history table will show the price at which the stock was bought)
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, date) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbolData["symbol"], symbolData["name"], int(shares), float(symbolData["price"]), datetime.datetime.now())
        db.execute("INSERT INTO history (user_id, symbol, name, shares, price, date) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbolData["symbol"], symbolData["name"], int(shares), float(symbolData["price"]), datetime.datetime.now())

        flash("Purchased!")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get all the transactions that the user has executed from the history table
    transactions = db.execute("SELECT symbol,shares,price,date FROM history WHERE user_id = ?", session["user_id"])

    return render_template("history.html", transactions=transactions, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbolData = lookup(symbol)

        # Render apology if no symbol is typed in
        if not symbol:
            return apology("Missing Symbol")

        # Render an apology if the symbol the user typed in does not exist
        if not symbolData:
            return apology("Invalid Symbol")

        # Render quoted template if symbol is valid
        return render_template("quoted.html", symbolData=symbolData, usd=usd)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passwordCheck = request.form.get("confirmation")

        # Render an apology if the user’s input is blank the username already exists
        if not username:
            return apology("Error Registering: Username Invalid")

        # Render an apology if the password is missing
        if not password:
            return apology("Error Registering: Missing Password")

        # Render an apology if passwords do not match
        if password != passwordCheck:
            return apology("Error Registering: Passwords Don't Match")

        # Insert the new user into the users database if all information is entered accurately
        passwordHash = generate_password_hash(password)

        # Render an apology if username already exists
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, passwordHash)
        except:
            return apology("Error Registering: Username Already Exists")

        flash("Registered! Please Log In")

        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Render apology if no symbol is entered
        if not symbol:
            return apology("Error: Missing Symbol")

        # Render apology if no shares are entered
        if not shares:
            return apology("Error: Missing Shares")

        # Get the stocks and shares that are currently owned, and add the selected symbol into a list
        ownedStocks = db.execute(
            "SELECT symbol, SUM(shares) AS shares FROM history WHERE user_id = ? GROUP BY symbol", session["user_id"])
        selectedStock = db.execute(
            "SELECT symbol, SUM(shares) AS shares FROM history WHERE symbol = ? AND user_id = ?", symbol, session["user_id"])

        # Render apology if the user does not own any stocks of the selected symbol
        if selectedStock[0]["shares"] < 1:
            return apology("Error: You do not Own this Stock")

        # Render apology if the user tries to sell more stocks than what they currently own
        shares = int(shares)
        if selectedStock[0]["shares"] < shares:
            return apology("Error: You do not own that many Shares")

        # Obtain the stock data and determine the updated cash the user will have in the bank after selling
        symbolData = lookup(symbol)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        updateCash = float(cash) + (shares * float(symbolData["price"]))

        # Update the cash the user has in the users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updateCash, session["user_id"])

        # Update the transactions and history tables with the details of the stocks sold
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, date) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbolData["symbol"], symbolData["name"], -shares, float(symbolData["price"]), datetime.datetime.now())
        db.execute("INSERT INTO history (user_id, symbol, name, shares, price, date) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbolData["symbol"], symbolData["name"], -shares, float(symbolData["price"]), datetime.datetime.now())

        flash("Sold!")

        return redirect("/")

    else:
        stocksOwned = db.execute(
            "SELECT symbol,SUM(shares) AS shares FROM history WHERE user_id = ? GROUP BY symbol", session["user_id"])

        symbolsOwned = []
        for stock in stocksOwned:
            if stock["shares"] > 0:
                symbolsOwned.append(stock["symbol"])

        return render_template("sell.html", symbolsOwned=symbolsOwned)


@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    """Add Cash to Account"""

    if request.method == "POST":
        amount = request.form.get("amount")

        # Get cash in users account
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Caluclate the new amount based on what the user typed in
        newAmount = float(cash) + float(amount)

        # Add the users updated balance into the users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])

        return redirect("/")

    else:
        return render_template("addcash.html")