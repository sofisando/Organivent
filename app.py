from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost' #en caso de cambiar esto tendriamos que poner la IP y el puerto al que corresponde

client = MongoClient(MONGO_URI) #client es el cursor o la conexion con la base de datos

db = client.tienda

print(db.Productos.find())