import requests
import base64

# URL del servidor
server_url = 'http://localhost:8000'

# Nombre y ruta de la imagen que deseas cargar
image_path = '/static/imagenes/1.jpg' #'/path/to/your/image.jpg'

# Lee la imagen en formato binario
with open(image_path, 'rb') as image_file:
    # Codifica la imagen en base64
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Parámetros del formulario
form_data = {
    'name': 'Product Name',
    'image': encoded_image
}

# Realiza la solicitud POST al servidor
response = requests.post(server_url, data=form_data)

# Imprime la respuesta del servidor
print(response.text)