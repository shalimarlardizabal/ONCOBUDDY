"""OncoBuddy Server by Shalimar Lardizabal"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import requests
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
    # print(f'email {email}')

    user = crud.get_user_by_email(email)
    # print(f'user {user}')

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
    user_name = request.form.get("name")
    age = request.form.get("age")
    sex = request.form.get("sex")

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Account with that email already exists. Please log in.")
    else:
        user = crud.create_user(email, password, user_name, age, sex)
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

    cancer_types= crud.get_oncologic_diagnoses()
    conditions = crud.get_diagnoses()
    drugs= crud.show_all_drugs()

    cancer_diagnosis_id= request.args.get("cancer-type")
    other_diagnosis_id= request.args.get("other-conditions")
    drug_id= request.args.get("user-medications")
    
    cancer_diagnosis= crud.get_diagnosis_by_id(cancer_diagnosis_id)

    if cancer_diagnosis:
        diagnosis_name= cancer_diagnosis.name
        user_cancer_diagnosis= crud.add_user_diagnosis(user_id, cancer_diagnosis_id, diagnosis_name)
        db.session.add(user_cancer_diagnosis)
        db.session.commit()

    other_diagnosis= crud.get_diagnosis_by_id(other_diagnosis_id)
    
    if other_diagnosis:
        diagnosis_name= other_diagnosis.name
        user_diagnosis=crud.add_user_diagnosis(user_id, other_diagnosis_id, diagnosis_name)
        db.session.add(user_diagnosis)
        db.session.commit()
  
    drug = crud.get_drug_by_id(drug_id)
    
    if drug:
        drug_name= drug.name
        user_drug= crud.add_user_drug(user_id, drug_id, drug_name)
        db.session.add(user_drug)
        db.session.commit()

    return render_template('welcomepage.html', user = user, cancer_types=cancer_types, conditions=conditions, drugs= drugs)

@app.route("/profile")
def show_daily_questionnaire():
    """Shows page with daily questionnaire"""

    user_id= session["user_id"]
    user= crud.get_user_by_id(user_id)

    symptoms = crud.get_symptoms()
    medications= crud.get_user_drugs(user_id)
    pain= crud.get_pain_symptoms()

    pain_level= request.args.get("pain")
    pain_location_id= request.args.get("pain-location")
    fatigue_level= request.args.get("fatigue")
    sleep_level= request.args.get("sleep")
    appetite_level= request.args.get("appetite")
    symptom_id= request.args.get("daily-symptoms")
    date= request.args.get("date")

    if symptom_id:
        symptom_name= symptom_id.name
        symptom_log= crud.add_user_symptom(user_id, symptom_id, symptom_name, pain_level, pain_location_id, sleep_level, fatigue_level, appetite_level, date)
        db.session.add(symptom_log)
        db.session.commit()

    return render_template("userpage.html", user=user, symptoms= symptoms, medications=medications, pain=pain)


@app.route('/profile/<user_id>')
def show_user_page(user_id):
    """Show user's page"""
    
    user_id= session["user_id"]
    user= crud.get_user_by_id(user_id)

    medications= crud.get_user_drugs(user_id)

    return render_template("user_details.html", user = user, medications=medications)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)