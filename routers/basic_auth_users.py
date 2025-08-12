from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import  BaseModel # nos da mecanismos para que clase se 
# pase a traves de la red de una manera más facil

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm 
# el primero es la clase que se va encargar de gestionar la autenticación (usuario y contraseña)
# el segundo es la forma en la que se va a enviar a nuestra api estos criterios de autenticación
# la forma de que nosotros tenenmos que enviar el usuario y la contraseña,
# la forma en que nuestro backend va a capturar el usuario y la contraseña para saber
# si es un usuario del sistema

router= APIRouter(prefix="/basicauth", 
                  tags=["basicauth"],
                  responses={status.HTTP_404_NOT_FOUND:{"mensaje":"No encontrado"}}) #instancia de nuestra api

oauth2=OAuth2PasswordBearer(tokenUrl="login") #instancia de  (estandar que nos dice como tenemos que trabajar con autenticación normal)
# se pone la url que se encarga de gestionar la autenticación


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
        "password": "123456" # asi no deberia por lo menos se debia hasearla
    },
    
    "josh2":{
        "username":"josh2",
        "full_name":"joseph romero 2",
        "email":"joseph.romero.h2@uni.pe",
        "disabled":True,
        "password": "654321" 
    }
} 


def search_user(username:str): 
    if username in users_db:
        return User(**users_db[username]) 
    #** varios parametros{}
    
    
def search_user_db(username:str): #aconstrumbarse a tipar todos los datos
    if username in users_db:
        return UserDB(**users_db[username]) 
    #** varios parametros

async def current_user(token:str=Depends(oauth2)): # criterio de dependencia
    user= search_user(token) # el token es el propio usuario de bd
    
    if not user:# si no encontramos el usuario
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas",
                            headers={"WWW-Authenticate":"Bearer"})  
        
    if user.disabled:# si el usuario luego de encontrarlo esta activo o no
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")  
        
    return user #retornamos el usuario 
#envio datos, uso un post
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # por ahora el depends, significa que esta operación va a recibir datos
    # pero no depende de nadie.
    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="El usuario no es correcto")
    
    user= search_user_db(form.username) 
    if not form.password == user.password:#la contraseña que ha llegado es igual a la que esta guardada
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta")
    
    # si se ha autenticado correctamente, lo que tiene que devolver el sistema
    # es lo que se llama un access token
    return {"acces_token":user.username,"token_type":"bearer"}
    # el token es encriptado, algo que solo conoce el backend
    #En realidad es para no estar continuamente autenticandonos.
    # Por que? Si ya has pasado una vez el usuario y contraseña
    #pero cada vez que quiero llamar una operación tengo que pasar usuario
    # y contraseña pero esto seria inviable.
    # se le debe pasar algo continuamente al backend pero que no sea
    # usuario y contraseña porque seria una mielda xd
    # por eso si te has autenticado correctamente, el token de autenticación
    # va a ser el propio nombre de usuario y cuando le pases como token de
    # autenticación el propio nombre de usuario va a estar bien.

@router.get("/users/me")# dime cual es mi usaurio
async def me(user:User=Depends(current_user)):# depende de que este autenticado
    # un usuario que no devuelve la contraseña, porque sino habria una brecha de seguridad
    return user