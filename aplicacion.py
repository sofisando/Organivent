# app.py

from apiwsgi import Wsgiclass
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader
from bson import Binary
from webob import Request
from webob.exc import HTTPFound
from waitress import serve
import base64

#aca se conecta la base de datos por el momento

MONGO_URI = 'mongodb://localhost' #en caso de cambiar esto tendriamos que poner la IP y el puerto al que corresponde
client = MongoClient(MONGO_URI) #client es el cursor o la conexion con la base de datos
db = client.Tienda  #db Sofi tienda | Ro Tienda 

# Configura Jinja2 para cargar las plantillas HTML desde un directorio
template_env = Environment(loader=FileSystemLoader("templates"))

app = Wsgiclass()

@app.ruta("/home")
def home(request, response):
    # response.text = "<h3>Pagina Home</h3>"
    response.text = app.template(
    "home.html", context={"title": "Pagina Principal", "user": "Pepita"})

@app.ruta("/productos")
def productos(request, response):  # Renamed the handler to avoid conflict
    # Realiza una consulta a la base de datos
    productos_cursor = db.Productos_prueba.find()

    # Convert the cursor to a list
    productos = list(productos_cursor)

    # Encode image data to base64
    for producto in productos:
        if 'imagen' in producto and producto['imagen']:
            producto['imagen'] = base64.b64encode(producto['imagen']).decode('utf-8')

    # Renderiza el template con los datos de la base de datos
    template = template_env.get_template("productos.html")
    rendered_template = template.render(productos=productos)

    # Configura la respuesta HTTP
    response.text = rendered_template    

    
@app.ruta("/productos/alta")
def alta_producto(request, response):
    if request.method == 'POST':
        # Handle the image upload
        uploaded_file = request.POST.get('imagen')
        if uploaded_file is not None:
            try:
                image_content = uploaded_file.file.read()
            except Exception as e:
                print(f"Error reading image file: {e}")
                # Handle the error appropriately, e.g., return an error page
                return

            # Store the image content in MongoDB
            producto = {
                "nombre_producto": request.POST.get('nombre_producto', ''),
                "descripcion": request.POST.get('descripcion', ''),
                "precio_venta": request.POST.get('precio', ''),
                "imagen": Binary(image_content)
            }

            # Check for negative price
            precio = float(producto["precio_venta"])
            if precio < 0:
                response.text = "Precio no puede ser negativo"
                return

            # Use the correct collection name
            try:
                db.Productos_prueba.insert_one(producto)
            except Exception as e:
                print(f"Error inserting product into the database: {e}")
                # Handle the error appropriately, e.g., return an error page
                return

            # Redirect to the product page or wherever you want
            # response.redirect("/Productos")
            response = HTTPFound(location="/Productos")
            return

    # If not a POST request or no file uploaded, render the form
    with open("templates/alta_producto.html", "r", encoding="utf-8") as file:
        form_html = file.read()

    response.text = form_html


# Handler para la ruta "/productos/atributos/<producto_id>"
@app.ruta("/productos/atributos/<producto_id>")
def producto_atributos(request, response, producto_id):
    # Realiza una consulta a la base de datos para obtener los detalles del producto por su ID
    producto = db.Productos_prueba.find_one({"_id": producto_id})

    # Renderiza el template con los detalles del producto
    template = template_env.get_template("producto_atributos.html")
    rendered_template = template.render(producto=producto)

    # Configura la respuesta HTTP
    response.text = rendered_template


# Handler para la ruta "/producto/<id>"
@app.ruta(r"/producto/(\w+)")
def producto_detalle(request, response, producto_id):
    # Realiza una consulta a la base de datos para obtener los detalles del producto por su ID
    producto = db.Productos_prueba.find_one({"_id": producto_id})

    # Renderiza el template con los detalles del producto
    template = template_env.get_template("producto_detalle.html")
    rendered_template = template.render(producto=producto)

    # Configura la respuesta HTTP
    response.text = rendered_template

@app.ruta("/carrito")
def otra(request, response):
    #response.text = "Otra Pagina"
    response.text = app.template(
    "carrito.html", context={"title": "Carrito", "user": "Pepita"})

@app.ruta("/ultima")
def ultima(request, response):
    response.text = "Ultima Pagina"
    response.image = open('g2.jpg', 'rb').read()


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



if __name__ == '__main__':
    # Utiliza Waitress para servir la aplicación
    serve(app, host='0.0.0.0', port=8000)    