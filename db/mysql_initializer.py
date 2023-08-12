"""
Separate out the mysql connection so that it can be imported in both ../app.py
and the .py files in ../routes directory.
This prevents circular import error if it were to be initialized in app.py

Citation for:
- How to fix circular import statements in Flask/Python with Blueprints
Scope: Line
Accessed by: Havensw
Date Accessed: August 6th, 2023
Copied from answer by Robert Moskal:
- Source URL:
https://stackoverflow.com/questions/28784849/how-to-fix-circular-import-in-flask-project-using-blueprints-mysql-w-o-sqlalchem
"""

from flask_mysqldb import MySQL

mysql = MySQL()  # Now mysql can be imported by app.py and any other .py files
