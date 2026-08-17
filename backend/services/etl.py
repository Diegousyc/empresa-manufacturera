"""
Servicio ETL (Extracción, Transformación, Carga)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLService:
    def __init__(self):
        self.db = db
        self.mensajes = []
    
    def agregar_mensaje(self, mensaje, tipo="info"):
        """Agrega un mensaje al registro de progreso"""
        self.mensajes.append({
            "mensaje": mensaje,
            "tipo": tipo,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(mensaje)
    
    def extraer_datos(self):
        """Extrae datos de MongoDB"""
        self.agregar_mensaje("📥 Iniciando extracción de datos desde MongoDB...")
        
        # Extraer todas las colecciones
        self.agregar_mensaje("  🔍 Extrayendo colección: producciones")
        self.producciones = self.db.to_dataframe('producciones')
        self.agregar_mensaje(f"     ✅ {len(self.producciones)} registros de producción")
        
        self.agregar_mensaje("  🔍 Extrayendo colección: productos")
        self.productos = self.db.to_dataframe('productos')
        self.agregar_mensaje(f"     ✅ {len(self.productos)} registros de productos")
        
        self.agregar_mensaje("  🔍 Extrayendo colección: máquinas")
        self.maquinas = self.db.to_dataframe('maquinas')
        self.agregar_mensaje(f"     ✅ {len(self.maquinas)} registros de máquinas")
        
        self.agregar_mensaje("  🔍 Extrayendo colección: operadores")
        self.operadores = self.db.to_dataframe('operadores')
        self.agregar_mensaje(f"     ✅ {len(self.operadores)} registros de operadores")
        
        self.agregar_mensaje("  🔍 Extrayendo colección: calidad")
        self.calidad = self.db.to_dataframe('calidad')
        self.agregar_mensaje(f"     ✅ {len(self.calidad)} registros de calidad")
        
        self.agregar_mensaje("  🔍 Extrayendo colección: mantenimientos")
        self.mantenimientos = self.db.to_dataframe('mantenimientos')
        self.agregar_mensaje(f"     ✅ {len(self.mantenimientos)} registros de mantenimientos")
        
        self.agregar_mensaje("  🔍 Extrayendo colección: paros")
        self.paros = self.db.to_dataframe('paros')
        self.agregar_mensaje(f"     ✅ {len(self.paros)} registros de paros")
        
        self.agregar_mensaje(f"✅ Extracción completada: {len(self.producciones)} producciones totales")
        return self
    
    def transformar_datos(self):
        """Transforma y limpia los datos"""
        self.agregar_mensaje("🔄 Iniciando transformación de datos...")
        
        # Unir producción con productos
        self.agregar_mensaje("  🔗 Uniendo producción con productos...")
        df = self.producciones.merge(
            self.productos, on='producto_id', how='left', suffixes=('', '_prod')
        )
        self.agregar_mensaje(f"     ✅ Registros después de unión con productos: {len(df)}")
        
        # Unir con máquinas
        self.agregar_mensaje("  🔗 Uniendo con máquinas...")
        df = df.merge(
            self.maquinas, on='maquina_id', how='left', suffixes=('', '_maq')
        )
        self.agregar_mensaje(f"     ✅ Registros después de unión con máquinas: {len(df)}")
        
        # Unir con operadores
        if not self.operadores.empty:
            self.agregar_mensaje("  🔗 Uniendo con operadores...")
            df = df.merge(
                self.operadores, on='operador_id', how='left', suffixes=('', '_op')
            )
            self.agregar_mensaje(f"     ✅ Registros después de unión con operadores: {len(df)}")
        
        # Unir con calidad
        if not self.calidad.empty:
            self.agregar_mensaje("  🔗 Uniendo con calidad...")
            calidad_agg = self.calidad.groupby('produccion_id').agg({
                'calidad': 'mean',
                'defectos': 'sum'
            }).reset_index()
            df = df.merge(calidad_agg, on='produccion_id', how='left')
            self.agregar_mensaje(f"     ✅ Registros después de unión con calidad: {len(df)}")
        
        # Unir con mantenimientos
        if not self.mantenimientos.empty:
            self.agregar_mensaje("  🔗 Uniendo con mantenimientos...")
            mant_agg = self.mantenimientos.groupby('maquina_id').agg({
                'costo': 'sum',
                'duracion': 'mean'
            }).reset_index()
            mant_agg.rename(columns={'costo': 'costo_mantenimiento_total'}, inplace=True)
            df = df.merge(mant_agg, on='maquina_id', how='left')
            self.agregar_mensaje(f"     ✅ Registros después de unión con mantenimientos: {len(df)}")
        
        # Unir con paros
        if not self.paros.empty:
            self.agregar_mensaje("  🔗 Uniendo con paros...")
            paros_agg = self.paros.groupby('maquina_id').agg({
                'duracion_paro': 'sum',
                'causa': 'count'
            }).rename(columns={'causa': 'num_paros'}).reset_index()
            df = df.merge(paros_agg, on='maquina_id', how='left')
            self.agregar_mensaje(f"     ✅ Registros después de unión con paros: {len(df)}")
        
        # Procesar fechas
        self.agregar_mensaje("  📅 Procesando fechas...")
        if 'fecha_inicio' in df.columns:
            df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], errors='coerce')
            if df['fecha_inicio'].isna().all():
                df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], format='ISO8601', errors='coerce')
        
        if 'fecha_fin' in df.columns:
            df['fecha_fin'] = pd.to_datetime(df['fecha_fin'], errors='coerce')
            if df['fecha_fin'].isna().all():
                df['fecha_fin'] = pd.to_datetime(df['fecha_fin'], format='ISO8601', errors='coerce')
        
        # Crear columnas de fecha
        if 'fecha_inicio' in df.columns:
            df['fecha_produccion'] = df['fecha_inicio'].dt.date
            df['hora_inicio'] = df['fecha_inicio'].dt.hour
            df['dia_semana'] = df['fecha_inicio'].dt.dayofweek
            df['mes'] = df['fecha_inicio'].dt.month
            self.agregar_mensaje(f"     ✅ Columnas de fecha creadas")
        
        # Calcular métricas adicionales
        self.agregar_mensaje("  📊 Calculando métricas adicionales...")
        
        df['tasa_defectos'] = df['cantidad_defectuosa'] / df['cantidad_producida']
        df['tasa_defectos'] = df['tasa_defectos'].fillna(0)
        
        if 'tiempo_produccion' in df.columns:
            df['productividad'] = df['cantidad_producida'] / df['tiempo_produccion']
            self.agregar_mensaje(f"     ✅ Productividad calculada")
        
        # Limpiar datos
        self.agregar_mensaje("  🧹 Limpiando datos (eliminando nulos y outliers)...")
        df = self._limpiar_datos(df)
        self.agregar_mensaje(f"     ✅ Registros después de limpieza: {len(df)}")
        
        self.datos_transformados = df
        self.agregar_mensaje(f"✅ Transformación completada: {len(df)} registros, {len(df.columns)} columnas")
        return self
    
    def _limpiar_datos(self, df):
        """Limpia el DataFrame"""
        df_clean = df.copy()
        
        # Eliminar duplicados
        if 'produccion_id' in df_clean.columns:
            duplicados = df_clean.duplicated(subset=['produccion_id']).sum()
            if duplicados > 0:
                self.agregar_mensaje(f"     ⚠️ Eliminando {duplicados} registros duplicados")
            df_clean = df_clean.drop_duplicates(subset=['produccion_id'])
        
        # Columnas numéricas para llenar nulos
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_clean[col].isnull().any():
                nulos = df_clean[col].isnull().sum()
                if nulos > 0:
                    self.agregar_mensaje(f"     📊 Llenando {nulos} valores nulos en {col} con la media")
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
        
        # Eliminar outliers con IQR
        for col in numeric_cols:
            if col not in ['produccion_id', 'producto_id', 'maquina_id', 'operador_id']:
                Q1 = df_clean[col].quantile(0.01)
                Q3 = df_clean[col].quantile(0.99)
                if Q1 != Q3:
                    outliers = ((df_clean[col] < Q1) | (df_clean[col] > Q3)).sum()
                    if outliers > 0:
                        self.agregar_mensaje(f"     📊 Corrigiendo {outliers} outliers en {col}")
                    df_clean[col] = df_clean[col].clip(Q1, Q3)
        
        return df_clean
    
    def cargar_datos(self):
        """Carga los datos transformados"""
        self.agregar_mensaje("💾 Datos transformados listos para análisis")
        return self.datos_transformados

    def ejecutar(self):
        """Ejecuta todo el pipeline ETL"""
        self.agregar_mensaje("🚀 INICIANDO PROCESO ETL")
        self.agregar_mensaje("=" * 50)
        resultado = self.extraer_datos().transformar_datos().cargar_datos()
        self.agregar_mensaje("=" * 50)
        self.agregar_mensaje("✅ ETL COMPLETADO EXITOSAMENTE")
        return resultado
    
    def obtener_mensajes(self):
        """Obtiene todos los mensajes del proceso"""
        return self.mensajes