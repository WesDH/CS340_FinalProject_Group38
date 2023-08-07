import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, render_template, request, flash, session
from db.mysql_initializer import mysql
from db import queries as sql

users_bp = Blueprint('users', __name__)


@users_bp.route("/", methods=['GET', 'POST'])
@users_bp.route("/index.html", methods=['GET', 'POST'])
def index():
    """
    Handles home route (User_Accounts Table)
    :return: response 202 OK, 500 Exception
    """
    if request.method == "GET":
        if "username" in session:
            print("index.html username selected: ", session["username"])

        # Set default username to None
        if "username" not in session:
            session["username"] = None

        # SELECT from users table to build frontend table
        cur = mysql.connection.cursor()
        user_info = cur.execute(sql.get_all_users)

        # Get user rows from cursor or set to empty tuple
        user_rows = cur.fetchall() if user_info > 0 else ()

        # pass user rows and current user to Jinja templating for index.html
        return render_template('index.html',
                               user_rows=user_rows,
                               username=session["username"])
    if request.method == "POST":
        try:
            # Grab the payload passed with fetch/POST from UX
            req = request.json
            if len(req) > 0:
                # If payload only has 2 key:value pairs it must be the
                # username dropdown:
                if len(req) == 2:
                    # Magic number just in case a user "None" exists:
                    if req["username"] == "None765":
                        session["username"] = None  # Store None as username
                    else:
                        # Store username selected from dropdown
                        session["username"] = req["username"]
                    # For debugging purposes print this out:
                    print("index.html username selected: ",
                          session["username"])
                # Otherwise payload must be from the INSERT username button:
                else:
                    cur = mysql.connection.cursor()

                    cur.execute(sql.insert_user, (
                        req["username"], req["password"], req["email"]))

                    mysql.connection.commit()
                    cur.close()

                    # Send feedback to UX with flash()
                    flash(f"User Account '{req['username']}' added", "info")
                return "OK", 202  # JS is handling the page reload
        except Exception as exc:
            # Exception handling, provide feedback to console and UX
            print(exc)
            flash_err(exc)
            return "NotOK", 503  # JS is handling the page reload
