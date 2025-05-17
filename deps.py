from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm    
from utils import create_access_token,decode_token,get_password_hash,verify_password
from db import get_session,User
ruta_token = OAuth2PasswordBearer(tokenUrl="api/login")

def get_user(email:str):
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()      
    if user is None:
        return None
    return user.dict()

def authenticate_user(email: str, password: str): 
    user = get_user(email)
    if not user:
        raise HTTPException(status_code=404,detail="Usuario no encontrado")
    if not verify_password(password,user['password']): 
        raise HTTPException(status_code=401,detail="Credenciales incorrectas")  
    return user

async def get_current_user(token:str = Depends(ruta_token)):
    payload = decode_token(token)
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=401,detail="Invalid token") 
    user = get_user(email)
    if user is None:
        raise HTTPException(status_code=404,detail="Usuario no encontrado") 
    return user 
