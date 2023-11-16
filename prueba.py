from apiwsgi import Wsgiclass
from pymongo import MongoClient
from bson import Binary
from webob import Request
from webob.exc import HTTPFound
from waitress import serve
from jinja2 import Environment, FileSystemLoader
#from werkzeug.utils import secure_filename   libreria para manejar mas seguro los archivos

# Conexión a la base de datos MongoDB
MONGO_URI = 'mongodb://localhost'
client = MongoClient(MONGO_URI)
db = client.tienda  #db Sofi tienda | Ro Tienda 

# Configura Jinja2 para cargar las plantillas HTML desde un directorio
template_env = Environment(loader=FileSystemLoader("templates"))

app = Wsgiclass()

# Handler para la ruta "/productos"
@app.ruta("/productos")
def productos(request, response):
    # Realiza una consulta a la base de datos
    productos = db.Productos.find()

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

            # Use the correct collection name
            try:
                db.Productos.insert_one(producto)
                print("Producto con imagen creado con éxito!")
            except Exception as e:
                print(f"Error inserting product into the database: {e}")
                # Handle the error appropriately, e.g., return an error page
                return

            # Redirect to the product page or wherever you want
            # response.redirect("/Productos")
            response = HTTPFound(location="/Productos")
            return

    # If not a POST request or no file uploaded, render the form
    response.text = """
    <form method="post" enctype="multipart/form-data">
        Nombre del Producto: <input type="text" name="nombre_producto" required><br>
        Descripción: <input type="text" name="descripcion" required><br>
        Precio: <input type="number" name="precio" required><br>
        Imagen: <input type="file" name="imagen" accept="image/*" required><br>
        <input type="submit" value="Alta de Producto">
    </form>
    """


#parametrizado de ruta
@app.ruta("/productos/atributos/<producto_id>")
def producto_detalle(request, response, producto_id):
    # Realiza una consulta a la base de datos para obtener los detalles del producto por su ID
    producto = db.Productos.find_one({"_id": producto_id})

    # Renderiza el template con los detalles del producto
    template = template_env.get_template("producto_atributos.html")
    rendered_template = template.render(producto=producto)

    # Configura la respuesta HTTP
    response.text = rendered_template



# Handler para la ruta "/producto/<id>"
@app.ruta(r"/producto/(\w+)")
def producto_detalle(request, response, producto_id):
    # Realiza una consulta a la base de datos para obtener los detalles del producto por su ID
    producto = db.Productos.find_one({"_id": producto_id})

    # Renderiza el template con los detalles del producto
    template = template_env.get_template("producto_detalle.html")
    rendered_template = template.render(producto=producto)

    # Configura la respuesta HTTP
    response.text = rendered_template

# Resto de tus handlers
@app.ruta("/home")
def home(request, response):
    response.text = app.template(
        "home.html", context={"title": "Pagina Principal", "user": "Pepita"})

@app.ruta("/carrito")
def otra(request, response):
    response.text = app.template(
        "carrito.html", context={"title": "Carrito", "user": "Pepita"})

@app.ruta("/ultima")
def ultima(request, response):
    response.text = "Ultima Pagina"
