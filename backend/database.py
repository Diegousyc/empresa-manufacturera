"""
Conexión y operaciones con MongoDB
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa la conexión"""
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Establece conexión con MongoDB"""
        try:
            # Intentar URL desde entorno si existe
            import os
            uri = os.getenv('MONGO_URI') or os.getenv('MONGODB_URI') or "mongodb://localhost:27017/"
            # Conexión
            self.client = MongoClient(uri)
            self.client.admin.command('ping')
            self.db = self.client["production_industrial"]
            logger.info("✅ Conectado a MongoDB exitosamente")
            
            # Verificar colecciones
            collections = self.db.list_collection_names()
            logger.info(f"📁 Colecciones: {collections}")
            
        except ConnectionFailure as e:
            logger.error(f"❌ Error de conexión a MongoDB: {e}")
            # No propagar la excepción para permitir que la API arranque en modo degradado.
            self.client = None
            self.db = None
            logger.info("⚠️ Iniciando en modo degradado: la base de datos no está disponible.")
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar a MongoDB: {e}")
            self.client = None
            self.db = None
            logger.info("⚠️ Iniciando en modo degradado: la base de datos no está disponible.")
    
    def get_collection(self, name):
        """Obtiene una colección"""
        if self.db is None:
            raise RuntimeError('Base de datos no conectada')
        return self.db[name]
    
    def insert_one(self, collection, data):
        """Inserta un documento"""
        if self.db is None:
            raise RuntimeError('Base de datos no conectada')
        if '_id' in data:
            del data['_id']
        result = self.db[collection].insert_one(data)
        return result.inserted_id
    
    def insert_many(self, collection, data):
        """Inserta múltiples documentos"""
        if self.db is None:
            raise RuntimeError('Base de datos no conectada')
        for doc in data:
            if '_id' in doc:
                del doc['_id']
        result = self.db[collection].insert_many(data)
        return result.inserted_ids
    
    def find(self, collection, query={}, limit=0, sort=None):
        """Busca documentos

        Parámetros:
        - collection: nombre de la colección
        - query: filtro MongoDB
        - limit: límite de resultados (0 = sin límite)
        - sort: lista de tuplas para ordenar, p.ej. [('fecha_inicio', -1)]
        """
        if self.db is None:
            return []
        cursor = self.db[collection].find(query)
        if sort:
            cursor = cursor.sort(sort)
        if limit > 0:
            cursor = cursor.limit(limit)
        data = list(cursor)
        for doc in data:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        return data
    
    def find_one(self, collection, query):
        """Busca un documento"""
        if self.db is None:
            return None
        doc = self.db[collection].find_one(query)
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return doc
    
    def update_one(self, collection, query, data):
        """Actualiza un documento"""
        if self.db is None:
            raise RuntimeError('Base de datos no conectada')
        if '_id' in data:
            del data['_id']
        result = self.db[collection].update_one(query, {"$set": data})
        return result.modified_count
    
    def delete_one(self, collection, query):
        """Elimina un documento"""
        if self.db is None:
            raise RuntimeError('Base de datos no conectada')
        result = self.db[collection].delete_one(query)
        return result.deleted_count
    
    def to_dataframe(self, collection, query={}):
        """Convierte una colección a DataFrame"""
        data = self.find(collection, query)
        if data:
            df = pd.DataFrame(data)
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
            return df
        return pd.DataFrame()
    
    def count(self, collection, query={}):
        """Cuenta documentos"""
        if self.db is None:
            return 0
        return self.db[collection].count_documents(query)

    

# Instancia global
db = Database()