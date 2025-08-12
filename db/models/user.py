from pydantic import BaseModel # nos permite gestionar modelos a nivel de entidad
from typing import Optional
#Entidad user
class User(BaseModel): # el basemodel lo que hace es dar la capacidad de crear una entidad
    id: Optional[str] = None #opcional, puede que no llegue al llamar al post 
    username: str
    email: str
    