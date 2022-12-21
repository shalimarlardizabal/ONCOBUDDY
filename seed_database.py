import os
import json
from datetime import datetime
import requests
import urllib.parse

import crud
import model
import server

os.system('dropdb oncobuddy')
os.system('createdb oncobuddy')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/symptoms.json') as f:
    symptoms= json.loads(f.read())

symptoms_in_db= []

for symptom in symptoms:
    name, common_name = (symptom['name'], symptom['common_name'])

    db_symptom= crud.create_symptom(name, common_name)
    symptoms_in_db.append(db_symptom)

model.db.session.add_all(symptoms_in_db)
model.db.session.commit()

with open('data/conditions.json') as f:
    diagnoses= json.loads(f.read())

diagnoses_in_db= []

for diagnosis in diagnoses:
    name, common_name= (diagnosis['name'], diagnosis['common_name'])

    db_diagnosis= crud.create_diagnosis(name, common_name)
    diagnoses_in_db.append(db_diagnosis)


# def get_drug_name():

#     url= 

