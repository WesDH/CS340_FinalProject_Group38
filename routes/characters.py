"""
    This Flask/Python file handles route for "Characters" table in the DB
    CRUD Functionality for this table implemented: Full CRUD
"""
import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, \
    render_template, request, redirect, url_for, \
    flash, session
from db.mysql_initializer import mysql
from db import queries as sql
from functions import flash_err

characters_bp = Blueprint('characters', __name__)

@characters_bp.route("/charSelection.html", methods=['GET', 'PATCH', 'POST'])
def char_selection():
    """
    handles CRUD functionality for character selection page
    :return: render_template, redirect(url_for())
    """
    if request.method == "GET":
        cur = mysql.connection.cursor()

        if session["username"]:
            username = session["username"]
            curr_user_id = cur.execute(sql.get_user_id, [username])
            curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
            print("curr_user_id =", curr_user_id)

            user_chars = cur.execute(sql.get_user_chars, [curr_user_id][0][0])
            user_chars = cur.fetchall() if user_chars > 0 else ()
        else:
            username, user_chars = None, None

        all_chars = cur.execute(sql.get_all_chars)
        if all_chars > 0:
            all_chars = cur.fetchall()
        else:
            all_chars = ()

        print("all_chars =", all_chars, file=sys.stderr)
        print("username =", username, file=sys.stderr)

        return render_template('charSelection.html',
                               username=username,
                               all_chars=all_chars,
                               user_chars=user_chars)

    elif request.method == "POST":
        print("button clicked =", request.form['button_press'],
              file=sys.stderr)

        cur = mysql.connection.cursor()

        if session["username"]:
            username = session["username"]
            curr_user_id = cur.execute(sql.get_user_id, [username])
            curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
            print("curr_user_id =", curr_user_id)

        if request.form['button_press'] == "insert":
            print("insert was clicked on charSelection page")
            try:
                char_name = request.form['char_name']
                char_race = request.form['char_race']
                char_class = request.form['char_class']
                char_type = request.form['char_type']
                char_alignment = request.form['char_alignment']
                cur = mysql.connection.cursor()
                cur.execute(sql.add_char, (
                    char_name, char_race, char_class, char_type,
                    char_alignment,
                    curr_user_id[0][0]))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for char: {char_name}", "info")
                return redirect(url_for("characters.char_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("characters.char_selection"))


        elif request.form['button_press'][0] == "d":
            print("delete was clicked on charSelection page")
            char_id = request.form['button_press'][1:]
            print("char_id =", char_id)
            try:
                char_name = request.form['char_name']
                char_race = request.form['char_race']
                char_class = request.form['char_class']
                char_type = request.form['char_type']
                char_alignment = request.form['char_alignment']
                cur = mysql.connection.cursor()
                cur.execute(sql.delete_char, [char_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row deleted for char: {char_name}", "info")
                return redirect(url_for("characters.char_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("characters.char_selection"))

        elif request.form['button_press'][0] == "u":
            print("update was clicked on charSelection page")
            char_id = request.form['button_press'][1:]
            print("char_id =", char_id)
            try:
                char_name = request.form['char_name']
                char_race = request.form['char_race']
                print("char_race:", char_race)
                char_class = request.form['char_class']
                char_type = request.form['char_type']
                char_alignment = request.form['char_alignment']
                cur = mysql.connection.cursor()
                cur.execute(sql.update_char, (
                    char_name, char_race, char_class, char_type,
                    char_alignment,
                    char_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row updated for char: {char_name}", "info")
                return redirect(url_for("characters.char_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("characters.char_selection"))
