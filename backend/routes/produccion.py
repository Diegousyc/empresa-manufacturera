"""
Rutas para Producción
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import logging

from models.produccion import Produccion
from database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def get_producciones(limit: int = Query(100, ge=1, le=2000)):
    """Obtiene todas las producciones"""
    try:
        # Devolver producciones ordenadas por fecha_inicio descendente (más recientes primero)
        data = db.find('producciones', {}, limit, sort=[('fecha_inicio', -1)])
        total = db.count('producciones', {})
        return {"data": data, "count": len(data), "total": total, "status": "success"}
    except Exception as e:
        logger.error(f"Error en get_producciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{produccion_id}")
async def get_produccion(produccion_id: str):
    """Obtiene una producción por ID"""
    try:
        data = db.find_one('producciones', {'produccion_id': produccion_id})
        if not data:
            raise HTTPException(status_code=404, detail="Producción no encontrada")
        return {"data": data, "status": "success"}
    except Exception as e:
        logger.error(f"Error en get_produccion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_produccion(produccion: Produccion):
    """Crea una nueva producción"""
    try:
        data = produccion.dict()
        # Convertir fechas a ISO
        if 'fecha_inicio' in data and data['fecha_inicio']:
            if hasattr(data['fecha_inicio'], 'isoformat'):
                data['fecha_inicio'] = data['fecha_inicio'].isoformat()
        if 'fecha_fin' in data and data['fecha_fin']:
            if hasattr(data['fecha_fin'], 'isoformat'):
                data['fecha_fin'] = data['fecha_fin'].isoformat()

        result = db.insert_one('producciones', data)
        return {"message": "Producción creada", "id": str(result), "data": data, "status": "success"}
    except Exception as e:
        logger.error(f"Error en create_produccion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{produccion_id}")
async def update_produccion(produccion_id: str, produccion: Produccion):
    """Actualiza una producción"""
    try:
        data = produccion.dict()
        if 'fecha_inicio' in data and data['fecha_inicio'] and hasattr(data['fecha_inicio'], 'isoformat'):
            data['fecha_inicio'] = data['fecha_inicio'].isoformat()
        if 'fecha_fin' in data and data['fecha_fin'] and hasattr(data['fecha_fin'], 'isoformat'):
            data['fecha_fin'] = data['fecha_fin'].isoformat()

        result = db.update_one('producciones', {'produccion_id': produccion_id}, data)
        if result == 0:
            raise HTTPException(status_code=404, detail="Producción no encontrada")
        return {"message": "Producción actualizada", "data": data, "status": "success"}
    except Exception as e:
        logger.error(f"Error en update_produccion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{produccion_id}")
async def delete_produccion(produccion_id: str):
    """Elimina una producción"""
    try:
        result = db.delete_one('producciones', {'produccion_id': produccion_id})
        if result == 0:
            raise HTTPException(status_code=404, detail="Producción no encontrada")
        return {"message": "Producción eliminada", "status": "success"}
    except Exception as e:
        logger.error(f"Error en delete_produccion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/resumen")
async def get_resumen_producciones():
    """Estadísticas resumidas de producciones"""
    try:
        producciones = db.find('producciones', {})
        total = len(producciones) if producciones else 0
        total_cantidad = sum(p.get('cantidad_producida', 0) for p in (producciones or []))
        promedio_calidad = (sum(p.get('calidad', 0) for p in (producciones or [])) / total) if total else 0
        return {
            "total_producciones": total,
            "cantidad_total": total_cantidad,
            "promedio_calidad": promedio_calidad,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error en get_resumen_producciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))