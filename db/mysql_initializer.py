'''
Separate out the mysql connection so that it can be imported in both ../app.py
and the .py files in ../routes directory.
This prevents circular import error if it were to be initialized in app.py
https://stackoverflow.com/questions/28784849/how-to-fix-circular-import-in-flask-project-using-blueprints-mysql-w-o-sqlalchem
'''

from flask_mysqldb import MySQL

mysql = MySQL()
