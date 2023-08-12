"""
    This Flask/Python file handles routes for single row views for tables:
    Characters, Dungeons, Items
    CRUD Functionality for this table implemented: SELECT
"""

import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, render_template, request, session

from db.mysql_initializer import mysql
from db import queries as sql

single_views_bp = Blueprint('single_views', __name__)

@single_views_bp.route("/charPage.html/char_id=<char_id>", methods=['GET'])
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

@single_views_bp.route("/dungeonPage.html/dungeon_id=<dungeon_id>", methods=['GET'])
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


# @app.route("/dungeonPage.html", methods=['GET'])
@single_views_bp.route("/itemPage.html/item_id=<item_id>", methods=['GET'])
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
