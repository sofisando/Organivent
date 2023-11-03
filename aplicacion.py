# app.py

from apiwsgi import Wsgiclass
from pymongo import MongoClient

#aca se conecta la base de datos por el momento

MONGO_URI = 'mongodb://localhost' #en caso de cambiar esto tendriamos que poner la IP y el puerto al que corresponde

client = MongoClient(MONGO_URI) #client es el cursor o la conexion con la base de datos

db = client.tienda




app = Wsgiclass()

@app.ruta("/home")
def home(request, response):
    # response.text = "<h3>Pagina Home</h3>"
    response.text = app.template(
    "home.html", context={"title": "Pagina Principal", "user": "Pepe Sanchez"})

@app.ruta("/otra")
def otra(request, response):
    response.text = "Otra Pagina"

@app.ruta("/ultima")
def ultima(request, response):
    response.text = "Ultima Pagina"