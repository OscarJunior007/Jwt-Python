from pydantic import BaseModel

class User1(BaseModel):
    id: str
    username:str
    email: str  
    profile:str
    
class UserInDB(User1):
    password:str   
    
class Token(BaseModel):
    access_token: str   
    token_type: str = "bearer"  
    
class UserCreate(BaseModel):
    nombre:str
    email:str
    password:str    
    
    