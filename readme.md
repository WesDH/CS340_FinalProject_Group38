# CS340 Intro to Databases : Summer 2023 Final Project
## Team 38
### Dungeons & Dragons Character Management System

### Team Members:<br>
Lauren Norman Schueneman<br>
Joseph Houghton<br>
Wesley Havens<br><br>

### Tech stack utilized:<br>
Flask/MySQL/HTML/CSS/Javascript<br><br>

### How to start the Flask server:<br>

Copy all project files to a working directory.
<br><br>
Next, define environment variables by creating ```/env/credentials.py``` in the working directory.<br>
Place these environment variable definitions into this file:<br>
```
ENV_HOST = 'your_mysql_host'
ENV_USERNAME = 'your_mysql_username'
ENV_PASSWORD = 'your_mysql_password'
ENV_DATABASE = 'your_mysql_database'
session_key = '_any_string'
```
Where above:<br>
Variables "your_mysql_" are custom defined and depend on your database credentials<br>
Variable session_key can be set to <i>any</i> string value<br>
<br>
<br>
Set global variable ```APP_PORT``` within app.py to the port you would like app.py to run on.
<br>
Default: ```APP_PORT = 19806```
<br>
<br>
Next, from the base project directory, run these commands to start the Flask server:
```
$ pip3 install --user virtualenv
$ python3 -m venv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python app.py
```
<br>

### Sources Cited:
<br>
Citation for:<br>
- &emsp; General usage and understanding throughout the project:<br>
- &emsp; Routes/Jinja templating<br>
Scope: Module<br>
Date: June 26th-August 5th, 2023<br>
Accessed by: Havensw, Houghtjo<br>
Adapted from:<br>
- &emsp; Source Title: osu-cs340-ecampus / flask-starter-app<br>
- &emsp; Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app#setup
<br>
<br>
Citation for:<br>
- &emsp;Using sessions to save a username for personalized view<br>
- &emsp;Using Flask flash() functionality to send feedback to the UI<br>
Scope: Module<br>
Date Accessed: July 22nd, 2023<br>
Accessed by: Havensw, Houghtjo<br>
Adapted from:<br>
- &emsp; Source Title: Flask Tutorials<br>
- &emsp; Source URL: https://www.youtube.com/playlist?list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX
<br>
<br>
Citation for:<br>
- &emsp;Using Flask flash() messages with categories<br>
Scope: Function<br>
Date Accessed: July 22nd, 2023<br>
Copied with modifications by: Havensw<br>
Adapted from:<br>
- &emsp; Source Title: Message Flashing<br>
- &emsp; Source URL: https://flask.palletsprojects.com/en/2.3.x/patterns/flashing/
<br>
<br>
Citation for:<br>
- &emsp;Better understanding for how to: SELECT from DB to display table to UX<br>
- &emsp;and INSERT to add row from UX into the DB<br>
Scope: Module<br>
Date Accessed: July 22nd, 2023<br>
Accessed by: Havensw, Houghtjo<br>
Adapted from:<br>
- &emsp; Source Title: Python Flask MySQL Database Example<br>
- &emsp; Source URL: https://www.youtube.com/watch?v=7r93l-sRmwI
<br>
<br>
Citation for:<br>
- &emsp;Javascript FETCH request syntax<br>
Scope: Function<br>
Date Accessed: July 27th, 2023<br>
Accessed by: Havensw<br>
Modified from previous CS290 final project Javascript source:<br>
- &emsp; Source Title: CRUDapp<br>
- &emsp; Source URL: http://weshavens.info/CRUDapp/
<br>
<br>
Citation for:<br>
- &emsp;Custom Google MDL CSS styling attributes applied throughout our HTML Pages<br>
Scope: Module<br>
Date Accessed: July 22nd-July 31st, 2023<br>
Accessed by: Havensw<br>
Adapted from component examples (Tables, Cards, Navbar, Inputs):<br>
- &emsp; Source URL: https://getmdl.io/components/
<br>
<br>
Citation for:<br>
- &emsp;MDL styling fix for MDL Icon Graphics<br>
Scope: Line<br>
Date Accessed: July 25th, 2023<br>
Accessed by: Havensw<br>
Adapted from solution:<br>
- &emsp; Source URL: https://github.com/angular/material/issues/3776
<br>
<br>
Citation for:<br>
- &emsp;MDL styling fix for database reload Icon with text<br>
Scope: Line<br>
Accessed by: Havensw<br>
Date Accessed: July 25th, 2023<br>
Copied from solution:<br>
- &emsp; Source URL: https://stackoverflow.com/questions/39907145/align-material-icon-with-text-on-materialize
<br>
<br>
Citation for:<br>
- &emsp;Flask Blueprinting<br>
Scope: Module<br>
Accessed by: Havensw<br>
Date Accessed: August 11th, 2023<br>
Modified from:<br>
- &emsp; Source URL: https://flask.palletsprojects.com/en/2.3.x/blueprints/
<br>
<br>
Citation for:<br>
- &emsp;How to import from parent directory "../" in Python<br>
Scope: Line<br>
Accessed by: Havensw<br>
Date Accessed: August 6th, 2023<br>
Copied from answer by user Jenish:<br>
- &emsp; Source URL: https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
<br>
<br>
Citation for:<br>
- &emsp;How to fix circular import statements in Flask/Python with Blueprints<br>
Scope: Line<br>
Accessed by: Havensw<br>
Date Accessed: August 6th, 2023<br>
Copied from answer by Robert Moskal:<br>
- &emsp; Source URL: https://stackoverflow.com/questions/28784849/how-to-fix-circular-import-in-flask-project-using-blueprints-mysql-w-o-sqlalchem
<br>
<br>
Citation for:<br>
- &emsp;Favicon icon<br>
Scope: Line<br>
Accessed by: Havensw<br>
Date Accessed: August 11th, 2023<br>
Downloaded from:<br>
- &emsp; Source URL: https://www.flaticon.com/packs/yokai-8?word=character
