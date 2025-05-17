from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse  
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm    
from db import get_session,User

from pydantic import BaseModel
from utils import create_access_token,decode_token,get_password_hash,verify_password
from schemas import UserCreate,User1
from deps import get_user,authenticate_user,get_current_user
app = FastAPI()
 
 
def create_user(data: UserCreate, password_hash: str):
    with get_session() as session:
        user = User(nombre=data.nombre, email=data.email, password=password_hash)  
        session.add(user)
        session.commit()    
    return user.dict()
     
 
@app.post("/api/register")
async def register_user(user:UserCreate): 
    db_user = get_user(user.email)
    
    if db_user:
        raise HTTPException(status_code=400,detail="Email already exists")  
    hashed_password = get_password_hash(user.password) 
    
    new_user = create_user(user,hashed_password)
    
    if new_user is None:
        return {"message": "No se pudo crear al usuario"}
    return  JSONResponse(status_code=201,content=jsonable_encoder(user))

@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  
    user = authenticate_user(form_data.username,form_data.password) 
    if not user:
        raise HTTPException(status_code=400,detail="Invalid email or password") 
    access_token = create_access_token(data={"email":user["email"]})
    return {"access_token":access_token,"token_type":"bearer"}   


@app.get("/api/me")
async def read_user_me(current_user: User1 = Depends(get_current_user)):
    return current_user  
    

    
    

