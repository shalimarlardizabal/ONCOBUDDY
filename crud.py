"""OncoBuddy CRUD operations"""
from model import connect_to_db, db, User, UserSymptom, UserAdministeredDrug, UserDrug, UserDiagnosis, Diagnosis, Symptom, Drug

def create_user(email, password, user_name, age, sex):
    """create and return a new user"""
    user = User(email= email, password=password, user_name= user_name, age=age, sex= sex)

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

def add_user_diagnosis(user_id, diagnosis_id):
    
    user_diagnosis = UserDiagnosis(user_id= user_id, diagnosis_id=diagnosis_id)

def create_drugs(name, description):

    drug= Drug(name=name, description= description)

    return drug

def show_all_drugs():
    
    return Drug.query.all()

def get_drug_by_name(name):

    return Drug.query.get(name)

def add_user_drugs(user_id, drug_id):

    user_drug= UserDrug(user_id, drug_id)

    return user_drug

def add_administered_drug(user_drug_id, administration_date):

    administered_drug= UserAdministeredDrug(user_drug_id, administration_date)
    
    return administered_drug

if __name__ == "__main__":
    from server import app
    connect_to_db(app)