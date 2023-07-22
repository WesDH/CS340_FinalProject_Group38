"""
    Starter flask app to define primary routes.
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from env.credentials import *
import queries as sql

app = Flask(__name__)

app.config['MYSQL_HOST'] = ENV_HOST
app.config['MYSQL_USER'] = ENV_USERNAME
app.config['MYSQL_PASSWORD'] = ENV_PASSWORD
app.config['MYSQL_DB'] = ENV_DATABASE

mysql = MySQL(app)


def generate_ddl():
    """
        Executes DB Schema
        Drops all tables and recreates default DB with sample data
    :return: None
    """
    schema = open('db/ddbtest.sql', mode='r')
    for statement in schema.readlines():
        statement = statement.rstrip()
        cur = mysql.connection.cursor()
        cur.execute(statement)
        mysql.connection.commit()
        cur.close()
        print(statement)


# Populate the DB once on startup, for now, like this:
# ddbtest.sql is as single line of the schema as .execute only
# Executes one line per execute.
with app.app_context():
    generate_ddl()  # Comment this during development to save some time
    #pass


@app.route("/logout", methods=['GET'])
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/Items.html", methods=['GET', 'POST'])
def items():
    cur = mysql.connection.cursor()
    items_info = cur.execute(sql.get_all_item_info)
    if items_info > 0:
        item_rows = cur.fetchall()

    return render_template('Items.html',
                           item_rows=item_rows)

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
