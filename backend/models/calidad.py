"""
Modelo de Calidad
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Calidad(BaseModel):
    calidad_id: str
    produccion_id: str
    producto_id: str
    inspector: str
    fecha_inspeccion: datetime = datetime.now()
    calidad: float
    defectos: int = 0
    defectos_tipo: Optional[str] = None
    especificaciones_cumplidas: bool = True
    acciones_correctivas: Optional[List[str]] = []
    observaciones: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }