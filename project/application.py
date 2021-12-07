import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from cronjobs import cron
from helpers import apology, login_required, date
from minibuses import minibus_route_stop_data, minibuses_stop_route_data, minibuses_eta_stop_data, minibuses_eta_route_stop_data

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["date"] = date

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Run cron
cron()


@app.route("/")
@login_required
def index():
    """Home page"""

    # Query database check user has added stop
    stops = db.execute("SELECT * FROM user_route_stops WHERE user_id = ?", session["user_id"])

    if len(stops) == 0:
        flash("Loading default, you can add route stop in list.")

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

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


@app.route("/minibuses")
def minibuses():
    """Minibus page"""

    # Get args
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    option = request.args.get('option')
    size = 20
    offset = (page - 1) * size

    # Format search column name
    if option == "route_name":
        col = "route_name"
    else:
        col = "route_name"

    # Query database
    if search is None:
        rows = db.execute(f"SELECT * FROM minibuses LIMIT {size} OFFSET {offset};")
    else:
        rows = db.execute(f"SELECT * FROM minibuses WHERE UPPER({col}) LIKE ? LIMIT {size} OFFSET {offset};", f"%{search}%")

    if search is None:
        if page == 1:
            return render_template("minibuses.html", minibuses=rows, more="/minibuses?page=2")
        else:
            return render_template("minibuses_list.html", minibuses=rows, more=f"/minibuses?page={page + 1}")
    else:
        return render_template("minibuses_list.html", minibuses=rows, more=f"/minibuses?page={page + 1}&search={search}&option={option}")


@app.route("/minibus/<route_id>/<route_seq>")
def minibus(route_id, route_seq):
    """Minibus page"""

    # Query database
    rows = db.execute("SELECT * FROM minibuses WHERE route_id = ? AND route_seq = ?;", route_id, route_seq)
    return render_template("minibus.html", routes=minibus_route_stop_data(route_id, route_seq), minibus=rows[0])


@app.route("/realtime", methods=["GET", "POST"])
@login_required
def realtime_all():
    """Realtime html"""

    if request.method == "POST":
        route_id = request.form.get("route_id")
        route_seq = request.form.get("route_seq")
        stop_seq = request.form.get("stop_seq")

        # Ensure symbol was submitted
        if not route_id:
            return apology("must provide route_id", 400)

        # Ensure shares was submitted
        elif not route_seq:
            return apology("must provide route_seq", 400)

        # Ensure shares was submitted
        elif not stop_seq:
            return apology("must provide stop_seq", 400)

        rows = db.execute("SELECT * FROM user_route_stops WHERE user_id = ? AND route_id = ? AND route_seq = ? AND stop_seq = ?;",
                          session["user_id"], route_id, route_seq, stop_seq)

        if len(rows) == 0:
            db.execute("INSERT INTO user_route_stops (user_id, route_id, route_seq, stop_seq) values (?, ?, ?, ?);",
                       session["user_id"], route_id, route_seq, stop_seq)

        # Redirect user to home page
        return redirect("/")
    else:
        result = []

        # Query database check user has added stop
        stops = db.execute("SELECT * FROM user_route_stops WHERE user_id = ?", session["user_id"])

        if len(stops) > 0:
            for stop in stops:
                rows = db.execute("SELECT * FROM minibuses WHERE route_id = ? AND route_seq = ?;",
                                  stop["route_id"], stop["route_seq"])
                if len(rows) > 0:
                    stop["route_name"] = rows[0]["route_name"]
                    stop["district"] = rows[0]["district"]
                    stop["start_name"] = rows[0]["start_name"]
                    stop["end_name"] = rows[0]["end_name"]
                    try:
                        # Get route stop detail
                        route_data = minibus_route_stop_data(stop["route_id"], stop["route_seq"])
                        stop["name_en"] = [x for x in route_data["data"]["route_stops"]
                                           if x["stop_seq"] == stop["stop_seq"]][0]["name_en"]
                        # Get route stop eta
                        route_stop_eta = minibuses_eta_route_stop_data(stop["route_id"], stop["route_seq"], stop["stop_seq"])
                        stop["diff"] = route_stop_eta["eta"][0]["diff"]
                        stop["remark"] = route_stop_eta["eta"][0]["remarks_en"]
                        stop["isAdded"] = True
                        result.append(stop)
                    except:
                        #  print("An exception occurred")
                        print("No data")
        else:
            # Get default realtime data
            stop = minibuses_stop_route_data()
            eta = minibuses_eta_stop_data()

            # Query database
            for route in stop:
                rows = db.execute("SELECT * FROM minibuses WHERE route_id = ? AND route_seq = ?;",
                                  route["route_id"], route["route_seq"])
                if len(rows) > 0:
                    route["route_name"] = rows[0]["route_name"]
                    route["district"] = rows[0]["district"]
                    route["start_name"] = rows[0]["start_name"]
                    route["end_name"] = rows[0]["end_name"]
                    try:
                        # Get route eta
                        route_stop_eta = [x for x in eta if x["route_id"] == route["route_id"]
                                          and x["route_seq"] == route["route_seq"] and x["stop_seq"] == route["stop_seq"]][0]
                        route["diff"] = route_stop_eta["eta"][0]["diff"]
                        route["remark"] = route_stop_eta["eta"][0]["remarks_en"]
                        result.append(route)
                    except:
                        #  print("An exception occurred")
                        print("No data")

        return render_template("routes_list.html", routes=result)


@app.route("/api/minibuses")
def api_minibuses():
    """Minibuses Search API"""

    # Get args
    search = request.args.get('search')
    option = request.args.get('option')
    page = request.args.get('page', 1, type=int)
    size = 20
    offset = (page - 1) * size

    # Format search column name
    if option == "route_name":
        col = "route_name"
    else:
        col = "route_name"

    # Query database
    if search is None:
        rows = db.execute(f"SELECT * FROM minibuses LIMIT {size} OFFSET {offset};")
        count = db.execute(f"SELECT COUNT(*) AS s FROM minibuses;")
    else:
        rows = db.execute(f"SELECT * FROM minibuses WHERE UPPER({col}) LIKE ? LIMIT {size} OFFSET {offset};", f"%{search}%")
        count = db.execute(f"SELECT COUNT(*) AS s FROM minibuses WHERE UPPER({col}) LIKE ?;", f"%{search}%")

    # Return
    f = {
        "data": rows,
        "page": page,
        "size": size,
        "total": count[0]["s"],
        "has_next": count[0]["s"] >= page * size,
        "next": f"/minibuses?page={page + 1}&search=${search}&option={option}"
    }
    if search is None:
        f["next"] = f"/minibuses?page={page + 1}"

    return f


@app.route("/api/realtime/<route_id>/<route_seq>/<stop_seq>", methods=["GET", "DELETE"])
@login_required
def realtime_route_stop(route_id, route_seq, stop_seq):
    """Route Stop Realtime API"""

    if request.method == "DELETE":
        db.execute("DELETE FROM user_route_stops WHERE user_id = ? AND route_id = ? AND route_seq = ? AND stop_seq = ?;",
                   session["user_id"], route_id, route_seq, stop_seq)

        # Redirect user to home page
        return {"message": "OK"}
    else:
        return minibuses_eta_route_stop_data(route_id, route_seq, stop_seq)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Run Application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

