"""
Modelo de Mantenimiento
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Mantenimiento(BaseModel):
    mantenimiento_id: str
    maquina_id: str
    tipo: str  # Preventivo, Correctivo, Predictivo
    descripcion: str
    fecha_inicio: datetime = datetime.now()
    fecha_fin: Optional[datetime] = None
    duracion: Optional[float] = None
    tecnico: str
    costo: float = 0.0
    piezas_reemplazadas: Optional[List[str]] = []
    observaciones: Optional[str] = None
    completado: bool = False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }