"""
    This Flask/Python file handles route for "Items" table in the DB.
    CRUD Functionality for this table implemented: SELECT, INSERT
"""
import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, \
    render_template, request, redirect, url_for, \
    flash
from db.mysql_initializer import mysql
from db import queries as sql
from functions import flash_err

items_bp = Blueprint('items', __name__)


@items_bp.route("/items.html", methods=['GET', 'POST'])
def items():
    """
    items() creates the Items table view and handles INSERT of new Items
    :return: render_template or redirect(url_for())
    """
    try:
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            items_info = cur.execute(sql.get_all_item_info)
            item_rows = cur.fetchall() if items_info > 0 else ()
            return render_template('items.html',
                                   item_rows=item_rows)
        elif request.method == 'POST':
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
            # Explain below 'items.items': first items is items.py,
            # second items is the function items()
            return redirect(url_for("items.items"))  # full page reload
        else:
            flash("route /items.html only accepts GET or POST requests",
                  "error")
            return "route /items.html only accepts GET or POST requests", 505
    except Exception as exc:
        flash_err(exc)
        return redirect(url_for("items.items"))
