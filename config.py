"""
Configuración del sistema
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "produccion_industrial")
    
    # Modelos
    MODEL_PATH = "backend/models/saved/"
    
    # Dataset
    DATASET_PATH = "datasets/produccion.csv"
    
    # Producción
    PRODUCTION_THRESHOLD = 1000  # Umbral para clasificación
    
    # Features relevantes
    FEATURES = [
        'cantidad_producida',
        'tiempo_produccion',
        'temperatura',
        'presion',
        'velocidad',
        'defectos'
    ]
    
    TARGET = 'calidad'

config = Config()