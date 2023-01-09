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

    drugs= db.relationship("Drug", secondary="user_drugs", back_populates= "users")
    symptoms = db.relationship("Symptom", secondary = "user_symptoms", back_populates= "users")
    diagnoses = db.relationship("Diagnosis", secondary= "user_diagnoses", back_populates= "users")
    daily_logs= db.relationship("UserDailyLog", back_populates="users")
    diagnoses = db.relationship("Diagnosis", secondary= "user_diagnoses", back_populates= "users")
    oncology_diagnoses= db.relationship("CancerDiagnosis", secondary= "user_cancer", back_populates= "users")
    
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class UserSymptom(db.Model):
    """Symptoms of specific user"""
    
    __tablename__= "user_symptoms"

    user_symptom_id= db.Column(db.Integer, primary_key= True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    symptom_id= db.Column(db.Integer, db.ForeignKey("symptoms.symptom_id"))
    symptom_name= db.Column(db.String)
    date= db.Column(db.DateTime)
    
    
    def __repr__(self):
        return f'<UserSymptoms user_symptom_id={self.user_symptom_id} symptom_id = {self.symptom_id} date = {self.date}>'

class UserDailyLog(db.Model):

    __tablename__= "daily_logs"

    daily_log_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    pain_level= db.Column(db.Integer)
    pain_location_id=db.Column(db.Integer)
    sleep_level= db.Column(db.Integer)
    fatigue_level= db.Column(db.Integer)
    appetite_level= db.Column(db.Integer)
    date= db.Column(db.DateTime)

    users = db.relationship("User", back_populates= "daily_logs")

    def __repr__(self):
        return f'<UserDailyLog daily_log_id={self.daily_log_id} user_id={self.user_id}>'

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

    users = db.relationship("User", secondary= "user_diagnoses", back_populates= "diagnoses")

    def __repr__(self):
        return f'<Diagnosis diagnosis_id= {self.diagnosis_id} name= {self.name}>'
class UserCancerDiagnosis(db.Model):
    """Cancer Diagnosis of Specific User"""

    __tablename__= "user_cancer"

    user_cancer_diagnosis_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cancer_id= db.Column(db.Integer, db.ForeignKey("oncology_diagnoses.cancer_id"))
    cancer_name= db.Column(db.String)
    
    def __repr__ (self):
        return f'<UserCancer user_cancer_id= {self.user_cancer_diagnosis_id}, cancer_id={self.cancer_id}>'

class CancerDiagnosis(db.Model):
    """Oncology Diagnosis"""
    __tablename__= "oncology_diagnoses"

    cancer_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String)
    description= db.Column(db.Text)

    users = db.relationship("User", secondary= "user_cancer", back_populates= "oncology_diagnoses")
    
    def __repr__ (self):
        return f'<Cancer Diagnosis cancer_id {self.cancer_id} name= {self.name}>'

class Symptom (db.Model):
    """All symptoms"""
    
    __tablename__= "symptoms"

    symptom_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String)
    common_name= db.Column(db.String)
    
    users = db.relationship("User", secondary= "user_symptoms", back_populates= "symptoms")

    def __repr__ (self):
        return f'<Symptoms symptom_id {self.symptom_id} name= {self.name}>'

class Drug (db.Model):
    """All Drugs"""

    __tablename__= "drugs"

    drug_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    
    users = db.relationship("User", secondary= "user_drugs", back_populates= "drugs")

    def __repr__ (self):
        return f'<Drugs drug_id {self.drug_id} name= {self.name}>'


if __name__ == "__main__":
    from server import app
    connect_to_db(app)