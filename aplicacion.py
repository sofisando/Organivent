# app.py

from apiwsgi import Wsgiclass
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader
from bson import Binary
import os
#import base64 #ver si lo usamos o sacar (imagenes)
from waitress import serve

#aca se conecta la base de datos por el momento

MONGO_URI = 'mongodb://localhost' #en caso de cambiar esto tendriamos que poner la IP y el puerto al que corresponde
client = MongoClient(MONGO_URI) #client es el cursor o la conexion con la base de datos
db = client.tienda  #db Sofi tienda | Ro Tienda 

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
    response.image = open('g2.jpg', 'rb').read()

@app.ruta("/obtener_documentos")
#def ultima(request, response):
#    response.text = "Ultima Pagina"
#    image_path = '/static/imagenes/2.jpg'
#    image_content = db['your_images_collection'].find_one({'path': image_path})['content']
#    response.content_type = 'image/jpeg'
#    response.body = image_content

#def ultima(request, response):
#    response.text = "Ultima Pagina"
#    image_path = '/static/imagenes/2.jpg'
#    
#    # Read the image file as binary data
#    image_file_path = os.path.join(os.getcwd(), 'static', 'imagenes', '2.jpg')
#
#    with open(image_file_path, 'rb') as image_file:
#    #with open('path/to/your/images' + image_path, 'rb') as image_file:
#
    # Store the image content in MongoDB
#    db['your_images_collection'].insert_one({'path': image_path, 'content': Binary(image_content)})
#
#    # Set the image content in the response
#    response.content_type = 'image/jpeg'
#    response.body = image_content

def ultima(request, response):
    if request.method == 'POST':
        # Handle the image upload / Carga de imagen
        uploaded_file = request.files.get('imagen')
        if uploaded_file:
            image_content = uploaded_file.file.read()

            # Store the image content in MongoDB
            db['Productos'].insert_one({'imagen': Binary(image_content)})

            # Set the image content in the response
            response.content_type = 'image/jpeg'
            response.body = image_content
            return

    # If not a POST request or no file uploaded, render a form
    # Si no es una solicitud POST o no se ha subido ningún archivo, renderice un formulario
    response.text = """
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="imagen" accept="image/*">
        <input type="submit" value="Subir Imagen">
    </form>
    """

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

@app.ruta("/cargar_imagen")
def cargar_imagen(request, response):
    if request.method == 'POST':
        try:
            # Obtener datos de la solicitud POST
            name = request.form.get('name', '')
            image_data = request.form.get('image', '')

            # Decodificar la imagen Base64
            decoded_image = base64.b64decode(image_data)

            # Guardar la imagen en MongoDB
            db.products.insert_one({
                'name': name,
                'image': decoded_image
            })

            response.json({"message": "Image uploaded successfully!"}, status_code=201)

        except Exception as e:
            print(e)
            response.json({"message": "Error uploading image."}, status_code=500)
    else:
        response.json({"message": "Invalid request method."}, status_code=405)

if __name__ == '__main__':
    # Utiliza Waitress para servir la aplicación
    serve(app, host='0.0.0.0', port=8000)    