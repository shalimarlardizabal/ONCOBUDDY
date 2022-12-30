"""Models for OncoBuddy"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///oncobuddy", echo= False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db")

class User(db.Model):
    """A User"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    user_name = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    age= db.Column(db.Integer)
    sex= db.Column(db.String)

    drugs= db.relationship("Drug", secondary="user_drugs", back_populates= "users")
    symptoms = db.relationship("Symptom", secondary = "user_symptoms", back_populates= "users")
    diagnoses = db.relationship("Diagnosis", secondary= "user_diagnoses", back_populates= "users")
    # administered_drugs = db.relationship("Drug", secondary="user_administered_drugs", back_populates="users")
    
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class UserSymptom(db.Model):
    """Symptoms of specific user"""
    
    __tablename__= "user_symptoms"

    user_symptom_id= db.Column(db.Integer, primary_key= True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    symptom_id= db.Column(db.Integer, db.ForeignKey("symptoms.symptom_id"))
    symptom_name= db.Column(db.String)
    pain_level= db.Column(db.Integer)
    pain_location_id=db.Column(db.Integer)
    sleep_level= db.Column(db.Integer)
    fatigue_level= db.Column(db.Integer)
    appetite_level= db.Column(db.Integer)
    date= db.Column(db.DateTime)
    
    
    def __repr__(self):
        return f'<UserSymptoms user_symptom_id={self.user_symptom_id} symptom_id = {self.symptom_id} date = {self.date}>'

class UserDrug(db.Model):
    """Drugs specific user is prescribed"""
    
    __tablename__= "user_drugs"

    user_drug_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    drug_id= db.Column(db.Integer, db.ForeignKey("drugs.drug_id"))
    drug_name= db.Column(db.String)

    user_administered_drugs = db.relationship("UserAdministeredDrug", back_populates="user_drugs")
    
    def __repr__(self):
        return f'<UserDrugs user_drug_id={self.user_drug_id}'

class UserAdministeredDrug(db.Model):
    """Drugs administered on specific user"""

    __tablename__= "user_administered_drugs"

    administered_drug_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_drug_id= db.Column(db.Integer, db.ForeignKey("user_drugs.user_drug_id"))
    drug_name= db.Column(db.String)
    administration_date= db.Column(db.DateTime)

    user_drugs = db.relationship("UserDrug", back_populates="user_administered_drugs")

    def __repr__(self):
        return f'<UserAdministeredDrugs administered_drug_id={self.administered_drug_id} administration_date ={self.administration_date}>'

class UserDiagnosis(db.Model):
    """Diagnosis of specific user"""
    
    __tablename__ = "user_diagnoses"

    user_diagnosis_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    diagnosis_id= db.Column(db.Integer, db.ForeignKey("diagnoses.diagnosis_id"))
    diagnosis_name= db.Column(db.String)

    def __repr__ (self):
        return f'<UserDiagnosis user_diagnosis_id= {self.user_diagnosis_id}, user_id={self.user_id}>'

class Diagnosis(db.Model):
    """Diagnosis"""
    __tablename__= "diagnoses"

    diagnosis_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String)
    common_name= db.Column(db.String)
    # description= db.Column(db.Text)

    users = db.relationship("User", secondary= "user_diagnoses", back_populates= "diagnoses")

    def __repr__(self):
        return f'<Diagnosis diagnosis_id= {self.diagnosis_id} name= {self.name}>'

class Symptom (db.Model):
    """All symptoms"""
    
    __tablename__= "symptoms"

    symptom_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String)
    common_name= db.Column(db.String)
    # description= db.Column(db.Text)
    
    users = db.relationship("User", secondary= "user_symptoms", back_populates= "symptoms")

    def __repr__ (self):
        return f'<Symptoms symptom_id {self.symptom_id} name= {self.name}>'

class Drug (db.Model):
    """All Drugs"""

    __tablename__= "drugs"

    drug_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    # side_effect_id= db.Column(db.Integer, db.ForeignKey("side_effects.side_effect_id"))
    
    users = db.relationship("User", secondary= "user_drugs", back_populates= "drugs")
    # administered_drugs= db.relationship("User", secondary= "user_administered_drugs", back_populates="drugs")
    # side_effects= db.relationship("SideEffect", back_populates= "drugs")
    
    def __repr__ (self):
        return f'<Drugs drug_id {self.drug_id} name= {self.name}>'

# class SideEffect(db.Model):
#     """All possible side effects"""

#     __tablename__= "side_effects"

#     side_effect_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String)
#     description = db.Column(db.Text)
    
#     drugs = db.relationship("Drug", back_populates= "side_effects")

#     def __repr__(self):
#         return f'<Side Effects side_effect_id= {self.side_effect_id} name = {self.name}>'

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    # with app.app_context():
    #     db.create_all()
    #     test_user= User(email='test@test.test', password= 'test', user_name= 'Test Test')
    #     db.session.add(test_user)
    #     db.session.commit()
    #     print(test_user)