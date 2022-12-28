import os
import json
from datetime import datetime
import requests
import urllib.parse
from bs4 import BeautifulSoup

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

model.db.session.add_all(diagnoses_in_db)
model.db.session.commit()


url = "https://www.cancerresearchuk.org/about-cancer/cancer-in-general/treatment/cancer-drugs/drugs"
data= requests.get(url)

drugs_in_db=[]
html= BeautifulSoup(data.text, 'html.parser')

links= html.select('.child-index-item')

for link in links:
    link_url= [a['href'] for a in link.select('a[href]')]
    medication_name= link.select('a')[0].get_text()
    content_url= link_url[0]
    # content= requests.get(content_url)
    # soup = BeautifulSoup(data.text, 'html.parser')
    # description = soup.get_text()
    
    db_drugs= crud.create_drugs(medication_name, content_url)
    drugs_in_db.append(db_drugs)

model.db.session.add_all(drugs_in_db)
model.db.session.commit()


