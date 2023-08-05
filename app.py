"""
-- CS340 Final Project, Summer 2023: Dungeons and Dragons Character Manager
-- GROUP 38: Joseph Houghton, Lauren Norman Schueneman, Wesley Havens
--
-- App.py is the logic for handling DB and UI interactions via routes with Flask
"""

from flask import Flask, render_template, request, redirect, url_for, flash, \
    session
from flask_mysqldb import MySQL
from env.credentials import *
from db import queries as sql
import sys
from datetime import timedelta

app = Flask(__name__)
app_port = 19806

# Custom variables defined below:
# Please create env/credentials.py to define these 4 ENV variables
app.config['MYSQL_HOST'] = ENV_HOST
app.config['MYSQL_USER'] = ENV_USERNAME
app.config['MYSQL_PASSWORD'] = ENV_PASSWORD
app.config['MYSQL_DB'] = ENV_DATABASE

# Sessions are only used for personalized table views,
# and for method .flash() to send user feedback
# "session_key" is defined in env/credentials.py
# And may be any string
app.secret_key = session_key
app.permanent_session_lifetime = timedelta(hours=1)

# app.config.from_pyfile(".env")

mysql = MySQL(app)


def generate_ddl():
    """
        Executes ddl.sql DB Schema
        Drops all tables and recreates default DB with sample data
    :return: None
    """
    cur = mysql.connection.cursor()
    schema = open('db/ddl.sql', mode='r')
    statement_so_far = ''
    # Convert multiline SQL statements into single line statements:
    for line in schema.readlines():
        line = line.rstrip()
        statement_so_far += '\r\n' + line
        # Execute a SQL statement when we encounter a ';' in the DDL
        if line.endswith(';'):
            print(statement_so_far)
            cur.execute(statement_so_far)
            mysql.connection.commit()
            statement_so_far = ''
    cur.close()


# Populate the DB once on startup:
with app.app_context():
    # generate_ddl()  # Comment this line during development to save some time
    pass


def flash_err(e):
    """
        Provides more details for flash() messages on Exception
    :param e: type() Exception
    :return: None
    """
    if len(e.args) > 1:  # This will give more info back to the UX
        flash(f"Row insertion error: {e.args[1]}", "error")
    elif e.args:
        flash(f"Column: {e.args[0]}: {e}", "error")
    else:
        flash(f"Row insertion error: {e}", "error")


@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
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
                        session["username"] = None # Store None as username
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

@app.route("/spells_abilities.html", methods=['GET', 'POST'])
def spells_abilities_page():
    """
    handles CRUD functionality for spells and abilities 
    """
    if request.method == "GET":
        cur = mysql.connection.cursor()

        # get user abilities & user spells
        if session["username"]:
            username = session["username"]
            curr_user_id = cur.execute(sql.get_user_id, [username])
            curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
            print("curr_user_id =", curr_user_id)

            user_abilities = cur.execute(sql.get_user_abilities, [curr_user_id][0][0])
            if user_abilities > 0:
                user_abilities = cur.fetchall()
                user_abilities_list = []
                for ability in user_abilities:
                    ability = list(ability)
                    # print(ability)
                    if ability[3]:
                        # this ability has a dungeon_id
                        dungeon_name = cur.execute(sql.get_ability_dungeon, [ability[3]])
                        dungeon_name = cur.fetchall()[0][0]
                        ability[3] = dungeon_name
                    else:
                        # this ability does NOT have a dungeon_id
                        ability[3] = "No Dungeon"
                    # print(ability)
                    user_abilities_list.append(ability)

            else:
                user_abilities_list = ()

            user_spells = cur.execute(sql.get_user_spells, [curr_user_id][0][0])
            if user_spells > 0:
                user_spells = cur.fetchall()
            else:
                user_spells = ()

            user_chars = cur.execute(sql.get_user_chars, [curr_user_id][0][0])
            if user_chars > 0:
                user_chars = cur.fetchall()
            else:
                user_chars = ()

        else:
            username = user_abilities_list = user_spells = user_chars = None 


        # get all abilities & all spells & all dungeons
        try: 
            all_abilities = cur.execute(sql.get_all_abilities)
            if all_abilities > 0:
                all_abilities = cur.fetchall() 
                all_abilities_list = []
                for ability in all_abilities:
                    ability = list(ability)
                    # print(ability)
                    if ability[3]:
                        # this ability has a dungeon_id
                        dungeon_name = cur.execute(sql.get_ability_dungeon, [ability[3]])
                        dungeon_name = cur.fetchall()[0][0]
                        ability[3] = dungeon_name
                    else:
                        # this ability does NOT have a dungeon_id
                        ability[3] = "No Dungeon"
                    # print(ability)
                    all_abilities_list.append(ability)
                    
            else:
                all_abilities_list = ()

            
            all_spells = cur.execute(sql.get_all_spells)
            all_spells = cur.fetchall() if all_spells > 0 else ()

            all_dungeons = cur.execute(sql.get_all_dungeons)
            all_dungeons = cur.fetchall() if all_dungeons > 0 else ()


            return render_template('spells_abilities.html',
                               username=username,
                               all_abilities=all_abilities_list,
                               all_spells=all_spells,
                               all_dungeons=all_dungeons,
                               user_abilities=user_abilities_list,
                               user_spells=user_spells,
                               user_chars=user_chars)


        except Exception as exc:
            print(exc)
            flash_err(exc)
            # Send the user to home page for now if Exception:
            return redirect(url_for("index")) 


    elif request.method == "POST":
        cur = mysql.connection.cursor()

        # get all abilities & all spells & all dungeons
        try: 
            all_abilities = cur.execute(sql.get_all_abilities)
            if all_abilities > 0:
                all_abilities = cur.fetchall() 
                all_abilities_list = []
                for ability in all_abilities:
                    ability = list(ability)
                    # print(ability)
                    if ability[3]:
                        # this ability has a dungeon_id
                        dungeon_name = cur.execute(sql.get_ability_dungeon, [ability[3]])
                        dungeon_name = cur.fetchall()[0][0]
                        ability[3] = dungeon_name
                    else:
                        # this ability does NOT have a dungeon_id
                        ability[3] = "No Dungeon"
                    # print(ability)
                    all_abilities_list.append(ability)
                    
            else:
                all_abilities_list = ()

            
            all_spells = cur.execute(sql.get_all_spells)
            all_spells = cur.fetchall() if all_spells > 0 else ()

            all_dungeons = cur.execute(sql.get_all_dungeons)
            all_dungeons = cur.fetchall() if all_dungeons > 0 else ()

        except Exception as exc:
            print(exc)
            flash_err(exc)
            # Send the user to home page for now if Exception:
            return redirect(url_for("index")) 




        print("button clicked =", request.form['button_press'],
              file=sys.stderr)
         

        if session["username"]:
            username = session["username"]
            curr_user_id = cur.execute(sql.get_user_id, [username])
            curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
            print("curr_user_id =", curr_user_id)

        if request.form['button_press'] == "ability_insert":
            print("ability insert was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_name = request.form['ability_name']
                ability_damage = request.form['ability_damage']
                ability_dungeon_id = request.form['ability_dungeon']
                if ability_dungeon_id == "No Dungeon":
                    cur.execute("INSERT INTO Abilities (ability_name, ability_damage, Dungeons_dungeon_id) VALUES (%s, %s, %s);", (ability_name, ability_damage, None))
                else:
                    cur.execute(sql.add_ability, (ability_name, ability_damage, ability_dungeon_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for Abilities: {ability_name}", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))

        elif request.form['button_press'] == "spell_insert":
            print("spell insert was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_name = request.form['spell_name']
                spell_damage = request.form['spell_damage']
                cur.execute(sql.add_spell, (spell_name, spell_damage))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for Spells: {spell_name}", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))


        elif request.form['button_press'][0:4] == "adda":
            print("Ability ADD was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_id = request.form['button_press'][4:]
                char_id = request.form['ability_user_char']
                cur.execute(sql.add_ability_to_char, (char_id, ability_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for Characters_has_Abilities", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))


        elif request.form['button_press'][0:4] == "adds":
            print("Spell ADD was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_id = request.form['button_press'][4:]
                char_id = request.form['spell_user_char']
                cur.execute(sql.add_spell_to_char, (char_id, spell_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for Characters_has_Spells", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))

        elif request.form['button_press'][0:4] == "dela":
            print("Ability DELETE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_id = request.form['button_press'][4:]
                cur.execute(sql.delete_ability, [ability_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row Deleted for Abilities", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))

        elif request.form['button_press'][0:2] == "a#":
            print("Characters_has_Abilities DELETE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_id = request.form['button_press'].split('#')[1]
                char_name = request.form['button_press'].split('#')[2]
                char_id = cur.execute(sql.get_char_id, [char_name])
                char_id = cur.fetchall() if char_id > 0 else None
                cur.execute(sql.delete_user_ability, [ability_id, char_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row Deleted for Characters_has_Abilities", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))

        elif request.form['button_press'][0:4] == "upda":
            print("Ability UPDATE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_id = request.form['button_press'][4:]
                ability_name = request.form['ability_name']
                ability_damage = request.form['ability_damage']
                ability_dungeon_id = request.form['ability_dungeon']
                print(ability_name, ability_damage, ability_dungeon_id, ability_id)
                if ability_dungeon_id == "No Dungeon": 
                    cur.execute("UPDATE Abilities SET ability_name = %s, ability_damage = %s, Dungeons_dungeon_id = %s WHERE ability_id = %s;", (ability_name, ability_damage, None, ability_id))
                else:
                    cur.execute(sql.update_ability, (ability_name, ability_damage, ability_dungeon_id, ability_id)) 
                mysql.connection.commit()
                cur.close()
                flash(f"Row Updated for Abilities", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))


        elif request.form['button_press'][0:4] == "dels":
            print("Spell DELETE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_id = request.form['button_press'][4:]
                cur.execute(sql.delete_spell, [spell_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row Deleted for Spells", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))

        elif request.form['button_press'][0:2] == "s#":
            print("Characters_has_Spells DELETE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_id = request.form['button_press'].split('#')[1]
                char_name = request.form['button_press'].split('#')[2]
                char_id = cur.execute(sql.get_char_id, [char_name])
                char_id = cur.fetchall() if char_id > 0 else None
                cur.execute(sql.delete_user_spell, [spell_id, char_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row Deleted for Characters_has_Spells", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))

        elif request.form['button_press'][0:4] == "upds":
            print("Spell UPDATE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_id = request.form['button_press'][4:]
                spell_name = request.form['spell_name']
                spell_damage = request.form['spell_damage']
                print(spell_name, spell_damage, spell_id)
                cur.execute(sql.update_spell, (spell_name, spell_damage, spell_id)) 
                mysql.connection.commit()
                cur.close()
                flash(f"Row Updated for Spells", "info")
                return redirect(url_for("spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities_page"))



@app.route("/charSelection.html", methods=['GET', 'PATCH', 'POST'])
def char_selection():
    """
    handles CRUD functionality for character selection page
    """
    # if "username" in session:
    #     print("charSelection username selected: ", session["username"])
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
                char_name, char_race, char_class, char_type, char_alignment,
                curr_user_id[0][0]))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for char: {char_name}", "info")
                return redirect(url_for("char_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection"))


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
                return redirect(url_for("char_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection"))

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
                char_name, char_race, char_class, char_type, char_alignment,
                char_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row updated for char: {char_name}", "info")
                return redirect(url_for("char_selection"))
            except Exception as exc:
                flash_err(exc)
                return redirect(url_for("char_selection"))


@app.route("/charPage.html/char_id=<char_id>", methods=['GET'])
def char_page(char_id):
    """
    char_page generates single item view from Characters table
    :param char_id: the Characters.character_id PK
    :return: render_template
    """
    print("char_id =", char_id)
    if request.method == "GET":
        cur = mysql.connection.cursor()

        if session["username"]:
            username = session["username"]
            curr_user_id = cur.execute(sql.get_user_id, [username])
            curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
            print("curr_user_id =", curr_user_id)
        else:
            username = None

        if char_id:
            char = cur.execute(sql.get_char, [char_id])
            char = cur.fetchall()[0] if char > 0 else ()
            print("char =", char)        
        else:
            char = None

        if username and char_id:
            char_spells = cur.execute(sql.get_char_spells, [char_id])
            char_spells = cur.fetchall() if char_spells > 0 else ()
            char_abilities = cur.execute(sql.get_char_abilities, [char_id])
            char_abilities = cur.fetchall() if char_abilities > 0 else ()
            if char_spells:
                if char_spells[0][3] != username:
                    # user is selected but that user is viewing some other users' characters
                    username = char_spells[0][3]
            if char_abilities:
                if char_abilities[0][4] != username:
                    # user is selected but that user is viewing some other users' characters
                    username = char_abilities[0][4]

        elif char_id:
            char_spells = cur.execute(sql.get_char_spells, [char_id])
            char_spells = cur.fetchall() if char_spells > 0 else ()
            char_abilities = cur.execute(sql.get_char_abilities, [char_id])
            char_abilities = cur.fetchall() if char_abilities > 0 else ()


        return render_template('charPage.html',
                                username=username,
                                char_id=char_id,
                                char=char,
                                char_spells=char_spells,
                                char_abilities=char_abilities)


# @app.route("/dungeonPage.html", methods=['GET'])
@app.route("/dungeonPage.html/dungeon_id=<dungeon_id>", methods=['GET'])
def dungeon_page(dungeon_id):
    """
    dungeon_page generates single item view from Dungeons table
    :param dungeon_id: the Dungeons.dungeon_id PK
    :return: render_template
    """
    print("dungeon_id =", dungeon_id)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        if dungeon_id:
            dungeon = cur.execute(sql.get_dungeon, [dungeon_id])
            dungeon = cur.fetchall()[0] if dungeon > 0 else ()
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
    """
    handles CRUD functionality for dungeon selection page
    """
    # if "username" in session:
    #     print("dungeonSelection username selected: ", session["username"])
    if request.method == "GET":
        cur = mysql.connection.cursor()

        if session["username"]:
            username = session["username"]
            curr_user_id = cur.execute(sql.get_user_id, [username])
            curr_user_id = cur.fetchall() if curr_user_id > 0 else ()
            print("curr_user_id =", curr_user_id)
            user_dungeons = cur.execute(sql.get_user_dungeons, [curr_user_id][0][0])
            user_dungeons = cur.fetchall() if user_dungeons > 0 else ()
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


# @app.route("/dungeonPage.html", methods=['GET'])
@app.route("/itemPage.html/item_id=<item_id>", methods=['GET'])
def item_page(item_id):
    """
    item_page generates single item view from Items table
    :param item_id: the Items.item_id PK
    :return: render_template
    """
    print("item_id =", item_id)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        if item_id:
            # char_list = cur.fetchall() if chars > 0 else ()
            item = cur.execute(sql.get_item, [item_id])
            cur_item = cur.fetchall()[0] if item > 0 else ()

            print("item =", cur_item)
            return render_template('itemPage.html',
                                   item=cur_item)
        else:
            cur_item = None
            return render_template('itemPage.html',
                                   item=cur_item)



@app.route("/items.html", methods=['GET', 'POST'])
def items():
    """
    items() creates the Items table view and handles INSERT of new Items
    :return:
    """
    if request.method == 'GET':
        # if "?" in request.url:
        #     print("Single item view clicked")
        #     return render_template('itemPage.html')
        cur = mysql.connection.cursor()
        items_info = cur.execute(sql.get_all_item_info)

        item_rows = cur.fetchall() if items_info > 0 else ()

        return render_template('items.html',
                               item_rows=item_rows)
    elif request.method == 'POST':
        try:
            if "insert_btn" in request.form.keys():
                item_name = request.form['Item Name']
                item_desc = request.form['Item Description']
                is_weapon = 1 if request.form['is_weapon'] == 'True' else 0
                cur = mysql.connection.cursor()
                cur.execute(sql.insert_new_item,
                            (item_name, item_desc, is_weapon))
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
    """
    item_selection handles CRUD functionality for Inventory_Items junction
    table, and relates Characters and Items tables as well
    and Dungeons table
    :return: render_template, redirect
    """
    if request.method == 'GET':

        # Logic to get the current user rows, or if no user then empty tuple ()
        cur_user_inv_table_rows = ()
        if "username" in session:
            if session["username"] is not None:
                # print("itemSelection username selected: ", session["username"])
                cur = mysql.connection.cursor()
                cur_usr = session["username"]
                # print(sql.individual_char_items % cur_usr)
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
                      f" from {request.form['character_name']}'s inventory",
                      "info")
            elif "update_btn" in request.form.keys():
                print("update clicked from inventory items panel")
                inventory_id = request.form['update_btn'].split("=").pop(-1)
                character_name = request.form['character_name']
                item_name = request.form['item_name']
                item_desc = request.form['item_description']
                item_qty = request.form['item_quantity']

                print("SQL statement to be executed:")
                query_parsed = (sql.update_inventory_items % (
                character_name, item_qty, item_name, item_desc, inventory_id))
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
                flash("Unknown POST sent to itemSelection route on Flask.",
                      "error")
            return redirect(url_for("item_selection"))
        except Exception as exc:
            print(exc)
            flash(f"Error on Item_Selection POST route: {exc}", "error")
            return redirect(url_for("item_selection"))


@app.route("/reload_the_db", methods=['POST'])
def reload_the_db():
    """
    Route to handle reload the DB being clicked on UI
    :return: Status code 202 OK, Status code 500 not OK
    """
    try:
        generate_ddl()
        flash("Database reloaded!", "success")
        return "OK!", 202
    except Exception as exc:
        print(exc)
        flash(f"Database reload error: {exc}", "error")
        return "Backend Exception on DB reload", 500


if __name__ == "__main__":
    app.run(port=app_port, debug=True)
