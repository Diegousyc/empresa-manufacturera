"""
Modelo de Productos
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Producto(BaseModel):
    producto_id: str
    nombre: str
    categoria: str
    descripcion: Optional[str] = None
    precio_unitario: float
    costo_produccion: float
    tiempo_estimado: float
    fecha_creacion: datetime = datetime.now()
    activo: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }