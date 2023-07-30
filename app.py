"""
    Starter flask app to define primary routes.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from env.credentials import *
import queries as sql
import sys, logging
from datetime import timedelta

app = Flask(__name__)

app.config['MYSQL_HOST'] = ENV_HOST
app.config['MYSQL_USER'] = ENV_USERNAME
app.config['MYSQL_PASSWORD'] = ENV_PASSWORD
app.config['MYSQL_DB'] = ENV_DATABASE

# Sessions are only used for personalized table views,
# And for method .flash() to send user feedback
app.secret_key = session_key
app.permanent_session_lifetime = timedelta(hours=1)

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
    schema = open('db/ddl.sql', mode='r')
    statement_so_far = ''
    for line in schema.readlines():
        line = line.rstrip()
        statement_so_far += '\r\n' + line
        if line.endswith(';'):
            print(statement_so_far)
            cur.execute(statement_so_far)
            mysql.connection.commit()
            statement_so_far = ''
    cur.close()


# Populate the DB once on startup:
# ddl.sql is as single line of the schema as .execute only
# Executes one line per execute.
with app.app_context():
    generate_ddl()  # Comment this during development to save some time
    pass


def flash_err(e):
    if len(e.args) > 1:
        flash(f"Row insertion error: {e.args[1]}", "error")
    elif e.args:
        flash(f"Column: {e.args[0]}: {e}", "error")
    else:
        flash(f"Row insertion error: {e}", "error")


@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        if "username" in session:
            print("index.html username selected: ", session["username"])

        # Set default username to None
        if "username" not in session:
            session["username"] = None

        cur = mysql.connection.cursor()
        user_info = cur.execute(sql.get_all_users)
        user_rows = cur.fetchall() if user_info > 0 else ()

        return render_template('index.html',
                               user_rows=user_rows,
                               username=session["username"])
    if request.method == "POST":
        try:
            req = request.json
            if len(req) > 0:
                if len(req) == 2:
                    # save in session dict{} the username that was selected
                    # print("table: ", req["table"])
                    # print("username: ", req["username"])
                    if req["username"] == "None765":
                        session["username"] = None
                    else:
                        session["username"] = req["username"]
                    print("index.html username selected: ", session["username"])
                else:
                    cur = mysql.connection.cursor()
                    cur.execute(sql.insert_user, (req["username"], req["password"], req["email"]))
                    mysql.connection.commit()
                    cur.close()
                    flash(f"User Account '{req['username']}' added", "info")
                return "OK", 202  # JS is handling the page reload
        except Exception as exc:
            print(exc)
            flash_err(exc)
            return "NotOK", 500 # JS is handling the page reload


@app.route("/charPage.html", methods=['GET'])
def char_page():
    return render_template('charPage.html')

@app.route("/charSelection.html", methods=['GET', 'PATCH', 'POST'])
def char_selection_v2():
    if "username" in session:
        print("charSelection username selected: ", session["username"])
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

        return render_template('charSelection.html',
                           username=username,
                           all_chars=all_chars,
                           user_chars=user_chars)


    elif request.method == "POST":
        print("button clicked =", request.form['button_press'], file=sys.stderr)
        if request.form['button_press'] == "insert":
            print("insert was clicked on charSelection page")
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


        

            return render_template('charSelection.html',
                                    username=username,
                                    all_chars=all_chars,
                                    user_chars=user_chars)


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
                return redirect(url_for("char_selection_v2"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection_v2"))


        

            # return render_template('charSelection.html',
            #                         username=username,
            #                         all_chars=all_chars,
            #                         user_chars=user_chars)


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
                cur.execute(sql.update_char, (char_name, char_race, char_class, char_type, char_alignment, char_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row updated for char: {char_name}", "info")
                return redirect(url_for("char_selection_v2"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection_v2"))


        

           # return render_template('charSelection.html',
           #                         username=username,
           #                         all_chars=all_chars,
           #                         user_chars=user_chars)
    # elif request.method == "PATCH":
    #     print(request.json)
    #     return "OK", 202


# @app.route("/dungeonPage.html", methods=['GET'])
@app.route("/itemPage.html/item_id=<item_id>", methods=['GET'])
def item_page(item_id):
    print("item_id =", item_id)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        if item_id:
            #char_list = cur.fetchall() if chars > 0 else ()
            item = cur.execute(sql.get_item, [item_id])
            cur_item = cur.fetchall()[0] if item > 0 else ()

            print("item =", cur_item)
            return render_template('itemPage.html',
                                   item=cur_item)
        else:
            cur_item = None
            return render_template('itemPage.html',
                                   item=cur_item)


# @app.route("/dungeonPage.html", methods=['GET'])
@app.route("/dungeonPage.html/dungeon_id=<dungeon_id>", methods=['GET'])
def dungeon_page(dungeon_id):
    print("dungeon_id =", dungeon_id)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        if dungeon_id:
            dungeon = cur.execute(sql.get_dungeon, [dungeon_id])
            if dungeon > 0:
                dungeon = cur.fetchall()[0]
            print("dungeon =", dungeon)
            return render_template('dungeonPage.html', 
                                   dungeon_id=dungeon_id, 
                                   dungeon=dungeon)
        else:
            dungeon = None
            return render_template('dungeonPage.html', 
                                   dungeon_id=dungeon_id, 
                                   dungeon=dungeon)





@app.route("/dungeonSelection.html", methods=['GET', 'POST'])
def dungeon_selection():
    if "username" in session:
        print("dungeonSelection username selected: ", session["username"])
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


    elif request.method == "POST":
        print("button clicked =", request.form['button_press'], file=sys.stderr)
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
                return redirect(url_for("dungeon_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("dungeon_selection"))


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
                return redirect(url_for("dungeon_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("dungeon_selection"))


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
                return redirect(url_for("dungeon_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("dungeon_selection"))


# @app.route("/itemPage.html", methods=['GET'])
# def item_page():
#     return render_template('itemPage.html')

@app.route("/items.html", methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        # if "?" in request.url:
        #     print("Single item view clicked")
        #     return render_template('itemPage.html')
        cur = mysql.connection.cursor()
        items_info = cur.execute(sql.get_all_item_info)
        if items_info > 0:
            item_rows = cur.fetchall()

        return render_template('Items.html',
                               item_rows=item_rows)
    elif request.method == 'POST':
        try:
            if "insert_btn" in request.form.keys():
                item_name = request.form['Item Name']
                item_desc = request.form['Item Description']
                is_weapon = 1 if request.form['is_weapon'] == 'True' else 0
                cur = mysql.connection.cursor()
                cur.execute(sql.insert_new_item, (item_name, item_desc, is_weapon))
                mysql.connection.commit()
                cur.close()
            flash(f"Created new entry for item: {item_name}", "info")
            return redirect(url_for("items"))
        except Exception as exc:
            flash_err(exc)
            return redirect(url_for("items"))
    else:
        flash("route /items.html only accepts GET or POST requests", "error")
        return "route /items.html only accepts GET or POST requests", 505


@app.route("/itemSelection.html", methods=['GET', 'POST'])
def item_selection():
    if request.method == 'GET':

        # Logic to get the current user rows, or if no user then empty tuple ()
        cur_user_inv_table_rows = ()
        if "username" in session:
            if session["username"] is not None:
                #print("itemSelection username selected: ", session["username"])
                cur = mysql.connection.cursor()
                cur_usr = session["username"]
                #print(sql.individual_char_items % cur_usr)
                parsed = (sql.individual_char_items % cur_usr)
                cur_user_inv_items = cur.execute(parsed)
                cur_user_inv_table_rows = cur.fetchall() if cur_user_inv_items > 0 else ()
        else:
            session["username"] = None

        cur = mysql.connection.cursor()
        join_chars_items = cur.execute(sql.chars_items_qty)
        left_table_rows = cur.fetchall() if join_chars_items > 0 else ()

        # The following 2 queries are for dynamic dropdown input functionality:
        chars = cur.execute(sql.get_char_list)
        char_list = cur.fetchall() if chars > 0 else ()
        all_items = cur.execute(sql.get_item_list)
        item_list = cur.fetchall() if all_items > 0 else ()

        return render_template('itemSelection.html',
                               left_table_rows=left_table_rows,
                               right_table_rows=cur_user_inv_table_rows,
                               char_list=char_list,
                               item_list=item_list,
                               username=session["username"])
    if request.method == 'POST':
        try:
            print(request.form)
            if "delete_btn" in request.form.keys():
                print("delete clicked from inventory items panel")
                inventory_id = request.form['delete_btn'].split("=").pop(-1)
                print(sql.delete_item_from_inv % inventory_id)
                cur = mysql.connection.cursor()
                cur.execute(sql.delete_item_from_inv, (inventory_id,))
                mysql.connection.commit()
                cur.close()
                flash(f"Removed {request.form['item_quantity']} "
                      f"{request.form['item_name']}"
                      f" from {request.form['character_name']}'s inventory", "info")
            elif "update_btn" in request.form.keys():
                print("update clicked from inventory items panel")
                inventory_id = request.form['update_btn'].split("=").pop(-1)
                character_name = request.form['character_name']
                item_name = request.form['item_name']
                item_desc = request.form['item_description']
                item_qty = request.form['item_quantity']

                print("SQL statement to be executed:")
                query_parsed = (sql.update_inventory_items % (character_name, item_qty, item_name, item_desc, inventory_id))
                print(query_parsed)
                cur = mysql.connection.cursor()
                cur.execute(query_parsed)
                mysql.connection.commit()
                cur.close()
                flash(f"Update {request.form['character_name']}"
                      f" with {request.form['item_quantity']}"
                      f" of {request.form['item_name']}"
                      f": \"{request.form['item_description']}\"", "info")

            elif "insert_btn" in request.form.keys():
                print("insert clicked from bottom panel")
                char_id = request.form['character_id_name'].split(",").pop(0)
                char_name = request.form['character_id_name'].split(",").pop(1)
                item_id = request.form['item_id_name'].split(",").pop(0)
                item_name = request.form['item_id_name'].split(",").pop(1)
                item_qty = request.form['item_quantity']
                cur = mysql.connection.cursor()
                cur.execute(sql.insert_inv_items, (char_id, item_id, item_qty))
                mysql.connection.commit()
                cur.close()
                flash(f"Inserted {item_qty} "
                      f"of {item_name} "
                      f"into {char_name}'s inventory", "info")
            else:
                flash("Unknown POST sent to itemSelection route on Flask.", "error")
            return redirect(url_for("item_selection"))
        except Exception as exc:
            print(exc)
            flash(f"Error on Item_Selection POST route: {exc}", "error")
            return redirect(url_for("item_selection"))



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
