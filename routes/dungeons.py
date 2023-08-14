"""
    This Flask/Python file handles route for "Dungeons" table in the DB
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

dungeons_bp = Blueprint('dungeons', __name__)

@dungeons_bp.route("/dungeonSelection.html", methods=['GET', 'POST'])
def dungeon_selection():
    """
    handles CRUD functionality for dungeon selection page
    :return: render_template, redirect(url_for())
    """
    # if "username" in session:
    #     print("dungeonSelection username selected: ", session["username"])
    if request.method == "GET":
        cur = mysql.connection.cursor()

        if "username" in session:
            if session["username"] is not None:
                username = session["username"]
                curr_user_id = cur.execute(sql.get_user_id, [username])
                curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
                print("curr_user_id =", curr_user_id)
                user_dungeons = cur.execute(sql.get_user_dungeons, [curr_user_id][0][0])
                user_dungeons = cur.fetchall() if user_dungeons > 0 else ()
            else:
                username, user_dungeons = None, None
        else:
            username, user_dungeons = None, None

        all_dungeons = cur.execute(sql.get_all_dungeons)
        if all_dungeons > 0:
            all_dungeons = cur.fetchall()
        else:
            all_dungeons = ()

        # print("username =", username, file=sys.stderr)
        # print("all_dungeons =", all_dungeons, file=sys.stderr)
        return render_template('dungeonSelection.html',
                               username=username,
                               all_dungeons=all_dungeons,
                               user_dungeons=user_dungeons)


    elif request.method == "POST":
        print("button clicked =", request.form['button_press'],
              file=sys.stderr)
        if request.form['button_press'] == "insert":
            print("insert was clicked on dungeonSelection page")
            try:
                dungeon_name = request.form['dungeon_name']
                dungeon_type = request.form['dungeon_type']
                dungeon_description = request.form['dungeon_description']
                damage_multiplier = request.form['damage_multiplier']
                cur = mysql.connection.cursor()
                cur.execute(sql.add_dungeon, (dungeon_name, dungeon_type, dungeon_description, damage_multiplier))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for dungeon: {dungeon_name}", "info")
                return redirect(url_for("dungeons.dungeon_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("dungeons.dungeon_selection"))


        elif request.form['button_press'][0] == "d":
            print("delete was clicked on dungeonSelection page")
            dungeon_id = request.form['button_press'][1:]
            print("dungeon_id =", dungeon_id)
            try:
                dungeon_name = request.form['dungeon_name']
                dungeon_type = request.form['dungeon_type']
                dungeon_description = request.form['dungeon_description']
                damage_multiplier = request.form['damage_multiplier']
                cur = mysql.connection.cursor()
                cur.execute(sql.delete_dungeon, [dungeon_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row deleted for dungeon: {dungeon_name}", "info")
                return redirect(url_for("dungeons.dungeon_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("dungeons.dungeon_selection"))


        elif request.form['button_press'][0] == "u":
            print("update was clicked on dungeonSelection page")
            dungeon_id = request.form['button_press'][1:]
            print("dungeon_id =", dungeon_id)
            try:
                dungeon_name = request.form['dungeon_name']
                dungeon_type = request.form['dungeon_type']
                dungeon_description = request.form['dungeon_description']
                damage_multiplier = request.form['damage_multiplier']
                cur = mysql.connection.cursor()
                cur.execute(sql.update_dungeon, (dungeon_name, dungeon_type, dungeon_description, damage_multiplier, dungeon_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row updated for dungeon: {dungeon_name}", "info")
                return redirect(url_for("dungeons.dungeon_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("dungeons.dungeon_selection"))
