from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
import os

app = FastAPI()

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost:3306/prova'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patient"
    
    patientID = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    
    vaccines = relationship("Vaccine", cascade="all, delete-orphan", back_populates="patient")

class Vaccine(Base):
    __tablename__ = "vaccine"
    
    vaccineID = Column(Integer, primary_key=True, index=True, nullable=False)
    vaccineName = Column(String(50), nullable=False)
    doseDate = Column(String(10), nullable=False)
    doseNumber = Column(Integer, nullable=False)
    vaccineType = Column(String(50), nullable=False)
    
    patientID = Column(Integer, ForeignKey('patient.patientID', ondelete='CASCADE'), nullable=False)
    patient = relationship("Patient", back_populates="vaccines")
    doses = relationship("Dose", cascade="all, delete-orphan", back_populates="vaccine")

class Dose(Base):
    __tablename__ = "dose"
    
    doseID = Column(Integer, primary_key=True, index=True, nullable=False)
    typeDose = Column(String(50), nullable=False)
    doseDate = Column(String(10), nullable=False)
    doseNumber = Column(Integer, nullable=False)
    applicationType = Column(String(50), nullable=False)
    
    vaccineID = Column(Integer, ForeignKey('vaccine.vaccineID', ondelete='CASCADE'), nullable=False)
    vaccine = relationship("Vaccine", back_populates="doses")

Base.metadata.create_all(bind=engine)

@app.get("/patients")
def read_patients():
    patients = session.query(Patient).all()
    
    patientList = []
    
    for patient in patients:
        if patient is None:
             return JSONResponse(content={'Erro 400': 'bad request'})
        patient_dict = {"id": patient.patientID, "name": patient.name, "last Name": patient.lastName}
        patientList.append(patient_dict)
        
    return JSONResponse(content=patientList)

@app.get("/patients/{patientID}")
def read_patient(patientID: int):
    patient = session.query(Patient).filter(Patient.patientID == patientID).first()
    
    
    if patient is not None:
        patient_dict = {"id": patient.patientID, "name": patient.name, "last Name": patient.lastName}
        return JSONResponse(content=patient_dict)
    else:
        return JSONResponse(content={'Erro 400': 'bad request'})

@app.post("/patients")
def create_patient(name: str, lastName: str):
    patient = Patient(name=name, lastName=lastName)
    session.add(patient)
    session.commit()
    
    
    
    if patient is not None:
        patient_dict = {"id": patient.patientID, "name": patient.name, "last Name": patient.lastName}
        return JSONResponse(content=patient_dict)
    else:
        return JSONResponse(content={'Erro 400': 'bad request'})

@app.put("/patients/{patientID}")
def update_patient(patientID: int, name: str, lastName: str):
    patient = session.query(Patient).filter(Patient.patientID == patientID).first()

    if patient is None:
        return JSONResponse(content={'Erro 400': 'bad request'})


    patient.name = name
    patient.lastName = lastName
    session.commit()
    
   
    
    patient_dict = {"id": patient.patientID, "name": patient.name, "last Name": patient.lastName}
    return JSONResponse(content=patient_dict)
        
@app.delete("/patients/{patientID}")
def delete_patient(patientID: int):
    patient = session.query(Patient).filter(Patient.patientID == patientID).first()

    if patient is None:
        return JSONResponse(content={'Erro 400': 'bad request'})

    session.delete(patient)
    session.commit()
    
    
    
    
    patient_dict = {"id": patient.patientID, "name": patient.name, "last Name": patient.lastName}
    
    return JSONResponse(content=patient_dict)
    
         

@app.get("/vaccines")
def read_vaccines():
    vaccines = session.query(Vaccine).all()
    vaccinesList = []
    for vaccine in vaccines:
        if vaccine is None:
             return JSONResponse(content={'Erro 400': 'bad request'})
        patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()
        vaccine_dict = {"id": vaccine.vaccineID, "vaccine name": vaccine.vaccineName, "Dose Date": vaccine.doseDate, "Dose Number": vaccine.doseNumber, "Vaccine Type": vaccine.vaccineType, "Patient": {'name': patient.name, 'last name': patient.lastName}}
        vaccinesList.append(vaccine_dict)
        
    return JSONResponse(content=vaccinesList)

@app.get("/vaccines/{vaccineID}")
def read_vaccine(vaccineID: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == vaccineID).first()

    if vaccine is None:
        return JSONResponse(content={'Erro 400': 'bad request'})

    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()
    
    
	
    
    vaccine_dict = {"id": vaccine.vaccineID, "name": vaccine.vaccineName, "Dose Date": vaccine.doseDate, "Dose Number": vaccine.doseNumber, "Vaccine Type": vaccine.vaccineType, "Patient": { "Name": patient.name, "Last Name": patient.lastName}}
    
    return JSONResponse(content=vaccine_dict)
   

@app.post("/vaccines")
def create_vaccine(patientID: int, vaccineName: str, doseDate: str, doseNumber: int, vaccineType: str):
    vaccine = Vaccine(patientID=patientID, vaccineName=vaccineName, doseDate=doseDate, doseNumber=doseNumber, vaccineType=vaccineType)
    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()
    session.add(vaccine)
    session.commit()
    
    
	
    if vaccine is not None:
        vaccine_dict = {"id": vaccine.vaccineID, "name": vaccine.vaccineName, "Dose Date": vaccine.doseDate, "Dose Number": vaccine.doseNumber, "Vaccine Type": vaccine.vaccineType, "Patient": { "Name": patient.name, "Last Name": patient.lastName}}
        return JSONResponse(content=vaccine_dict)
    else:
        return JSONResponse(content={'erro 400': "bad request"})

@app.put("/vaccines/{vaccineID}")
def update_patient(vaccineID: int, patientID: int, vaccineName: str, doseDate: str, doseNumber: int, vaccineType: str):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == vaccineID).first()

    if vaccine is None:
        return JSONResponse(content={'Erro 400': 'bad request'})

    patient = session.query(Patient).filter(Patient.patientID == patientID).first()

    if patient is None:
        return JSONResponse(content={'erro 400': "bad request"})
    
    vaccine.doseDate = doseDate
    vaccine.doseNumber = doseNumber
    vaccine.vaccineName = vaccineName
    vaccine.patientID = patientID
    vaccine.vaccineType = vaccineType
    session.commit()
    
    
	
    
    vaccine_dict = {"id": vaccine.vaccineID, "name": vaccine.vaccineName, "Dose Date": vaccine.doseDate, "Dose Number": vaccine.doseNumber, "Vaccine Type": vaccine.vaccineType, "Patient": { "Name": patient.name, "Last Name": patient.lastName}}
    
    return JSONResponse(content=vaccine_dict)
   
    
@app.delete("/vaccines/{vaccineID}")
def delete_vaccine(vaccineID: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == vaccineID).first()

    if vaccine is None:
        return JSONResponse(content={'Erro 400': 'bad request'})

    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()
    session.delete(vaccine)
    session.commit()
    
    
	
  
    vaccine_dict = {"id": vaccine.vaccineID, "name": vaccine.vaccineName, "Dose Date": vaccine.doseDate, "Dose Number": vaccine.doseNumber, "Vaccine Type": vaccine.vaccineType, "Patient": { "Name": patient.name, "Last Name": patient.lastName}}
    
    return JSONResponse(content=vaccine_dict)
    

@app.get("/doses")
def read_doses():
    doses = session.query(Dose).all()
    dosesList = []
    
    for dose in doses:
        if dose is None:
            return JSONResponse(content={'erro 400': "bad request"})    
    
        vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == dose.vaccineID).first()
        patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()
        dose_dict = {
            "id": dose.doseID,
            "Dose Date": dose.doseDate,
            "Dose Number": dose.doseNumber,
            "Application Type": dose.applicationType,
            "Type Dose": dose.typeDose,
            "vaccine": {
                "id": vaccine.vaccineID,
                "name": vaccine.vaccineName,
                "Dose Date": vaccine.doseDate,
                "Dose Number": vaccine.doseNumber,
                "Vaccine Type": vaccine.vaccineType,
                "Patient": {
                    "Name": patient.name,
                    "Last Name": patient.lastName
                }
            }
        }
        dosesList.append(dose_dict)
    
    return JSONResponse(content=dosesList)


@app.get("/doses/{doseID}")
def read_dose(doseID: int):
    dose = session.query(Dose).filter(Dose.doseID == doseID).first()

    if dose is None:
        return JSONResponse(content={'Erro 400': 'bad request'})

    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == dose.vaccineID).first()
    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()
    
    
    
    dose_dict = {"id": dose.doseID, "Dose Date": dose.doseDate, "Dose Number": dose.doseNumber, "Application Type": dose.applicationType, "Type Dose": dose.typeDose, "vaccine": {"id": vaccine.vaccineID, "name": vaccine.vaccineName, "Dose Date": vaccine.doseDate, "Dose Number": vaccine.doseNumber, "Vaccine Type": vaccine.vaccineType, "Patient":{ "Name": patient.name, "Last Name": patient.lastName}}}
    
    return JSONResponse(content=dose_dict)
    
@app.post("/doses")
def create_dose(vaccineID: int, typeDose: str, doseDate: str, doseNumber: int, applicationType: str):
    dose = Dose(vaccineID=vaccineID, typeDose=typeDose, doseDate=doseDate, doseNumber=doseNumber, applicationType=applicationType)

    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == dose.vaccineID).first()
    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()

    session.add(dose)
    session.commit()

    if dose is not None:
        dose_dict = {
            "id": dose.doseID,
            "Dose Date": dose.doseDate,
            "Dose Number": dose.doseNumber,
            "Application Type": dose.applicationType,
            "Type Dose": dose.typeDose,
            "vaccine": {
                "id": vaccine.vaccineID,
                "name": vaccine.vaccineName,
                "Dose Date": vaccine.doseDate,
                "Dose Number": vaccine.doseNumber,
                "Vaccine Type": vaccine.vaccineType,
                "Patient": {
                    "Name": patient.name,
                    "Last Name": patient.lastName
                }
            }
        }
        return JSONResponse(content=dose_dict)
    else:
        return JSONResponse(content={'erro 400': "bad request"})


@app.put("/doses/{doseID}")
def update_dose(doseID: int, vaccineID: int, typeDose: str, doseDate: str, doseNumber: int, applicationType: str):
    dose = session.query(Dose).filter(Dose.doseID == doseID).first()

    if dose is None:
        return JSONResponse(content={'erro 400': "bad request"})

    dose.vaccineID = vaccineID
    dose.applicationType = applicationType
    dose.doseDate = doseDate
    dose.doseNumber = doseNumber
    dose.typeDose = typeDose

    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == dose.vaccineID).first()

    if vaccine is None:
        return JSONResponse(content={'erro 400': "bad request"})
    
    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()

    if patient is None:
        return JSONResponse(content={'erro 400': "bad request"})

    session.commit()

    dose_dict = {
        "id": dose.doseID,
        "Dose Date": dose.doseDate,
        "Dose Number": dose.doseNumber,
        "Application Type": dose.applicationType,
        "Type Dose": dose.typeDose,
        "vaccine": {
            "id": vaccine.vaccineID,
            "name": vaccine.vaccineName,
            "Dose Date": vaccine.doseDate,
            "Dose Number": vaccine.doseNumber,
            "Vaccine Type": vaccine.vaccineType,
            "Patient": {
                "Name": patient.name,
                "Last Name": patient.lastName
            }
        }
    }
    return JSONResponse(content=dose_dict)

@app.delete("/doses/{doseID}")
def delete_dose(doseID: int):
    dose = session.query(Dose).filter(Dose.doseID == doseID).first()

    if dose is None:
        return JSONResponse(content={'erro 400': "bad request"})

    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == dose.vaccineID).first()
    patient = session.query(Patient).filter(Patient.patientID == vaccine.patientID).first()

    session.delete(dose)
    session.commit()

    dose_dict = {
        "id": dose.doseID,
        "Dose Date": dose.doseDate,
        "Dose Number": dose.doseNumber,
        "Application Type": dose.applicationType,
        "Type Dose": dose.typeDose,
        "vaccine": {
            "id": vaccine.vaccineID,
            "name": vaccine.vaccineName,
            "Dose Date": vaccine.doseDate,
            "Dose Number": vaccine.doseNumber,
            "Vaccine Type": vaccine.vaccineType,
            "Patient": {
                "Name": patient.name,
                "Last Name": patient.lastName
            }
        }
    }
    return JSONResponse(content=dose_dict)
