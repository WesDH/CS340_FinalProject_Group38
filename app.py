"""
-- CS340 Final Project, Summer 2023: Dungeons and Dragons Character Manager
-- GROUP 38: Joseph Houghton, Lauren Norman Schueneman, Wesley Havens
--
-- App.py is the logic for handling DB and UI interactions via routes with Flask
"""
#import sys
from flask import Flask
#render_template, request, redirect, url_for, flash, session
#from flask_mysqldb import MySQL
from env.credentials import *
#from db import queries as sql
from datetime import timedelta
from functions import generate_ddl

# Route imports:
import routes.characters
import routes.dungeons
import routes.items
import routes.reload_db
import routes.single_views
import routes.spells_abilities
import routes.users
import routes.inventory

# Separate out MySQL connector so that python files in routes can import it too
from db.mysql_initializer import mysql

app = Flask(__name__)

APP_PORT = 19807

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

# Initialize MySQL connector from mysql_initializer.py
mysql.init_app(app)

# Load in the route Blueprints:
app.register_blueprint(routes.characters.characters_bp)
app.register_blueprint(routes.dungeons.dungeons_bp)
app.register_blueprint(routes.items.items_bp)
app.register_blueprint(routes.inventory.inventory_bp)
app.register_blueprint(routes.reload_db.reload_database_bp)
app.register_blueprint(routes.users.users_bp)
app.register_blueprint(routes.single_views.single_views_bp)
app.register_blueprint(routes.spells_abilities.spells_abilities_bp)

# Populate the DB once on startup:
with app.app_context():
    # Comment generate_ddl() during development to save some time:
    #generate_ddl()
    pass

if __name__ == "__main__":
    app.run(port=APP_PORT, debug=True)
