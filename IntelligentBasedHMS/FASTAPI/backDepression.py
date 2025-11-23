import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Annotated, Literal, Optional
import pickle
import pandas as pd
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()
threshold = 0.24  

# Load Pipeline
def load_pipeline(path=r"C:\Users\Muhammad's PC\Documents\saad\Intelligent Health Monitoring System\IntelligentBasedHMS\pipe.pkl"):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Pipeline file not found: {path.resolve()}")
    with open(path, "rb") as f:
        pipe = pickle.load(f)
    return pipe

try:
    pipe = load_pipeline(r"C:\Users\Muhammad's PC\Documents\saad\Intelligent Health Monitoring System\IntelligentBasedHMS\pipe.pkl")
except Exception as e:
     print("Could not load pipeline (pipe.pkl). Make sure file is in the same folder as this script.")

class DepressionInput(BaseModel):
    gender: Annotated[str, Field(description="Gender of the person")]
    succide: Annotated[str, Field(description="Have you ever had suicidal thoughts?")]
    age: Annotated[int, Field(description="Age of the person")]
    work_hours: Annotated[int, Field(..., gt=0, lt=12, description="Work/Study Hours (0-12)")]
    profession: Annotated[str, Field(description="Profession of the person")]
    sleep: Annotated[int, Field(..., gt=0, lt=24, description="Sleep Duration (hours)")]
    financial: Annotated[int, Field(..., gt=0, lt=5, description="Financial Stress (0-5)")]
    family: Annotated[str, Field(description="Family History of Mental Illness?")]
    pressure: Annotated[int, Field(..., gt=0, lt=5, description="Pressure (0-5)")]
    dietary: Annotated[str, Field(description="Dietary Habits")]
    satisfaction: Annotated[int, Field(..., gt=0, lt=5, description="Satisfaction (0-5)")] 


@app.post("/predict_depression/")
def predict_depression(input_data: DepressionInput):
    
    # Convert input to DataFrame
    input_df = pd.DataFrame([{
        'Gender': input_data.gender,
        'Age': input_data.age,
        'Working Professional or Student': input_data.profession,
        'Sleep Duration': input_data.sleep,
        'Dietary Habits': input_data.dietary,
        'Have you ever had suicidal thoughts ?': input_data.succide,   
        'Work/Study Hours': input_data.work_hours,
        'Financial Stress': input_data.financial,
        'Family History of Mental Illness': input_data.family,
        'Pressure': input_data.pressure,
        'Satisfaction': input_data.satisfaction
    }])

    # ✅ If model supports probability prediction
    if hasattr(pipe, "predict_proba"):
        proba = pipe.predict_proba(input_df)[0][1]  # probability of positive/depressed class
        proba = float(proba)

        # Apply threshold classification
        status = "High Risk of Depression" if proba >= threshold else "Low Risk of Depression"

        return JSONResponse(status_code=200, content={"depression_probability": proba,"risk_status": status})

    # ⚠️ If no predict_proba, fall back to normal prediction
    pred = pipe.predict(input_df)[0]
    pred = int(pred)

    status = "High Risk of Depression" if pred == 1 else "Low Risk of Depression"

    return JSONResponse(status_code=200, content={"depression_prediction": pred,"risk_status": status})
 