from sqlalchemy import Column, Integer, Float
from database.database import Base

class RetinopathyData(Base):
    __tablename__ = "retinopathy_data"

    PtID = Column(Integer, primary_key=True, index=True)
    Age = Column(Float)
    Sex = Column(Integer)
    Duration_of_Diabetes = Column(Float)
    IMC = Column(Float)
    Has_Hypertension = Column(Integer)
    TotDlyIns = Column(Float)
    Is_Pump_User = Column(Integer)
    Glucose_Mean = Column(Float)
    Glucose_Std = Column(Float)
    Glucose_CV = Column(Float)
    Time_In_Range_70_180 = Column(Float)
    Time_Above_180 = Column(Float)
    Time_Above_250 = Column(Float)
    Time_Below_70 = Column(Float)
    Time_Below_54 = Column(Float)
    Education_Score = Column(Float)
    Keeps_BG_High_Fear = Column(Float)
    Not_Careful_Eating_Distress = Column(Float)

class UserMedicalData(Base):
    __tablename__ = "user_medical_data"

    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Float)
    glucose = Column(Float)
    blood_pressure = Column(Float)
