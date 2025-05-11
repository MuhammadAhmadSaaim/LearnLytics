from venv import logger
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Load the logging configuration
import logging
logging.basicConfig(level=logging.INFO)

# Load the saved model
model = joblib.load('model/student_grade_predictor.pkl')

# Define the FastAPI app
app = FastAPI()

# Allow all origins (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Pydantic model for input validation
class StudentData(BaseModel):
    Gender: str
    Age: int
    Department: str
    Attendance: float
    Midterm_Score: float
    Assignments_Avg: float
    Quizzes_Avg: float
    Participation_Score: float
    Projects_Score: float
    Study_Hours_per_Week: float
    Extracurricular_Activities: str
    Internet_Access_at_Home: str
    Parent_Education_Level: int
    Stress_Level: float
    Sleep_Hours_per_Night: float

# Function to predict grade based on the score
def predict_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# Define the prediction endpoint
@app.post("/predict")
def predict(student_data: StudentData):
    try:
        # Convert the input data to a DataFrame
        student_df = pd.DataFrame([student_data.dict()])

        # Make the prediction
        predicted_score = model.predict(student_df)[0]
        predicted_grade = predict_grade(predicted_score)

        # Return the result as a dictionary
        return {
            "predicted_score": round(predicted_score, 2),
            "predicted_grade": predicted_grade
        }

    except Exception as e:
        return {"error": str(e)}

# To run the server, use the command below in the terminal:
# uvicorn app:app --reload
