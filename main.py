#PASO 1:IMPORTAMOS FASTAPI
from fastapi import FastAPI,status
from routers import products,users,basic_auth_users,jwt_auth_users,users_db  # tenemos acceso al fichero de productos
from fastapi.staticfiles import StaticFiles # para recursos estaticos

#PASO 2:INSTANCIAMOS FastAPI
app= FastAPI(title="API de Joseph",
    description="API para ejemplo con FastAPI",
    version="1.0.0")



#routers 
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.mount("/static",StaticFiles(directory="static"),name="static") #operación para montar recursos estaticos


@app.get("/",tags=["main"])

# es una función asincrona, siempre que nosotros llamamos al servidor, 
# la operación que se ejecuta tiene que ser asincrona.


#que es la asincronia?
#si tenemos una petición asincrona, que nosotros desde la web o el movil, llamamos
#al servidor y nuestra aplicación no puede hacer absolutamente nada hasta 
#que retorne algo del servidor, eso seria un caos, pensar cuando aparezca un
#loading en la pantalla, igual esta haciendo esperar la aplicación,
#pero nos esta haciendo esperar por algo muy concreto.
#Porque igual sin esos datos que nos esta dando el servidor no podemos hacer nada
#Especificamos que no sea no sincrono, que sea asincrono, porque puedo llamar al 
#servidor y yo se sobre el servidor lo que va a tardar, y es algo sobre la cual
#no tengo control. Si le digo al servidor, dime cual es mi número de telefono,
#porque estoy autenticado, igual el servidor son milesimas de segundo, pero
#si le digo al servidor cuales son los 500 libros que he leido y dame todos
#los 500 libros. El servidor en lugar de milesimas tarda un segundo.
#¿Que hago durante ese segundo? Me quedo esperando que vengan los datos
#o igual podria seguir mi aplicación haciendo cosas.
#Al dia de hoy, todo es asincrono. Estas navegando por twuiter y despues le 
#aperece una campanita con una aplicación, la aplicación estaba bloqueada?
#Respuesta: No
#Derepente el backend le dijo: tienes una notifación, pintalo en la web de 
#alguna forma, porque son procesos asincronos, por eso intuimos que la 
#función de nuestra api va a ser asincrona, para que funcione y haga lo que
# quiera y tenga que hacer cuando pueda, asincrono, hacen cosas en segundo plano,
# devolviendo datos o haciendo lo que tienene que hacer pero en segundo plano


#PASO 3: TENEMOS UNA OPERACIÓN QUE DICE Hola FastAPI!
async def root(): #falta donde va estar escuchando la llamada a nuestro servidor
    return "Hola FastAPI!"


# ¿CUAL ES EL PROTOCOLO ES LA CUAL UNO SE PUEDE COMUNICAR A TRAVES DE INTERNET?
# EL ESTANDAR ES EL HTTP
# EXISTE UN ESTANDAR QUE NOS PERMITE HABLAR A TRAVES DE LA RED Y ES EL HTTP

# EL GET FORMA PARTE DE LAS OPERACIOENS QUE ESTAN DISPONIBLES DENTRO DE LA 
# COMUNICACIÓN HTTP, 
# ¿QUE ES UN GET?
# PRACTICAMENTE "TODO" LO QUE HACEMOS CUANDO VAMOS A UN EXPLORADOR Y LLAMAMOS 
# A UNA WEB

 
# uvicorn main:app --reload
# uvicorn: servidor
# main: el nombre del fichero
# app: instancia
# reload: argumento
# --reload(recarga el contexto del servidor cada vez que cambiamos algo en este fichero)
# para que no tenga que parar el servidor y vuelva a arrancar
# con que simplemente cambiemos algo en el fichero y lo guardemos, se vuelve a recargar


#@app.get("/") no desplegar en el mismo path
@app.get("/url",tags=["main"])
async def url():
    return { "url_curso":"https://joseph.com/python"}

#aparte de permitir comunicarnos y mover datos, trabaja con codigos
# aparete de devovlernos un json, nos delvuelve un codigo 404 "not found"

# Swagger: nos ayuda con la documentación
# al colocar en el url, /docs , la documentación con Swagger se ha creado 
# de forma automatica
# es decir a medida que programamos, se crea documentación.

# tambien hay redoc, otra herramienta para generar documentación

# a medida que avanzamos, ya no va hacer más comodo, porque tenemos que ir
# al explorador. y si tenemos que hacer peticiones que no sean unicamente un get
# desde el explorador no la podremos lanzar, ya que el explorador en la barra
# de dirección solo acepta get

# opción: postman
# clinte para poder ejecutar peticiones a un API.
# herramienta para interactuar con un  API

# documentación con swuager y redocs

# para probar la API, o bien postman lo descargar o dentro del vs con thunder client

# GET: OBTENER O LEER DATOS

# CRUD: CREATE, READ, UPDATE, DELETE . OPERACIONES BASICAS QUE SE PUEDE IMPLEMENTAR
# CONTRA UN USAURIO


