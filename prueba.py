from apiwsgi import Wsgiclass
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader

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
    # Obtener parámetros desde la URL
    nombre = request.params.get('nombre_producto', '')
    descripcion = request.params.get('descripcion', '')
    precio = request.params.get('precio', '')

    # Crear el diccionario del producto
    producto = {
        "nombre_producto": nombre,
        "descripcion": descripcion,
        "precio": precio,
    }

    # Insertar el producto en la base de datos
    db.Productos.insert_one(producto)
    print("Producto creado con éxito!")

    # Redirigir a la página de productos (o a donde desees)
    response.redirect("/productos")


    #aca adentro deberian estar las funciones, 
    #aca va el python 

#parametrizado de ruta
@app.ruta("/productos/atributos/<producto_id>")
def producto_detalle(request, response, producto_id):
    # Realiza una consulta a la base de datos para obtener los detalles del producto por su ID
    producto = db.productos.find_one({"_id": producto_id})

    # Renderiza el template con los detalles del producto
    template = template_env.get_template("producto_atributos.html")
    rendered_template = template.render(producto=producto)

    # Configura la respuesta HTTP
    response.text = rendered_template



# Handler para la ruta "/producto/<id>"
@app.ruta(r"/producto/(\w+)")
def producto_detalle(request, response, producto_id):
    # Realiza una consulta a la base de datos para obtener los detalles del producto por su ID
    producto = db.productos.find_one({"_id": producto_id})

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
