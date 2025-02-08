import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Get the database URL from an environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Note model
class Note(Base):
    __tablename__ = "notes"
    name = Column(String(10), primary_key=True, index=True)
    content = Column(String(200), index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create an instance of the FastAPI class
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for the Note
class NoteCreate(BaseModel):
    name: str
    content: str

class NoteRead(BaseModel):
    name: str
    content: str

# Define a route to add a note
@app.post("/notes/", response_model=NoteRead)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(name=note.name, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Define a route to read a note
@app.get("/notes/{name}", response_model=NoteRead)
def read_note(name: str, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.name == name).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@app.get("/")
def read_root():
    return {"Hello": "Hello from fastapi backend inside docker"}

# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
