#  Patient Management API

A simple REST API built with FastAPI to manage patient records with CRUD operations, automatic BMI calculation, sorting, and input validation.

##  Features

- Add, view, update, and delete patients
- View patient by ID
- Sort by height, weight, or BMI
- Automatic BMI calculation
- Input validation with Pydantic
- Interactive API docs with Swagger

##  Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON

##  Project Structure

```text
patient-management-api/
├── main.py
├── patient.json
├── requirements.txt
└── README.md
```
 Installation
git clone https://github.com/your-username/patient-management-api.git
cd patient-management-api
pip install -r requirements.txt

 Run the Application
uvicorn main:app --reload

API Documentation
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

 API Endpoints
Method	Endpoint	   Description
GET	    /view	       Get all patients
GET	    /patient/{id}	Get patient by ID
GET	    /sort	        Sort patients
POST	  /add	        Add a patient
PUT	    /edit/{id}	  Update a patient
DELETE	/delete/{id}	Delete a patient

Sample Request
{
  "id": "P001",
  "name": "Jatin",
  "city": "Kurukshetra",
  "age": 21,
  "gender": "Male",
  "height": 175,
  "weight": 68
}
Example patient.json
{
  "patients": []
}

 Requirements
fastapi
uvicorn
pydantic

 Future Improvements
-SQLite database integration
-JWT authentication
-Unit testing with pytest
-Docker support

Author
Jatin Dhanda
