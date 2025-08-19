from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from sqlalchemy.orm import sessionmaker
from openai import OpenAI   
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

os.environ["OPENAI_API_KEY"]=
client = OpenAI()

# User Can ask his query here
class UserQuery(BaseModel):
    query: str


# User model for SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)

# Create the database table
Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def translate_text(query):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Professional Fitness Coach in which you have to give the best recommendations to the users query on his way to Become Fit, like what to eat and when to eat and what foods to avoid etc.. , I need you to be as Blunt as Possible. this is the Users Query :",
            },
            {"role": "user", "content": query},
        ],
    )
    return completion.choices[0].message.content


def scemantic_search(query):
    vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db")

    docs = db.similarity_search(query)

    return docs



#Create a new user
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Get all users
@app.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

#Delete the user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.post("/translate/")  # This line decorates 'translate' as a POST endpoint
async def translate(request: UserQuery):
    try:
        # Call your translation function
        translated_text = translate_text(request.query)
        return {"translated_text": translated_text}
    except Exception as e:
        # Handle exceptions or errors during translation
        raise HTTPException(status_code=500, detail=str(e))
    