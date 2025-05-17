from sqlmodel import Session, create_engine,SQLModel,Field
from uuid import uuid4

class User(SQLModel,table=True):
    __tablename__ = "usuarios"
    id: str = Field(default_factory=lambda: str(uuid4()),primary_key=True)
    nombre:str
    email:str
    profile : str = Field("DEFAULT")
    password: str   
    
    
DB_FILE = "db.sqlite3"
engine =  create_engine(f"sqlite:///{DB_FILE}",echo=True)

def get_session():
    return Session(engine)

def create_table():
    SQLModel.metadata.create_all(engine)    
    
    
if __name__ == "__main__":  
    create_table()  