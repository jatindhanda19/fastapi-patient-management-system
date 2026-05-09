from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient")]
    name: Annotated[str, Field(..., description="The name of the patient")]
    city: Annotated[str, Field(..., description="The city of the patient")]
    age: Annotated[int, Field(...,gt=0, lt=120, description="The age of the patient")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/((self.height/100)**2), 2)
        return bmi
    
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def hello():
    return {"message": "Patient Management System API is running!"}

@app.get("/about")
def about():
    return {"message": "This is a simple Patient Management System API."}

@app.get('/view')
def view():
    data = load_data()
    return {"patients": data["patients"]}

@app.get('/patient/{id}')
def view_patient(id: str = Path(..., description="The ID of the patient to retrieve", examples=["P001"], ge=0)):
    data = load_data()
    for patient in data["patients"]:
        if patient["id"] == id:
            return {"patient": patient}
    raise HTTPException(status_code=404, detail="Patient not found.")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="Sort in asc and desc order")):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field: {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order: 'asc' or 'desc'")
    
    data = load_data()
    reverse = True if order=='desc' else False
    
    sorted_patients = sorted(data["patients"], key=lambda x: x.get('height', 0), reverse=reverse) if sort_by == 'height' else sorted(data["patients"], key=lambda x: x.get('weight', 0), reverse=sort_order) if sort_by == 'weight' else sorted(data["patients"], key=lambda x: x.get('bmi', 0), reverse=sort_order)
    return {"sorted_patients": sorted_patients}

@app.post('/add')
def create_patient(patient: Patient):
    data = load_data()

    for existing_patient in data["patients"]:
        if existing_patient["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
        
    data["patients"].append(patient.model_dump())
    save_data(data)
    return {"message": "Patient added successfully."}

@app.put('/edit/{id}')
def update_patient(id: str, patient_update: PatientUpdate):
    data = load_data()
    for index, patient in enumerate(data["patients"]):
        if patient["id"] == id:    
            updated_info = patient_update.model_dump(exclude_unset=True)
            
            for key, value in updated_info.items():
                patient[key] = value

            validated_patient = Patient(**patient)
            data["patients"][index] = validated_patient.model_dump()

            save_data(data)
    
            return JSONResponse(
                status_code=200, 
                content={"message": "Patient updated successfully."}
                )
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete('/delete/{id}')
def delete_patient(id: str):
    data = load_data()
    
    for index, patient in enumerate(data["patients"]):
        if patient["id"] == id:
            data["patients"].pop(index)
            save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully."})

raise HTTPException(status_code=404, detail="Patient not found")



