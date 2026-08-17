"""
Modelo de Producción
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Produccion(BaseModel):
    produccion_id: str
    producto_id: str
    maquina_id: str
    operador_id: str
    lote: str
    cantidad_producida: int
    cantidad_defectuosa: int = 0
    tiempo_produccion: float
    temperatura: Optional[float] = None
    presion: Optional[float] = None
    velocidad: Optional[float] = None
    fecha_inicio: datetime = datetime.now()
    fecha_fin: Optional[datetime] = None
    eficiencia: float = 0.0
    calidad: float = 100.0
    observaciones: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }