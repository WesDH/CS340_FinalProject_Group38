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
Set global variable ```app_port``` within app.py to the port you would like app.py to run on.
<br>
Default: ```app_port = 19806```
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
&emsp; General usage and understanding throughout the project:<br>
&emsp; Routes/Jinja templating<br>
Date: June 26th-August 5th, 2023<br>
Adapted from:<br>
&emsp; Source Title: osu-cs340-ecampus / flask-starter-app<br>
&emsp; Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app#setup
<br>
<br>
Citation for:<br>
&emsp;Using sessions to save a username for personalized view<br>
&emsp;Using Flask flash() functionality to send feedback to the UI<br>
Date Accessed: July 22nd, 2023<br>
Adapted from:<br>
&emsp; Source Title: Flask Tutorials<br>
&emsp; Source URL: https://www.youtube.com/playlist?list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX
<br>
<br>
Citation for:<br>
&emsp;Better understanding for how to: SELECT from db to display to UX<br>
&emsp;and INSERT to insert from UX into DB<br>
Date Accessed: July 22nd, 2023<br>
Adapted from:<br>
&emsp; Source Title: Python Flask MySQL Database Example<br>
&emsp; Source URL: https://www.youtube.com/watch?v=7r93l-sRmwI
<br>
<br>
Citation for:<br>
&emsp;Javascript FETCH request syntax<br>
Date Accessed: July 27th, 2023<br>
Copied from previous CS290 final project:<br>
&emsp; Source Title: CRUDapp<br>
&emsp; Source URL: http://weshavens.info/CRUDapp/