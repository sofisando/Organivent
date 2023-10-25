from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Conéctate a la base de datos MongoDB
client = MongoClient('mongodb://tu_usuario:tu_contraseña@localhost:27017/tu_base_de_datos')
db = client.tu_base_de_datos  # Reemplaza "tu_base_de_datos" con el nombre de tu base de datos

# Función para crear un nuevo pedido
def crear_pedido(usuario_id, productos, metodo_pago):
    pedido = {
        "usuario": usuario_id,
        "productos": productos,
        "estado": "Pendiente",
        "metodo_pago": metodo_pago,
        "fecha": datetime.now()
    }
    db.pedidos.insert_one(pedido)
    print("Pedido creado con éxito!")

# Función para obtener y mostrar información de un pedido
def mostrar_pedido(pedido_id):
    pedido = db.pedidos.find_one({"_id": ObjectId(pedido_id)})
    if pedido:
        print("Información del Pedido:")
        print(f"ID del Pedido: {pedido['_id']}")
        print(f"Usuario: {pedido['usuario']}")
        print(f"Productos: {pedido['productos']}")
        print(f"Estado: {pedido['estado']}")
        print(f"Método de Pago: {pedido['metodo_pago']}")
        print(f"Fecha: {pedido['fecha']}")
    else:
        print("Pedido no encontrado.")

# Ejemplo de uso
if __name__ == "__main__":
    # Crea un nuevo pedido
    usuario_id = "ID del Usuario"  # Reemplaza con el ID del usuario que hace el pedido
    productos = [
        {"producto_id": "product_id_1", "cantidad": 2},
        {"producto_id": "product_id_2", "cantidad": 1}
    ]
    metodo_pago = {
        "tipo": "Tarjeta de Crédito",
        "id_metodo_pago": "ID de la Tarjeta de Crédito del Usuario"
    }
    crear_pedido(usuario_id, productos, metodo_pago)

    # Muestra información del pedido
    pedido_id = "ID del Pedido Creado"  # Reemplaza con el ID del pedido que quieres mostrar
    mostrar_pedido(pedido_id)
