### Users API con autorización OAuth2 JWT ###

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import  BaseModel 
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm 
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone

ALGORITHM="HS256" #ALGORITMO DE ENCRIPTACIÓN
ACCESS_TOKEN_DURATION= 1 # DURACIÓN DEL TOKEN
SECRET= "79c10ff09c8dc8048b7ba528c96d3dd88aa50ffed53cd32fd693a6497e93d73c"


router= APIRouter(prefix="/jwtauth", 
                  tags=["jwtauth"],
                  responses={status.HTTP_404_NOT_FOUND:{"mensaje":"No encontrado"}})

oauth2=OAuth2PasswordBearer(tokenUrl="login") # autenticación por usuario y contraseña
crypt= CryptContext(schemes=["bcrypt"])

class User(BaseModel): # el basemodel lo que hace es dar la capacidad de crear una entidad
    username: str
    full_name: str
    email : str
    disabled:bool
    
class UserDB(User): # usuario de base de datos
    password: str

users_db={
    "josh":{
        "username":"josh",
        "full_name":"joseph romero",
        "email":"joseph.romero.h@uni.pe",
        "disabled":False,
        "password": "$2a$12$vyUk7DmdD6Lo/h4/eoN9Y.qcz4DSCk2NjPapK6fBves62G1AEQpJK" # asi no deberia por lo menos se debia hasearla
    },
    
    "josh2":{
        "username":"josh2", 
        "full_name":"joseph romero 2",
        "email":"joseph.romero.h2@uni.pe",
        "disabled":True,
        "password": "$2a$12$hOqT83F/kWUjFVv4gR8Jc.K8iiWz4j3HOzGq.TyUcNoCxy2bKEkky" 
    }
} 
def search_user_db(username:str): #aconstrumbarse a tipar todos los datos
    if username in users_db:
        return UserDB(**users_db[username]) 
    #** varios parametros
    
def search_user(username:str): 
    if username in users_db:
        return User(**users_db[username]) 
    
        
async def auth_user(token:str= Depends(oauth2)):
    #obtenemos el token (Proceso de validación de token)
    exception=  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas",
                            headers={"WWW-Authenticate":"Bearer"}) 
    try:
        # desincriptamos y sacamos el nombre del usuario
        username= jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None: 
             raise exception
        
        
    except JWTError:
        # si no encontramos el usuario
        raise exception  
        
    # si no ha sucedido ninguna excepción
    return search_user(username)  #buscamos


async def current_user(user:User =Depends(auth_user)): # criterio de dependencia
    
    if user.disabled:# si el usuario luego de encontrarlo esta activo o no
        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")  
        
    return user #si no esta desabilitado, retornamos el usuario  
 
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # por ahora el depends, significa que esta operación va a recibir datos
    # pero no depende de nadie.
    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="El usuario no es correcto")
    
    user= search_user_db(form.username) 
    
    
    
    if not crypt.verify(form.password,user.password):#contraseña del formulario y la otra encriptada
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta")
    
    access_token_expiration= timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    expire= datetime.now(timezone.utc) + access_token_expiration
    
    access_token={"sub":user.username, "exp":expire} #algo encriptado que inicialmente es un JSON
    # si se ha autenticado correctamente, lo que tiene que devolver el sistema
    # es lo que se llama un access token
    return {"acces_token":jwt.encode(access_token,SECRET, algorithm=ALGORITHM),"token_type":"bearer"}


#devolvemos 
@router.get("/users/me")# dime cual es mi usaurio
async def me(user:User=Depends(current_user)):# depende de que este autenticado
    # un usuario que no devuelve la contraseña, porque sino habria una brecha de seguridad
    return user
