import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query database for user cash
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    # Query database for user stocks
    rows = db.execute("SELECT * FROM stockholders WHERE user_id = ? AND shares > 0", session["user_id"])

    # Get user stocks table
    total = cash
    stocks = []
    for stock in rows:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stocks.append(stock)
        total += stock["price"] * stock["shares"]

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        elif not shares:
            return apology("must provide shares", 400)

        # Ensure shares is valid
        try:
            if int(shares) <= 0:
                return apology("shares must be a postive integer", 400)
        except ValueError:
            return apology("shares must be a postive integer", 400)

        quote = lookup(symbol)

        # Ensure symbol was valid
        if quote is None:
            return apology("invalid symbol", 400)

        # Query database for user cash
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]

        # Ensure user has enough cash
        used = quote["price"] * int(shares)
        if used > cash:
            return apology("can't affort", 400)

        # Insert to database
        db.execute("BEGIN")
        db.execute("INSERT INTO stockholders (user_id, symbol, shares) values (?, ?, ?) ON CONFLICT(user_id, symbol) DO UPDATE SET shares = shares + ?",
                   session["user_id"], symbol.upper(), int(shares), int(shares))
        db.execute("INSERT INTO stock_logs (user_id, symbol, shares, price, action) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], symbol.upper(), int(shares), quote["price"], 'BUY')
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", used, session["user_id"])
        db.execute("COMMIT")

        # show message
        flash("Bought!")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query database for user cash
    rows = db.execute("SELECT * FROM stock_logs WHERE user_id = ?", session["user_id"])

    return render_template("history.html", histories=rows)


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

        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)

        # Ensure simbol was valid
        if quote is None:
            return apology("invalid symbol", 400)

        return render_template("quote.html", quote=quote)

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

        # Get form value
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must provide password (again)", 400)

        # Ensure username is not registered
        elif len(rows) > 0:
            return apology("Username is not available ", 400)

        # Ensure password and confirmation are same
        elif password != confirmation:
            return apology("Passwords do not match ", 400)

        # Insert new user to database
        hashpass = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashpass)

        # Query database for new username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # show message
        flash("Registered!")

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
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        elif not shares:
            return apology("must provide shares", 400)

        # Ensure shares is valid
        try:
            if int(shares) <= 0:
                return apology("shares must be a postive integer", 400)
        except ValueError:
            return apology("shares must be a postive integer", 400)

        quote = lookup(symbol)

        # Ensure symbol was valid
        if quote is None:
            return apology("invalid symbol", 400)

        # Query database for user stocks
        rows = db.execute("SELECT * FROM stockholders WHERE user_id = ? AND symbol = ?", session["user_id"], symbol.upper())

        # Ensure user has enough shares
        if len(rows) == 0:
            return apology("can't affort", 400)
        old_shares = rows[0]["shares"]
        if int(shares) > old_shares:
            return apology("too many shares", 400)

        prices = quote["price"] * int(shares)

        # Insert to database
        db.execute("BEGIN")
        db.execute("UPDATE stockholders SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
                   int(shares), session["user_id"], symbol.upper())
        db.execute("INSERT INTO stock_logs (user_id, symbol, shares, price, action) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], symbol.upper(), int(shares), quote["price"], 'SELL')
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", prices, session["user_id"])
        db.execute("COMMIT")

        flash("Sold!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Query database for user stocks
        rows = db.execute("SELECT symbol FROM stockholders WHERE user_id = ? AND shares > 0", session["user_id"])

        return render_template("sell.html", stocks=rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
