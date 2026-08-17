"""
Modelo de Máquinas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Maquina(BaseModel):
    maquina_id: str
    nombre: str
    tipo: str
    modelo: str
    fabricante: str
    año_fabricacion: Optional[int] = None
    capacidad_produccion: float
    consumo_energetico: float = 0.0
    temperatura_operacion: Optional[float] = None
    presion_operacion: Optional[float] = None
    estado: str = "Operativa"
    ultimo_mantenimiento: Optional[datetime] = None
    proximo_mantenimiento: Optional[datetime] = None
    horas_operacion: float = 0
    fecha_instalacion: datetime = datetime.now()
    activa: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }