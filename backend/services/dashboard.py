"""
Servicio de Dashboard y Visualización
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardService:
    def __init__(self):
        self.figures = []
    
    def crear_dashboard_completo(self, df):
        """Crea un dashboard completo con Plotly"""
        # Subplots: 3 filas, 2 columnas
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Producción por Máquina',
                'Calidad Promedio por Producto',
                'Distribución de Eficiencia',
                'Tasa de Defectos por Máquina',
                'Tendencia de Producción',
                'Correlación de Variables'
            )
        )
        
        # 1. Producción por máquina
        prod_maquina = df.groupby('maquina_id')['cantidad_producida'].sum().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(x=prod_maquina.values, y=prod_maquina.index, orientation='h', name='Producción'),
            row=1, col=1
        )
        
        # 2. Calidad por producto
        calidad_producto = df.groupby('producto_id')['calidad'].mean().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=calidad_producto.index, y=calidad_producto.values, name='Calidad'),
            row=1, col=2
        )
        
        # 3. Distribución de eficiencia
        fig.add_trace(
            go.Histogram(x=df['eficiencia'], nbinsx=30, name='Eficiencia'),
            row=2, col=1
        )
        
        # 4. Tasa de defectos por máquina
        defectos_maquina = df.groupby('maquina_id')['tasa_defectos'].mean().sort_values()
        fig.add_trace(
            go.Bar(x=defectos_maquina.index, y=defectos_maquina.values, name='Tasa Defectos'),
            row=2, col=2
        )
        
        # 5. Tendencia de producción
        df['fecha_produccion'] = pd.to_datetime(df['fecha_produccion'])
        prod_tendencia = df.groupby('fecha_produccion')['cantidad_producida'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=prod_tendencia['fecha_produccion'], y=prod_tendencia['cantidad_producida'], 
                      mode='lines+markers', name='Tendencia'),
            row=3, col=1
        )
        
        # 6. Matriz de correlación (simplificada)
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        corr = df[numeric_cols].corr()
        
        # Seleccionar top 5 correlaciones
        corr_top = corr.iloc[:5, :5] if len(corr) >= 5 else corr
        
        fig.add_trace(
            go.Heatmap(z=corr_top.values, x=corr_top.columns, y=corr_top.index, 
                      colorscale='RdBu', zmin=-1, zmax=1),
            row=3, col=2
        )
        
        fig.update_layout(height=1200, width=1500, showlegend=True)
        fig.update_layout(title_text="Dashboard de Producción Industrial")
        
        return fig
    
    def crear_grafico_eficiencia(self, df):
        """Crea gráfico de eficiencia por máquina"""
        fig = px.box(df, x='maquina_id', y='eficiencia', color='maquina_id',
                    title='Distribución de Eficiencia por Máquina',
                    labels={'maquina_id': 'Máquina', 'eficiencia': 'Eficiencia (%)'})
        return fig
    
    def crear_grafico_calidad_tiempo(self, df):
        """Crea gráfico de calidad en el tiempo"""
        df['fecha_produccion'] = pd.to_datetime(df['fecha_produccion'])
        df_agrupado = df.groupby('fecha_produccion').agg({
            'calidad': 'mean',
            'cantidad_producida': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_agrupado['fecha_produccion'],
            y=df_agrupado['calidad'],
            mode='lines+markers',
            name='Calidad',
            line=dict(color='green')
        ))
        
        fig.add_trace(go.Scatter(
            x=df_agrupado['fecha_produccion'],
            y=df_agrupado['cantidad_producida'],
            mode='lines+markers',
            name='Producción',
            yaxis='y2',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title='Calidad y Producción en el Tiempo',
            xaxis_title='Fecha',
            yaxis_title='Calidad (%)',
            yaxis2=dict(
                title='Cantidad Producida',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified'
        )
        
        return fig
    
    def crear_grafico_defectos(self, df):
        """Crea gráfico de defectos por tipo"""
        if 'defectos_tipo' in df.columns:
            # Si tenemos datos de tipo de defectos
            fig = px.pie(df, names='defectos_tipo', title='Distribución de Defectos')
        else:
            # Usar defectos por producto
            defectos_prod = df.groupby('producto_id')['cantidad_defectuosa'].sum()
            fig = px.pie(values=defectos_prod.values, names=defectos_prod.index,
                        title='Defectos por Producto')
        
        return fig