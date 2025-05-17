from jose import jwt    
from jose.exceptions import JWTError
from datetime import datetime,timedelta,timezone
import bcrypt

secret_key = "my_secret_key" 
algorithm = "HS256" 

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy() 
    expire =  datetime.now(timezone.utc) + expires_delta if expires_delta else datetime.now(timezone.utc) + timedelta(minutes=15)   
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,secret_key,algorithm=algorithm)

def decode_token(token:str):
    try:
        return jwt.decode(token,secret_key,algorithms=[algorithm])  
    except JWTError as e: 
        return {"error":str(e)} 
    
    
def get_password_hash(password:str) ->str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)     
    return hashed_password.decode('utf-8')


def verify_password(password:str, hash_password:str) -> str:
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))  

if __name__ == "__main__":
   contra = "micontra"
   
   contra_hashed = get_password_hash(contra)

   is_valid = verify_password("micontraa",contra_hashed)
   print(f"contra es valida? {is_valid}")