"""
Rutas para Máquinas
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import logging

# Importar el modelo y la base de datos
from models.maquinas import Maquina
from database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_maquinas(
    limit: int = Query(100, ge=1, le=1000),
    estado: Optional[str] = None,
    tipo: Optional[str] = None
):
    """Obtiene todas las máquinas"""
    try:
        query = {}
        if estado:
            query['estado'] = estado
        if tipo:
            query['tipo'] = tipo
        
        data = db.find('maquinas', query, limit)
        
        # Contar total sin límite para estadísticas
        total = db.count('maquinas', query)
        
        return {
            "data": data, 
            "count": len(data),
            "total": total,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error en get_maquinas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{maquina_id}")
async def get_maquina(maquina_id: str):
    """Obtiene una máquina por ID"""
    try:
        data = db.find_one('maquinas', {'maquina_id': maquina_id})
        if not data:
            raise HTTPException(status_code=404, detail="Máquina no encontrada")
        return {"data": data, "status": "success"}
    except Exception as e:
        logger.error(f"Error en get_maquina: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_maquina(maquina: Maquina):
    """Crea una nueva máquina"""
    try:
        # Convertir a diccionario
        data = maquina.dict()
        
        logger.info(f"📝 Datos recibidos: {data}")
        
        # Convertir fechas a string para MongoDB
        if 'fecha_instalacion' in data and data['fecha_instalacion']:
            if hasattr(data['fecha_instalacion'], 'isoformat'):
                data['fecha_instalacion'] = data['fecha_instalacion'].isoformat()
            else:
                data['fecha_instalacion'] = str(data['fecha_instalacion'])
        
        if 'ultimo_mantenimiento' in data and data['ultimo_mantenimiento']:
            if hasattr(data['ultimo_mantenimiento'], 'isoformat'):
                data['ultimo_mantenimiento'] = data['ultimo_mantenimiento'].isoformat()
            else:
                data['ultimo_mantenimiento'] = str(data['ultimo_mantenimiento'])
        
        if 'proximo_mantenimiento' in data and data['proximo_mantenimiento']:
            if hasattr(data['proximo_mantenimiento'], 'isoformat'):
                data['proximo_mantenimiento'] = data['proximo_mantenimiento'].isoformat()
            else:
                data['proximo_mantenimiento'] = str(data['proximo_mantenimiento'])
        
        # Asegurar que campos requeridos existan
        if 'activa' not in data:
            data['activa'] = True
        
        if 'horas_operacion' not in data:
            data['horas_operacion'] = 0
        
        # Asegurar que estado tenga un valor válido
        if 'estado' not in data or not data['estado']:
            data['estado'] = 'Operativa'
        
        # Insertar en la base de datos
        result = db.insert_one('maquinas', data)
        
        logger.info(f"✅ Máquina insertada con ID: {result}")
        
        return {
            "message": "Máquina creada exitosamente",
            "id": str(result),
            "data": data,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"❌ Error en create_maquina: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{maquina_id}")
async def update_maquina(maquina_id: str, maquina: Maquina):
    """Actualiza una máquina"""
    try:
        data = maquina.dict()
        
        # Convertir fechas a string
        if 'fecha_instalacion' in data and data['fecha_instalacion']:
            if hasattr(data['fecha_instalacion'], 'isoformat'):
                data['fecha_instalacion'] = data['fecha_instalacion'].isoformat()
        
        if 'ultimo_mantenimiento' in data and data['ultimo_mantenimiento']:
            if hasattr(data['ultimo_mantenimiento'], 'isoformat'):
                data['ultimo_mantenimiento'] = data['ultimo_mantenimiento'].isoformat()
        
        if 'proximo_mantenimiento' in data and data['proximo_mantenimiento']:
            if hasattr(data['proximo_mantenimiento'], 'isoformat'):
                data['proximo_mantenimiento'] = data['proximo_mantenimiento'].isoformat()
        
        result = db.update_one('maquinas', {'maquina_id': maquina_id}, data)
        
        if result == 0:
            raise HTTPException(status_code=404, detail="Máquina no encontrada")
        
        return {
            "message": "Máquina actualizada exitosamente",
            "data": data,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error en update_maquina: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{maquina_id}")
async def delete_maquina(maquina_id: str):
    """Elimina una máquina"""
    try:
        result = db.delete_one('maquinas', {'maquina_id': maquina_id})
        if result == 0:
            raise HTTPException(status_code=404, detail="Máquina no encontrada")
        return {
            "message": "Máquina eliminada exitosamente",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error en delete_maquina: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/estadisticas/resumen")
async def get_resumen_maquinas():
    """Obtiene estadísticas resumidas de máquinas"""
    try:
        maquinas = db.find('maquinas', {})
        
        if not maquinas:
            return {
                "total": 0,
                "operativas": 0,
                "mantenimiento": 0,
                "inactivas": 0,
                "status": "success"
            }
        
        total = len(maquinas)
        operativas = len([m for m in maquinas if m.get('estado') == 'Operativa'])
        mantenimiento = len([m for m in maquinas if m.get('estado') == 'Mantenimiento'])
        inactivas = len([m for m in maquinas if m.get('estado') in ['Inactiva', 'Fuera_servicio']])
        
        return {
            "total": total,
            "operativas": operativas,
            "mantenimiento": mantenimiento,
            "inactivas": inactivas,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error en get_resumen_maquinas: {e}")
        raise HTTPException(status_code=500, detail=str(e))