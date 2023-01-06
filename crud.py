"""OncoBuddy CRUD operations"""
from model import connect_to_db, db, User, UserSymptom, UserAdministeredDrug, UserDrug, UserDiagnosis, Diagnosis, Symptom, Drug, UserDailyLog

def create_user(email, password, user_name):
    """create and return a new user"""
    user = User(email= email, password=password, user_name= user_name)

    return user

def get_user_by_email(email):
    """Shows users email"""
    return User.query.filter_by(email = email).first()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def create_symptom(name, common_name):
    """Populate each symptom"""
    symptom= Symptom(name=name, common_name=common_name)

    return symptom

def get_symptoms():
    """Return all symptoms"""

    return Symptom.query.all()

def get_symptoms_by_common_name(common_name):

    return Symptom.query.get(common_name)

def create_diagnosis(name, common_name):
    """populate each diagnosis"""
    diagnosis= Diagnosis(name=name, common_name=common_name)

    return diagnosis

def get_diagnoses():
    """Return all conditions"""

    return Diagnosis.query.all()

def get_oncologic_diagnoses():

    return Diagnosis.query.filter(Diagnosis.common_name.contains('cancer')).all()

def get_diagnosis_by_id(diagnosis_id):

    return Diagnosis.query.get(diagnosis_id)


def get_diagnosis_by_common_name(common_name):

    return Diagnosis.query.get(common_name)

def add_user_diagnosis(user_id, diagnosis_id, diagnosis_name):
    
    user_diagnosis = UserDiagnosis(user_id= user_id, diagnosis_id=diagnosis_id, diagnosis_name= diagnosis_name)
    
    return user_diagnosis

def get_symptom_by_id(symptom_id):

    return Symptom.query.get(symptom_id)

def add_user_symptom(user_id, symptom_id, symptom_name, date):
    user_symptom= UserSymptom(user_id=user_id, symptom_id=symptom_id, symptom_name=symptom_name,  date=date)

    return user_symptom

def add_user_daily_log(user_id, pain_level,pain_location_id, sleep_level, fatigue_level, appetite_level, date):

    user_daily_log= UserDailyLog(user_id=user_id, pain_level=pain_level, pain_location_id=pain_location_id, sleep_level=sleep_level, fatigue_level=fatigue_level, appetite_level=appetite_level, date=date)

    return user_daily_log

def get_pain_symptoms():
    return Symptom.query.filter(Symptom.common_name.contains('pain')).all()

def add_user_drug(user_id, drug_id, drug_name):
    
    user_drug= UserDrug(user_id= user_id, drug_id= drug_id, drug_name=drug_name)

    return user_drug

def add_user_administered_drug(user_drug_id, drug_name, administration_date):
    user_administered_drug= UserAdministeredDrug(user_drug_id=user_drug_id, drug_name=drug_name, administration_date=administration_date)
    return user_administered_drug

def create_drugs(name, description):

    drug= Drug(name=name, description= description)

    return drug

def show_all_drugs():
    
    return Drug.query.all()

def get_drug_by_id(drug_id):
    return Drug.query.get(drug_id)

def get_drug_by_name(name):

    return Drug.query.get(name)

def get_all_user_drugs(user_id):
    user= User.query.get(user_id)
    user_drug= user.drugs

    user_drugs=[]
    
    for drug in user_drug:
        user_drugs.append({'drug_name': drug.name, 'description': drug.description})
    
    return user_drugs

def get_user_drugs(user_id):
    
    return UserDrug.query.filter(UserDrug.user_id==user_id).all()

def get_user_drugs_by_id(user_drug_id):
    return UserDrug.query.filter(UserDrug.user_drug_id==user_drug_id).first()

def get_user_symptoms(user_id):
    return UserSymptom.query.filter(UserSymptom.user_id==user_id).all()

def get_user_symptom_with_date(user_id):
    symptoms= UserSymptom.query.filter(UserSymptom.user_id==user_id)
    symptom_date=[]

    for symptom in symptoms:
        symptom_date.append({'symptom':symptom.symptom_name, 'date': symptom.date})
    
    return symptom_date
    
def add_user_drugs(user_id, drug_id, drug_name):

    user_drug= UserDrug(user_id, drug_id, drug_name)

    return user_drug

def add_administered_drug(user_drug_id, drug_name, administration_date):

    administered_drug= UserAdministeredDrug(user_drug_id=user_drug_id, drug_name=drug_name, administration_date=administration_date)
    
    return administered_drug

def get_painlog_by_user(user_id):
    """Get all pain log by user"""
    pain_level=[]
    date=[]

    dailylogs= UserDailyLog.query.filter_by(user_id=user_id).all()

    for user in dailylogs:
        pain_level.append(user.pain_level)
        date.append(user.date)

    pain_log= zip(pain_level, date)

    return pain_log

def get_sleeplog_by_user(user_id):
    """Gett all sleep log by user"""
    sleep_level=[]
    date=[]

    dailylogs= UserDailyLog.query.filter_by(user_id=user_id).all()

    for user in dailylogs:
        sleep_level.append(user.sleep_level)
        date.append(user.date)

    sleep_log= zip(sleep_level, date)

    return sleep_log

def get_appetitelog_by_user(user_id):
    """Gett all appetite log by user"""
    appetite_level=[]
    date=[]

    dailylogs= UserDailyLog.query.filter_by(user_id=user_id).all()

    for user in dailylogs:
        appetite_level.append(user.appetite_level)
        date.append(user.date)

    appetite_log= zip(appetite_level, date)

    return appetite_log

def get_fatiguelog_by_user(user_id):
    """Gett all fatigue log by user"""
    fatigue_level=[]
    date=[]

    dailylogs= UserDailyLog.query.filter_by(user_id=user_id).all()

    for user in dailylogs:
        fatigue_level.append(user.fatigue_level)
        date.append(user.date)

    fatigue_log= zip(fatigue_level, date)

    return fatigue_log

if __name__ == "__main__":
    from server import app
    connect_to_db(app)