"""
    This Flask/Python file handles route for "Inventory_Items"
    junction table in the DB.
    CRUD Functionality for this table implemented: Full CRUD
    Also has functionality of NULL'able FK: Inventory_Items.Items_item_id
"""
import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, \
    render_template, request, redirect, url_for, \
    flash, session
from db.mysql_initializer import mysql
from db import queries as sql

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route("/itemSelection.html", methods=['GET', 'POST'])
def item_selection():
    """
    Function item_selection() handles CRUD functionality for Inventory_Items
    junction table, and also relates Characters and Items tables
    :return: render_template, redirect(url_for())
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
                # First query is logic to create a NULL'able FK,
                # Set Inventory_Items.Items_item_id = NULL if the user requests:
                if item_name.lower() == "none" or item_name.lower() == "null":
                    query_parsed = (sql.update_inv_items_null % (
                    character_name, item_qty, inventory_id))
                # Otherwise do a standard update query:
                else:
                    query_parsed = (sql.update_inventory_items % (
                    character_name, item_qty, item_name, item_desc, inventory_id))
                print(query_parsed)
                cur = mysql.connection.cursor()
                rows_affect = cur.execute(query_parsed)
                mysql.connection.commit()
                cur.close()

                # If the query affected zero rows, that means the relationship
                # with Items table doesn't exist. This means that
                # Items_items_id FK must be set to NULL:
                if not rows_affect:
                    flash(f"Item name/description can no longer be UPDATED as " 
                          f"the relationship no longer exists. Try deleting row instead.",
                          "error")
                # else we may have updated with a NULLable FK request:
                elif item_name.lower() == "none" or item_name.lower() == "null":
                    flash(f"Update Char {request.form['character_name']}"
                          f" SET Inventory_Items.Items_item_id=NULL", "info")
                # All other cases means a standard UPDATE request
                else:
                    flash(f"Update {request.form['character_name']}"
                          f" with {request.form['item_quantity']}"
                          f" of {request.form['item_name']}"
                          f": \"{request.form['item_description']}\"", "info")

            # Logic to insert a new item and quantity into a char's inventory:
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
            return redirect(url_for("inventory.item_selection"))
        except Exception as exc:
            print(exc)
            flash(f"Error on Item_Selection POST route: {exc}", "error")
            return redirect(url_for("inventory.item_selection"))
