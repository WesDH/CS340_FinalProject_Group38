"""
-- CS340 Final Project, Summer 2023: Dungeons and Dragons Character Manager
-- GROUP 38: Joseph Houghton, Lauren Norman Schueneman, Wesley Havens
--
-- App.py is the logic for handling DB and UI interactions via routes with Flask

References:
    Citation for:
-   General usage and understanding throughout the project:
-   Routes/Jinja templating
Scope: Module
Date: June 26th-August 5th, 2023
Accessed by: Havensw, Houghtjo
Adapted from:
-   Source Title: osu-cs340-ecampus / flask-starter-app
-   Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app#setup

Citation for:
-  Using sessions to save a username for personalized view
-  Using Flask flash() functionality to send feedback to the UI
Scope: Module
Date Accessed: July 22nd, 2023
Accessed by: Havensw, Houghtjo
Adapted from:
-   Source Title: Flask Tutorials
-   Source URL: https://www.youtube.com/playlist?list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX

Citation for:
-  Flask Blueprinting
Scope: Module
Accessed by: Havensw
Date Accessed: August 11th, 2023
Modified from:
-   Source URL: https://flask.palletsprojects.com/en/2.3.x/blueprints/
"""
from flask import Flask
from env.credentials import *
from datetime import timedelta

# Route imports:
import routes.characters
import routes.dungeons
import routes.items
import routes.reload_db
import routes.single_views
import routes.spells_abilities
import routes.users
import routes.inventory

APP_PORT = 19806

# Separate out MySQL connector so that python files in routes can import it too
from db.mysql_initializer import mysql

app = Flask(__name__)

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
