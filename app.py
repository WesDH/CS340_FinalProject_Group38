"""
    Starter flask app to define primary routes.
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from env.credentials import *

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
        print("Statement ran: {}".format(statement))


# Populate the DB once on startup, for now, like this:
# ddbtest.sql is as single line of the schema as .execute only
# Executes one line per execute.
with app.app_context():
    generate_ddl()  # Comment this during development to save some time

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/itemSelection.html", methods=['GET', 'POST'])
def item_selection():
    return render_template('itemSelection.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
