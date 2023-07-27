"""
    Starter flask app to define primary routes.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from env.credentials import *
import queries as sql
import sys, logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = ENV_HOST
app.config['MYSQL_USER'] = ENV_USERNAME
app.config['MYSQL_PASSWORD'] = ENV_PASSWORD
app.config['MYSQL_DB'] = ENV_DATABASE
app.secret_key = session_key

# app.config.from_pyfile(".env")

mysql = MySQL(app)

curr_user_id = 1

def generate_ddl():
    """
        Executes DB Schema
        Drops all tables and recreates default DB with sample data
    :return: None
    """
    cur = mysql.connection.cursor()
    schema = open('db/ddbtest.sql', mode='r')
    for statement in schema.readlines():
        statement = statement.rstrip()
        cur.execute(statement)
        mysql.connection.commit()
        print(statement)
    cur.close()


# Populate the DB once on startup, for now, like this:
# ddbtest.sql is as single line of the schema as .execute only
# Executes one line per execute.
with app.app_context():
    #generate_ddl()  # Comment this during development to save some time
    pass


def flash_err(e):
    if len(e.args) > 1:
        flash(f"Row insertion error: {e.args[1]}", "error")
    elif e.args:
        flash(f"Column: {e.args[0]}: {e}", "error")
    else:
        flash(f"Row insertion error: {e}", "error")

@app.route("/logout", methods=['GET'])
@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET'])
def index():
    if request.method == "GET":
        session["default"] = "default_session"
        cur = mysql.connection.cursor()
        user_info = cur.execute(sql.get_all_users)
        if user_info > 0:
            user_rows = cur.fetchall()

        return render_template('index.html',
                               user_rows=user_rows)
    if request.method == "POST":
        try:
            req = request.json
            if len(req) > 0:
                if len(req) == 2:
                    print("table: ", req["table"])
                    print("username: ", req["username"])
                else:
                    print("table: ", req["table"])
                    print("username: ", req["username"])
                    print("password: ", req["password"])
                    print("email: ", req["email"])
                return "OK", 200
            return "Empty request received", 500
        except Exception as exc:
            print(exc)
            return f"Exception on POST to / route: {exc}", 500


@app.route("/charPage.html", methods=['GET'])
def char_page():
    return render_template('charPage.html')




# TODO : New char_selection route
@app.route("/charSelection_v2.html", methods=['GET', 'POST'])
def char_selection_v2():

    
    if request.method == "GET":
        cur = mysql.connection.cursor()
            
        if curr_user_id:
            username = cur.execute(sql.get_user, [curr_user_id])
            if username > 0:
                username = cur.fetchall()
            user_chars = cur.execute(sql.get_user_chars, [curr_user_id])
            if user_chars > 0:
                user_chars = cur.fetchall()
        else:
            username, user_chars = None, None

        all_chars = cur.execute(sql.get_all_chars)
        if all_chars > 0:
            all_chars = cur.fetchall() 

        print("all_chars =", all_chars, file=sys.stderr)
        print("username =", username, file=sys.stderr)

        return render_template('charSelection_v2.html',
                           username=username,
                           all_chars=all_chars,
                           user_chars=user_chars)


    elif request.method == "POST":
        print("button clicked =", request.form['button_press'], file=sys.stderr)
        if request.form['button_press'] == "insert":
            print("insert was clicked")
            try:
                char_name = request.form['char_name']
                char_race = request.form['char_race']
                char_class = request.form['char_class']
                char_type = request.form['char_type']
                char_alignment = request.form['char_alignment']
                cur = mysql.connection.cursor()
                cur.execute(sql.add_char, (char_name, char_race, char_class, char_type, char_alignment, curr_user_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for char: {char_name}", "info")
                return redirect(url_for("char_selection_v2"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection_v2"))


        

            return render_template('charSelection_v2.html',
                                    username=username,
                                    all_chars=all_chars,
                                    user_chars=user_chars)


        elif request.form['button_press'][0] == "d":
            print("delete was clicked")
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
                return redirect(url_for("char_selection_v2"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection_v2"))


        

            return render_template('charSelection_v2.html',
                                    username=username,
                                    all_chars=all_chars,
                                    user_chars=user_chars)


        elif request.form['button_press'][0] == "u":
            print("update was clicked")
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
                cur.execute(sql.update_char, (char_name, char_race, char_class, char_type, char_alignment, char_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row updated for char: {char_name}", "info")
                return redirect(url_for("char_selection_v2"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection_v2"))


        

            return render_template('charSelection_v2.html',
                                    username=username,
                                    all_chars=all_chars,
                                    user_chars=user_chars)




@app.route("/dungeonPage.html", methods=['GET'])
def dungeon_page():
    return render_template('dungeonPage.html')



@app.route("/dungeonSelection.html", methods=['GET', 'POST'])
def dungeon_selection():
    if request.method == "GET":
        cur = mysql.connection.cursor()

        if curr_user_id:
            username = cur.execute(sql.get_user, [curr_user_id])
            if username > 0:
                username = cur.fetchall()
            user_dungeons = cur.execute(sql.get_user_dungeons, [curr_user_id])
            if user_dungeons > 0:
                user_dungeons = cur.fetchall()
        else:
            username, user_dungeons = None, None



        all_dungeons = cur.execute(sql.get_all_dungeons)
        if all_dungeons > 0:
            all_dungeons = cur.fetchall()


        # print("username =", username, file=sys.stderr)
        # print("all_dungeons =", all_dungeons, file=sys.stderr)
        return render_template('dungeonSelection.html',
                           username=username,
                           all_dungeons=all_dungeons,
                           user_dungeons=user_dungeons)


# TODO : Deprecated route
# @app.route("/charSelection.html", methods=['GET'])
# def char_selection():
#     return render_template('charSelection.html')


@app.route("/itemPage.html", methods=['GET'])
def item_page():
    return render_template('itemPage.html')


@app.route("/Items.html", methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        items_info = cur.execute(sql.get_all_item_info)
        if items_info > 0:
            item_rows = cur.fetchall()

        return render_template('Items.html',
                               item_rows=item_rows)
    elif request.method == 'POST':
        try:
            item_name = request.form['name']
            item_desc = request.form['description']
            is_weapon = 1 if request.form['is_weapon'] == 'True' else 0
            cur = mysql.connection.cursor()
            cur.execute(sql.insert_new_item, (item_name, item_desc, is_weapon))
            mysql.connection.commit()
            cur.close()
            flash(f"Row inserted for item: {item_name}", "info")
            return redirect(url_for("items"))
        except Exception as exc:
            flash_err(exc)
            return redirect(url_for("items"))
    else:
        flash("route /items.html only accepts GET or POST requests", "error")
        return "route /items.html only accepts GET or POST requests", 505


@app.route("/Inventory_Items.html", methods=['GET', 'POST'])
def item_selection():
    cur = mysql.connection.cursor()
    join_chars_items = cur.execute(sql.chars_items_qty)
    if join_chars_items > 0:
        left_table_rows = cur.fetchall()

    join_user_items = cur.execute(sql.individual_char_items)
    if join_user_items > 0:
        right_table_rows = cur.fetchall()

    # The following 2 queries are for dynamic dropdown input functionality:
    chars = cur.execute(sql.get_char_names)
    if chars > 0:
        char_list = cur.fetchall()

    items = cur.execute(sql.get_item_list)
    if items > 0:
        item_list = cur.fetchall()

    return render_template('Inventory_Items.html',
                           left_table_rows=left_table_rows,
                           right_table_rows=right_table_rows,
                           char_list=char_list,
                           item_list=item_list)


@app.route("/reload_the_db", methods=['POST'])
def reload_the_db():
    try:
        generate_ddl()
        flash("Database reloaded!", "success")
        return "OK!", 202
    except Exception as exc:
        print(exc)
        flash(f"Database reload error: {exc}", "error")
        return "Backend Exception on DB reload", 506


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
