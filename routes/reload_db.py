import sys
sys.path.append("..")  # Add parent directory sys.path for imports
from flask import Blueprint, flash
from functions import generate_ddl

reload_database_bp = Blueprint('reload_the_db', __name__)

@reload_database_bp.route("/reload_the_db", methods=['POST'])
def reload_the_db():
    """
    Route to handle reload the DB being clicked on UI
    :return: Status code 202 OK, Status code 500 not OK
    """
    try:
        generate_ddl()
        flash("Database reloaded!", "success")
        return "OK!", 202
    except Exception as exc:
        print(exc)
        flash(f"Database reload error: {exc}", "error")
        return "Backend Exception on DB reload", 500
