from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
print(cliente.list_database_names());