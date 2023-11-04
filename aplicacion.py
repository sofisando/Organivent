# app.py

from apiwsgi import Wsgiclass
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader

#aca se conecta la base de datos por el momento

MONGO_URI = 'mongodb://localhost' #en caso de cambiar esto tendriamos que poner la IP y el puerto al que corresponde
client = MongoClient(MONGO_URI) #client es el cursor o la conexion con la base de datos
db = client.tienda  #db Sofi

# Configura Jinja2 para cargar las plantillas HTML desde un directorio
template_env = Environment(loader=FileSystemLoader("templates"))

app = Wsgiclass()

@app.ruta("/home")
def home(request, response):
    # response.text = "<h3>Pagina Home</h3>"
    response.text = app.template(
    "home.html", context={"title": "Pagina Principal", "user": "Pepita"})

@app.ruta("/carrito")
def otra(request, response):
    #response.text = "Otra Pagina"
    response.text = app.template(
    "carrito.html", context={"title": "Carrito", "user": "Pepita"})

@app.ruta("/ultima")
def ultima(request, response):
    response.text = "Ultima Pagina"

@app.ruta("/obtener_documentos")

def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    if path == '/':
        # Accede a una colección en la base de datos
        collection = db["Clientes"]  # Reemplaza con el nombre de tu colección

        # Recupera los datos de la colección (puedes personalizar esta parte según tus necesidades)
        datos = list(collection.find())

        # Renderiza una plantilla HTML con los datos
        template = template_env.get_template("template.html")  # Reemplaza con el nombre de tu plantilla
        rendered_template = template.render(datos=datos)

        start_response('200 OK', [('Content-type', 'text/html')])
        return [rendered_template.encode('utf-8')]
    elif path.startswith('/static/'):
        # Si se solicitan recursos estáticos, como CSS o JavaScript, sirve los archivos desde la carpeta "static"
        static_path = path[1]



@app.ruta("/")
def home(request, response):
    # response.text = "<h3>Pagina Home</h3>"
    response.text = app.template(
    "viajes.html")