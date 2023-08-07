import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, session
from db.mysql_initializer import mysql
from db import queries as sql
from functions import flash_err

spells_abilities_bp = Blueprint('spells_abilities', __name__)


@spells_abilities_bp.route("/spells_abilities.html", methods=['GET', 'POST'])
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

            user_abilities = cur.execute(sql.get_user_abilities,
                                         [curr_user_id][0][0])
            if user_abilities > 0:
                user_abilities = cur.fetchall()
                user_abilities_list = []
                for ability in user_abilities:
                    ability = list(ability)
                    # print(ability)
                    if ability[3]:
                        # this ability has a dungeon_id
                        dungeon_name = cur.execute(sql.get_ability_dungeon,
                                                   [ability[3]])
                        dungeon_name = cur.fetchall()[0][0]
                        ability[3] = dungeon_name
                    else:
                        # this ability does NOT have a dungeon_id
                        ability[3] = "No Dungeon"
                    # print(ability)
                    user_abilities_list.append(ability)

            else:
                user_abilities_list = ()

            user_spells = cur.execute(sql.get_user_spells,
                                      [curr_user_id][0][0])
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
                        dungeon_name = cur.execute(sql.get_ability_dungeon,
                                                   [ability[3]])
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
            return redirect(url_for("users.index"))


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
                        dungeon_name = cur.execute(sql.get_ability_dungeon,
                                                   [ability[3]])
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
            return redirect(url_for("users.index"))

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
                    cur.execute(
                        "INSERT INTO Abilities (ability_name, ability_damage, Dungeons_dungeon_id) VALUES (%s, %s, %s);",
                        (ability_name, ability_damage, None))
                else:
                    cur.execute(sql.add_ability, (
                    ability_name, ability_damage, ability_dungeon_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row inserted for Abilities: {ability_name}", "info")
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))

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
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))


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
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))


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
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))

        elif request.form['button_press'][0:4] == "dela":
            print("Ability DELETE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_id = request.form['button_press'][4:]
                cur.execute(sql.delete_ability, [ability_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row Deleted for Abilities", "info")
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))

        elif request.form['button_press'][0:2] == "a#":
            print(
                "Characters_has_Abilities DELETE was clicked on spells/abilities page")
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
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))

        elif request.form['button_press'][0:4] == "upda":
            print("Ability UPDATE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                ability_id = request.form['button_press'][4:]
                ability_name = request.form['ability_name']
                ability_damage = request.form['ability_damage']
                ability_dungeon_id = request.form['ability_dungeon']
                print(ability_name, ability_damage, ability_dungeon_id,
                      ability_id)
                if ability_dungeon_id == "No Dungeon":
                    cur.execute(
                        "UPDATE Abilities SET ability_name = %s, ability_damage = %s, Dungeons_dungeon_id = %s WHERE ability_id = %s;",
                        (ability_name, ability_damage, None, ability_id))
                else:
                    cur.execute(sql.update_ability, (
                    ability_name, ability_damage, ability_dungeon_id,
                    ability_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row Updated for Abilities", "info")
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))


        elif request.form['button_press'][0:4] == "dels":
            print("Spell DELETE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_id = request.form['button_press'][4:]
                cur.execute(sql.delete_spell, [spell_id])
                mysql.connection.commit()
                cur.close()
                flash(f"Row Deleted for Spells", "info")
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))

        elif request.form['button_press'][0:2] == "s#":
            print(
                "Characters_has_Spells DELETE was clicked on spells/abilities page")
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
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))

        elif request.form['button_press'][0:4] == "upds":
            print("Spell UPDATE was clicked on spells/abilities page")
            try:
                cur = mysql.connection.cursor()
                spell_id = request.form['button_press'][4:]
                spell_name = request.form['spell_name']
                spell_damage = request.form['spell_damage']
                print(spell_name, spell_damage, spell_id)
                cur.execute(sql.update_spell,
                            (spell_name, spell_damage, spell_id))
                mysql.connection.commit()
                cur.close()
                flash(f"Row Updated for Spells", "info")
                return redirect(url_for("spells_abilities.spells_abilities_page"))
            except Exception as exc:
                print(exc)
                flash_err(exc)
                return redirect(url_for("spells_abilities.spells_abilities_page"))