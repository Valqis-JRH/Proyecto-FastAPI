"""
Crear un api para base datos usuarios
"""

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client #para trabajar con base datos se importa el cliente de base de datos
from db.schemas.user import user_schema, users_schema
from bson import ObjectId # creamos un ObjectId

router= APIRouter(
                  prefix="/userdb", 
                  tags=["userdb"],
                  responses={status.HTTP_404_NOT_FOUND:{"mensaje":"No encontrado"}}
                  )



# cambiamos el path porque en el users.py se repetiria si colocamos lo mismo
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Path
@router.get("/{id}") # en el propio path, pasamos parametro que tenemos que capturar
async def user(id:str):
     return search_user("_id",ObjectId(id))

# Query
# @app.get("/userquery/") # ahora haciendo con el query
@router.get("/") # ahora haciendo con el query
async def user(id:str):
    return search_user("_id",ObjectId(id))

# tambien se puede hacer una busqueda por nombre pero eso es más avanzado


# generico, pasamos el criterio de busqueda y la clave
def search_user(field:str,key):
    try:
        # primero buscarlo en base de datos
        user=  db_client.users.find_one({field:key})
        # si lo encontramos realizamos la transformación a diccionario
        # y creamos el objeto Users
        return User(**user_schema(user))
        
    except:
        return {"error": "No se ha encontrado el usuario"}
    






# ahora hacemos con un post

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user:User): # ya tenemos una entidad llamada User
    if type(search_user("email",user.email)) == User:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="El usuario ya existe") # eliges el codigo de error que más se acerca

    user_dict= dict(user) #transformar el modelo usuario en diccionario
    del user_dict["id"] #eliminar el campo id ya que va a salir como un null, ya que no vamos a ingresar nada
    id= db_client.users.insert_one(user_dict).inserted_id
    #Operación de creación en base de datos y el id con el que se ha insertado
    new_user=user_schema(db_client.users.find_one({"_id":id}))
    #el nombre de la clave unica que crea mongodb no es id sino _id
    #user_schema: nos crea el objeto que queremos retornar
    
    return User(**new_user) # pasar todos los campos del new_user


# actulizar
@router.put("/",response_model=User)
async def user(user:User):
    user_dict= dict(user)
    del user_dict["id"] # el id es algo que no puede cambiar (no actualizar)
    try:

        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id",ObjectId(user.id))

# eliminar
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str): 
    
    found =db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    

    if not found:
        return {"error": "No se ha eliminado el usuario"}
  