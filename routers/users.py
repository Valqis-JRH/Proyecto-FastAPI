"""
Crear un api para usuarios
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel #

#Entidad user
class User(BaseModel): # el basemodel lo que hace es dar la capacidad de crear una entidad
    id:int
    name: str
    surname: str
    url: str
    age:int

users_list= [
    User(id=1, name="joseph", surname="romero", url="https://joseph.dev", age=22),
    User(id=2, name="takemichi", surname="aoya", url="https://take.dev", age=25),
    User(id=3, name="taiyu", surname="hidan", url="https://tayu.dev", age=30)
]



router= APIRouter(prefix="/users", 
                  tags=["users"],
                  responses={404:{"message":"No encontrado"}})
@router.get("/usersjson")
async def usersjson():
    return [{"name":"joseph", "surname":"romero","url":"https://joseph.dev","age":22},
            {"name":"takemichi", "surname":"aoya","url":"https://take.dev","age":25},
            {"name":"taiyu", "surname":"hidan","url":"https://tayu.dev","age":30}]
    #manera que no se deberia hacer


@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}") # en el propio path, pasamos parametro que tenemos que capturar
async def user(id:int):
     return search_user(id)

# Query
# @app.get("/userquery/") # ahora haciendo con el query
@router.get("/user/") # ahora haciendo con el query
async def user(id:int):
    return search_user(id)

# tambien se puede hacer una busqueda por nombre pero eso es más avanzado

def search_user(id:int):
    users=filter (lambda user: user.id==id, users_list)#funcion de orden superiro 
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
# ya no lo arranco en el main, si no en un fichero llamado users.
# el json es la forma en que se comunica
# todo eso debemos escribir, si es un lenguaje orientada a objetos porque no se
# trabaja con objetos que es como se tendria que hacer


# ir por el path y por la query.
# ir por el path, es ir por el propio path de la url
# pero cuando ir por el query es indicarle todo lo que nosotros queramos


# que significa llamar a un parametro por query, significa empezar a igualar
# una clave a un valor dentro de una url. 

# recomendación usar path: parametros fijos
# recomendación usar query: parametros que pueden no ser necesarios para hacer la petición

# Ejemplo tipico de query: imagina que tengamos una base de datos con cientos de usuarios
# no le puedes decir, dame todos los usuarios, te tarda una hora en devolver.
# la aplicación explota, el servidorexplota
# el usuario ya cerro el API y se fue a su casa.
# entonces: seguramente forme parte de la url como una query, que va a formar
# parte de la query, la paginación, como por ejemplo dame las publicaciónes
# del 1 al 10, ... cuando esta llegando a la publicación 7 o 8, entonces le digo
# dame la 11 a la 20 , es algo variable.

# parameteros que pueden ir o no ir para la query
# parametros obligatorios

# ahora hacemos con un post

@router.post("/user/",response_model=User,status_code=201)
async def user(user:User): # ya tenemos una entidad llamada User
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404,detail="El usuario ya existe") # eliges el codigo de error que más se acerca
    else: # si no existe añadimos
        users_list.append(user)
        return user

# FastAPI se encarga de transforma el json  en el usuario (User)

# la respuesta es null
# un post inserta
# un put actualiza

@router.put("/user/")
async def user(user:User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id==user.id: #hemos encontrado el usuario
            users_list[index]= user
            found=True
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

# eliminar
@router.delete("/user/{id}")
async def user(id:int): # no tiene sentido pasarle todo el usuario solo la clave
    # cuando es obligatorio pasamos path
    
    found =False
    for index, saved_user in enumerate(users_list):
        if saved_user.id==id: #hemos encontrado el usuario
            del users_list[index]
            found=True
            
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else:
        return {"elimino": "correctamente"}
# aunque estemos llamando a barra user, no importa si le pasas el body json
# no le hace caso, ya que lo unico que hace es buscar en el path un parametro
# que va a interpretar como un id de tipo entero. al body no le hace caso