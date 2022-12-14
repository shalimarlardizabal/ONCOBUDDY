"""OncoBuddy Server by Shalimar Lardizabal"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View Homepage"""

    return render_template('homepage.html')

@app.route("/users", methods = ["POST"])
def userlogin():
    """User login"""

    email = request.form.get("email")
    password = request.form.get("password")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)