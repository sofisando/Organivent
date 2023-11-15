from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from pymongo import MongoClient
import base64
from waitress import serve  # Importa la función serve de Waitress

# Conecta con la base de datos MongoDB (reemplaza 'mongodb://localhost:27017/your_database_name' con tu cadena de conexión real)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['tienda']

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))

        name = params.get('name', [''])[0]
        image_data = params.get('image', ['/static/imagenes/1.jpg'])[0]

        try:
            # Decodifica la imagen Base64
            decoded_image = base64.b64decode(image_data)

            # Guarda la imagen en MongoDB
            db.products.insert_one({
                'name': name,
                'image': decoded_image
            })

            self._send_response(201, '{"message": "Image uploaded successfully!"}')

        except Exception as e:
            print(e)
            self._send_response(500, '{"message": "Error uploading image."}')

if __name__ == '__main__':
    # Usa Waitress para servir la aplicación en lugar del servidor HTTP incorporado
    serve(RequestHandler, host='0.0.0.0', port=8000)

