"""OncoBuddy Server by Shalimar Lardizabal"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import requests
import crud
from jinja2 import StrictUndefined
from datetime import datetime
from bs4 import BeautifulSoup

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

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash ('Incorrect email or password!')
        return redirect('/')

    elif user.email == email or user.password == password:
        session["name"] = user.user_name
        session["user_id"] = user.user_id

        flash(f"Welcome back {user.user_name}! How are you feeling today?")

        return redirect("/dailylog")

@app.route("/logout")
def logout():
    """logout user"""

    del session["name"]
    del session["user_id"]

    return redirect("/")

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

    cancer_types= crud.show_all_cancer()
    conditions = crud.get_diagnoses()
    drugs= crud.show_all_drugs()

    cancer_id= request.args.get("cancer-type")
    other_diagnosis_id= request.args.get("other-conditions")
    drug_id= request.args.get("user-medications")
    
    cancer_diagnosis= crud.get_cancer_by_id(cancer_id)

    if cancer_diagnosis:
        flash(f'You have entered {cancer_diagnosis.name} as your diagnosis.')
        cancer_name= cancer_diagnosis.name
        user_cancer_diagnosis= crud.add_user_cancer(user_id, cancer_id, cancer_name)
        db.session.add(user_cancer_diagnosis)
        db.session.commit()

    other_diagnosis= crud.get_diagnosis_by_id(other_diagnosis_id)
    
    if other_diagnosis:
        flash(f'Successfully added {other_diagnosis.name}!')
        diagnosis_name= other_diagnosis.name
        user_diagnosis=crud.add_user_diagnosis(user_id, other_diagnosis_id, diagnosis_name)
        db.session.add(user_diagnosis)
        db.session.commit()
  
    drug = crud.get_drug_by_id(drug_id)
    
    if drug:
        flash(f'You have added {drug.name} as your treatment.')
        drug_name= drug.name
        user_drug= crud.add_user_drug(user_id, drug_id, drug_name)
        db.session.add(user_drug)
        db.session.commit()

    return render_template('welcomepage.html', user = user, cancer_types=cancer_types, conditions=conditions, drugs= drugs)

@app.route("/dailylog")
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
    date= datetime.now()
    
    if pain_level:
        db_daily_log= crud.add_user_daily_log(user_id, pain_level, pain_location_id, sleep_level, fatigue_level, appetite_level, date)
        db.session.add(db_daily_log)
        db.session.commit()
    
    if symptom_id:
        symptom= crud.get_symptom_by_id(symptom_id)
        symptom_name= symptom.common_name
        symptom_in_db= crud.add_user_symptom(user_id, symptom_id, symptom_name, date)
        db.session.add(symptom_in_db)
        db.session.commit()
    
    user_drug_id= request.args.get("administered-medications")
    
    if user_drug_id:
        date= datetime.now()
        drug= crud.get_user_drugs_by_id(user_drug_id)
        drug_name= drug.drug_name
        administered_medications=crud.add_administered_drug(user_drug_id, drug_name, date)
        db.session.add(administered_medications)
        db.session.commit()

    return render_template("dailylog.html", user=user, symptoms= symptoms, medications=medications, pain=pain)


@app.route('/profile/<user_id>')
def show_user_page(user_id):
    """Show user's page"""
    
    user_id= session["user_id"]
    user= crud.get_user_by_id(user_id)

    medications= crud.get_all_user_drugs(user_id) 
    cancer= crud.get_user_cancer(user_id)
    administered_drugs= crud.get_administered_drug(user_id)
    
    for drugs in administered_drugs:
        drugs['start']=drugs['start'].date()
    
    symptoms= crud.get_user_symptom_with_date(user_id)
    for symptom in symptoms:
        symptom['start']= symptom['start'].date()


    for element in cancer:
        url= element['description']+ '/about'
        data= requests.get(url)
        html= BeautifulSoup(data.text, 'html.parser')
        content= html.select('.region-content')

    user_medication=[]

    for element in medications:
        name = element['drug_name']
        url= element['description']
        data= requests.get(url)
        html= BeautifulSoup(data.text, 'html.parser')
        med_content= html.select('.region-content')
        user_medication.append((name, med_content[0]))
    
    
    return render_template("user_details.html", user = user, medications=medications, symptoms=symptoms, cancer=cancer, content=content, user_medication=user_medication, administered_drugs=administered_drugs)


@app.route('/logs.json')
def get_daily_log():
    """Get daily log as json"""

    user_id= session["user_id"]
    pain_log= crud.get_painlog_by_user(user_id)
    sleep_log= crud.get_sleeplog_by_user(user_id)
    appetite_log= crud.get_appetitelog_by_user(user_id)
    fatigue_log= crud.get_fatiguelog_by_user(user_id)

    pain_log_data=[]
    sleep_log_data=[]
    appetite_log_data=[]
    fatigue_log_data=[]

    for log in pain_log:
        date= log[1]
        pain_log_data.append({'pain_level':log[0],'date': date.isoformat()})
    
    for log in sleep_log:
        date= log[1]
        sleep_log_data.append({'sleep_level':log[0], 'date': date.isoformat()})

    for log in appetite_log:
        date= log[1]
        appetite_log_data.append({'appetite_level':log[0], 'date': date.isoformat()})
    
    for log in fatigue_log:
        date= log[1]
        fatigue_log_data.append({'fatigue_level': log[0], 'date': date.isoformat()})

    return jsonify({'pain_data': pain_log_data, 'sleep_data': sleep_log_data, 'appetite_data': appetite_log_data, 'fatigue_data': fatigue_log_data})


@app.route('/calendar')
def show_user_calendar():
    user_id= session["user_id"]
    symptoms= crud.get_user_symptom_with_date(user_id)
    treatments= crud.get_user_drugs(user_id)
    user= crud.get_user_by_id(user_id)

    return render_template('calendar.html', treatments= treatments, symptoms=symptoms, user=user)

@app.route('/symptoms.json')
def add_events_to_calendar():
    user_id= session["user_id"]
    symptoms=crud.get_user_symptom_with_date(user_id)
    for symptom in symptoms:
        symptom['start']=symptom['start'].isoformat()
    
    administered_drugs=crud.get_administered_drug(user_id)

    for drug in administered_drugs:
        drug['start']= drug['start'].isoformat()
    
    return jsonify({'symptoms': symptoms, 'administered_drugs': administered_drugs})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)