# ejecución:  mongod --dbpath "C:\Users\Joseph\Desktop\MongoDB\data"

# encargado de gestionar la conexión a nuestra base de datos llamado db
from pymongo import MongoClient
# Base de datos local MongoDB
#db_client = MongoClient().local  # creamos una variable con la clase mongo_client
# si no le pongo nada se despliega en la url del localhost

# replicamos 
#para una base de datos en el servidor (remota)

db_client = MongoClient("mongodb+srv://joseph:Izana852456@cluster0.mdrsm1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test 


