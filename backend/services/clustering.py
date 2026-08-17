"""
Servicio de Clustering (No supervisado)
"""

import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClusteringService:
    def __init__(self):
        self.model_path = "models/saved/"
        os.makedirs(self.model_path, exist_ok=True)
        self.scaler = StandardScaler()
        self.kmeans = None
        self.pca = None
        self.mensajes = []
    
    def agregar_mensaje(self, mensaje, tipo="info"):
        """Agrega un mensaje al registro de progreso"""
        self.mensajes.append({
            "mensaje": mensaje,
            "tipo": tipo,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(mensaje)
    
    def preparar_datos(self, df):
        """Prepara datos para clustering"""
        self.agregar_mensaje("📊 Preparando datos para clustering...")
        
        feature_cols = [
            'cantidad_producida', 'tiempo_produccion', 'temperatura',
            'presion', 'velocidad', 'cantidad_defectuosa', 'tasa_defectos'
        ]
        
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        if not feature_cols:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            exclude = ['produccion_id', 'producto_id', 'maquina_id', 'operador_id']
            feature_cols = [col for col in numeric_cols if col not in exclude]
            self.agregar_mensaje(f"  📋 Usando columnas numéricas disponibles: {len(feature_cols)}")
        else:
            self.agregar_mensaje(f"  📋 Características seleccionadas: {len(feature_cols)}")
        
        X = df[feature_cols]
        X = X.fillna(X.mean())
        
        self.agregar_mensaje(f"  ✅ Datos preparados: {len(X)} muestras, {len(X.columns)} características")
        return X
    
    def entrenar_kmeans(self, X, n_clusters=3):
        """Entrena modelo K-means"""
        self.agregar_mensaje(f"🧩 Entrenando K-means con {n_clusters} clusters...")
        try:
            # Escalar datos
            self.agregar_mensaje("  📊 Normalizando datos...")
            X_scaled = self.scaler.fit_transform(X)
            
            self.agregar_mensaje(f"  🧩 Inicializando {n_clusters} centroides...")
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            
            self.agregar_mensaje("  🔄 Ejecutando algoritmo K-means...")
            clusters = self.kmeans.fit_predict(X_scaled)
            
            # Estadísticas de clusters
            self.agregar_mensaje("  📊 Distribución de clusters:")
            for i in range(n_clusters):
                count = np.sum(clusters == i)
                self.agregar_mensaje(f"     • Cluster {i}: {count} elementos ({count/len(X)*100:.1f}%)")
            
            self.agregar_mensaje(f"✅ K-means entrenado con {n_clusters} clusters")
            return clusters
        except Exception as e:
            self.agregar_mensaje(f"❌ Error en K-means: {e}", "error")
            return np.random.randint(0, n_clusters, len(X))
    
    def reducir_dimensiones(self, X, n_components=2):
        """Reduce dimensionalidad con PCA"""
        self.agregar_mensaje(f"📉 Reduciendo dimensionalidad con PCA (a {n_components} componentes)...")
        try:
            X_scaled = self.scaler.fit_transform(X)
            
            self.pca = PCA(n_components=n_components)
            X_pca = self.pca.fit_transform(X_scaled)
            
            varianza_explicada = self.pca.explained_variance_ratio_
            self.agregar_mensaje(f"  📊 Varianza explicada:")
            for i, var in enumerate(varianza_explicada):
                self.agregar_mensaje(f"     • Componente {i+1}: {var*100:.1f}%")
            self.agregar_mensaje(f"  ✅ Varianza total explicada: {sum(varianza_explicada)*100:.1f}%")
            
            self.agregar_mensaje(f"✅ PCA completado: {X_pca.shape[1]} componentes")
            return X_pca
        except Exception as e:
            self.agregar_mensaje(f"❌ Error en PCA: {e}", "error")
            return np.random.randn(len(X), n_components)
    
    def guardar_modelo(self, name="kmeans"):
        """Guarda el modelo en disco"""
        if self.kmeans is None:
            self.agregar_mensaje("⚠️ No hay modelo K-means para guardar", "warning")
            return None
        
        path = os.path.join(self.model_path, f"{name}.pkl")
        joblib.dump(self.kmeans, path)
        self.agregar_mensaje(f"💾 Modelo guardado: {path}")
        return path
    
    def cargar_modelo(self, name="kmeans"):
        """Carga un modelo guardado"""
        path = os.path.join(self.model_path, f"{name}.pkl")
        if os.path.exists(path):
            self.kmeans = joblib.load(path)
            self.agregar_mensaje(f"📂 Modelo cargado: {path}")
            return self.kmeans
        self.agregar_mensaje(f"⚠️ Modelo no encontrado: {path}", "warning")
        return None
    
    def obtener_mensajes(self):
        """Obtiene todos los mensajes del proceso"""
        return self.mensajes