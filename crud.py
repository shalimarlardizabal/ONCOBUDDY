"""OncoBuddy CRUD operations"""
from model import connect_to_db, db, User, UserSymptom, UserAdministeredDrug, UserDrug, UserDiagnosis, Diagnosis, Symptom, Drug, SideEffect

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

# def add_user_diagnosis(user_id, symptom_id):
    
    
#     user_diagnosis = 
# def add_user_drugs():

# def add_user_administered_drugs():

# def add_user_symptoms():

# def show_all_drugs():

# def show_all_symptoms():
# def show_all_side_effects():

if __name__ == "__main__":
    from server import app
    connect_to_db(app)