"""OncoBuddy Server by Shalimar Lardizabal"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View Homepage"""

    return render_template('homepage.html')

@app.route("/users", methods= ["POST"])
def user_login():
    """User login"""

    email = request.form.get("email")
    password = request.form.get("password")
    print(f'email {email}')

    user = crud.get_user_by_email(email)
    print(f'user {user}')

    if not user or user.password != password:
        flash ('Incorrect email or password')
        return redirect('/')

    elif user.email == email or user.password == password:
        session["name"] = user.user_name
        session["user_id"] = user.user_id

        flash(f"Welcome back, {user.user_name}")

        return render_template('userpage.html', user= user)

@app.route("/createaccount")
def creat_account():
    """View create account"""

    return render_template('createaccount.html')

@app.route("/createaccount", methods= ["POST"])
def create_account():
    """Create account for user"""

    email = request.form.get("email")
    password = request.form.get("password")
    user_name= request.form.get("username")

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Account with that email already exists. Please log in.")
    else:
        user = crud.create_user(email, password, user_name)
        db.session.add(user)
        db.session.commit()

        session["name"] = user.user_name
        session["user_id"] = user.user_id
        
        flash("Account successfully created!")

        return redirect("/intake")

@app.route("/intake")
def show_intake_form():
    """User intake when account first created"""

    user_id= session["user_id"]
    user= crud.get_user_by_id(user_id)

    return render_template('welcomepage.html', user = user)

@app.route("/profile")
def show_daily_questionnaire():
    """Shows page with daily questionnaire"""

    user_id= session["user_id"]
    user= crud.get_user_by_id(user_id)

    return render_template("userpage.html", user=user)


@app.route('/profile/<user_id>')
def show_user_page(user_id):
    """Show user's page"""
    
    user_id= session["user_id"]
    user= crud.get_user_by_id(user_id)

    return render_template("user_details.html", user = user )


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)