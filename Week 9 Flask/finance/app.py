import os, datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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

    # Get Funds amount from cash
    user = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
    cash = user[0].get("cash")

    # Get user stocks
    all_trans = db.execute("SELECT name,symbol,SUM(shares),action FROM transactions GROUP BY symbol,action HAVING SUM(shares)>0 AND userid = :userid", userid=session["user_id"])
    all_symbols = db.execute("SELECT name,symbol,SUM(shares),action FROM transactions GROUP BY symbol HAVING SUM(shares)>0 AND userid = :userid", userid=session["user_id"])

    # Set up dictionary to pass to html
    holding = {}
    total = 0
    for i in all_symbols:
        shares = 0
        price_holding = 0
        for j in all_trans:
            if j.get("action") == "buy" and i.get("symbol") == j.get("symbol"):
                symbol = j.get("symbol")
                name = j.get("name")
                price = lookup(symbol).get("price")
                shares += j.get("SUM(shares)")
                price_holding += price * shares
                total += price_holding
                holding[symbol] = (symbol, name, shares, usd(price), usd(price_holding))
            if j.get("action") == "sell" and i.get("symbol") == j.get("symbol"):
                symbol = j.get("symbol")
                name = j.get("name")
                price = lookup(symbol).get("price")
                shares -= j.get("SUM(shares)")
                price_holding -= price * shares
                total -= price_holding
                holding[symbol] = (symbol, name, shares, usd(price), usd(price_holding))
    total += cash
    return render_template("index.html", stocks=holding, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Verify shares is an integer
        try:
            int(request.form.get("shares"))
        except ValueError:
            return apology("Shares must be a whole number")

        # Verify valid stock symbol
        if lookup(request.form.get("symbol")) == None:
            return apology("Invalid Stock")

        # Verify number of shares entered
        elif not request.form.get("shares") or int(request.form.get("shares")) < 1:
            return apology("Invalid Shares")

        # Get current stock price
        stock = lookup(request.form.get("symbol"))
        price=stock.get("price")

        # Get user funds
        user = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
        avail = user[0].get("cash")

        # Check for sufficient funds
        shares = int(request.form.get("shares"))
        current = shares*int(price)
        if avail < current:
            return apology("Insufficient Funds")

        # Update user cash
        db.execute("UPDATE users SET cash = :new WHERE id = :userid", userid=session["user_id"], new=avail-current)

        # Update database with transaction
        db.execute("INSERT INTO transactions (userid, action, name, symbol, shares, price, date) VALUES(:userid, :action, :name, :symbol, :shares, :price, :date)",
            userid=session["user_id"],
            action="buy",
            name=stock.get("name"),
            symbol=stock.get("symbol"),
            shares=shares,
            price=stock.get("price"),
            date=datetime.datetime.now())

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Insert Cash"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Verify cash is an integer
        try:
            int(request.form.get("amount"))
        except ValueError:
            return apology("Amount must be a whole number")

        # Verify number of shares entered
        if not request.form.get("amount") or int(request.form.get("amount")) < 1:
            return apology("Invalid Amount")

        # Redirect to stock quote if valid
        else:
            cash = int(request.form.get("amount"))
            user = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
            avail = user[0].get("cash")
            db.execute("UPDATE users SET cash = :new WHERE id = :userid", userid=session["user_id"], new=avail+cash)
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cash.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM transactions WHERE userid = :userid", userid=session["user_id"])
    # Set up dictionary to pass to html
    trans = {}
    for i in history:
        action = i.get("action")
        symbol = i.get("symbol")
        price = i.get("price")
        shares = i.get("shares")
        date = i.get("date")
        trans[i.get("id")] = (action, symbol, shares, price, date)
    return render_template("history.html", trans=trans)

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Verify valid stock symbol
        if lookup(request.form.get("symbol")) == None:
            return apology("Invalid Stock")

        # Redirect to stock quote if valid
        else:
            stock = lookup(request.form.get("symbol"))
            return render_template("quoted.html", name=stock.get("name"), price=stock.get("price"), symbol=stock.get("symbol"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation is not blank and matches password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't exist
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Hash password and register user
        else:
            usr = request.form.get("username")
            pasw = request.form.get("password")
            obfu = generate_password_hash(pasw, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", usr, obfu)
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has registered
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    transactions = db.execute("SELECT symbol,SUM(shares) FROM transactions GROUP BY symbol HAVING SUM(shares) > 0 AND userid = :userid", userid=session["user_id"])
    if request.method == "POST":

        # Verify valid stock symbol
        if not request.form.get("symbol"):
            return apology("Invalid Stock")

        # Verify number of shares entered
        elif not request.form.get("shares"):
            return apology("Invalid Shares")

        # Get current stock price
        stock = lookup(request.form.get("symbol"))
        symbol = stock.get("symbol")
        price=stock.get("price")

        # Get user funds
        user = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
        avail = user[0].get("cash")

        # Check for sufficient shares
        sum_shares = 0
        for i in transactions:
            if i.get("symbol") == symbol:
                sum_shares = i.get("SUM(shares)")
        shares = int(request.form.get("shares"))

        # Update user cash
        current = shares*int(price)
        if sum_shares > shares:
            db.execute("UPDATE users SET cash = :new WHERE id = :userid", userid=session["user_id"], new=avail+current)
        else:
            return apology("Insufficient Shares")

        # Update database with transaction
        db.execute("INSERT INTO transactions (userid, action, name, symbol, shares, price, date) VALUES(:userid, :action, :name, :symbol, :shares, :price, :date)",
            userid=session["user_id"],
            action="sell",
            name=stock.get("name"),
            symbol=stock.get("symbol"),
            shares=shares,
            price=stock.get("price"),
            date=datetime.datetime.now())

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Set up dictionary to pass to html
        stocks = {}
        for i in transactions:
            symbol = i.get("symbol")
            stocks[symbol] = (symbol)
        return render_template("sell.html", stocks=stocks)
