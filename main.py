""" from fastapi import FastAPI, Form, Depends
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import database

app = FastAPI()

# Allow all origins (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
import sqlite3
print(sqlite3.version)

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Route to create a new client
@app.post("/clients/")
def create_client(name: str, client_code: str, db: Session = Depends(get_db)):
    return crud.create_client(db=db, name=name, client_code=client_code)

# Route to list all clients, ordered by name
@app.get("/clients/")
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

# Route to render the HTML form
@app.get("/add-client-form", response_class=HTMLResponse)
def get_add_client_form(request: Request):
    return templates.TemplateResponse("add_client_form.html", {"request": request})

# Route to process form submission
@app.post("/add-client-form")
def post_add_client_form(
    name: str = Form(...), client_code: str = Form(...), db: Session = Depends(get_db)
):
    crud.create_client(db=db, name=name, client_code=client_code)
    return {"message": "Client added successfully", "name": name, "client_code": client_code} """

from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import database
import random
import string

app = FastAPI()

# Allow all origins (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

# Function to generate a random client code
def generate_client_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@app.get("/")
def read_root():
    return {"message": "Hello, katambo. i am working and up and running!"}

# Route to display form
@app.get("/add-client-form", response_class=HTMLResponse)
def show_add_client_form(request: Request):
    return templates.TemplateResponse("add_client_form.html", {"request": request, "message": ""})

# Route to create a new client
@app.post("/add-client-form", response_class=HTMLResponse)
def add_client(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    client_code = generate_client_code()
    crud.create_client(db=db, name=name, client_code=client_code)
    message = f"Client '{name}' added successfully with code: {client_code}"
    return templates.TemplateResponse("add_client_form.html", {"request": request, "message": message})

@app.get("/clients/", response_class=HTMLResponse)
def read_clients(request: Request, db: Session = Depends(get_db)):
    clients = crud.get_clients(db)
    return templates.TemplateResponse(
        "client_list.html", {"request": request, "clients": clients}
    )