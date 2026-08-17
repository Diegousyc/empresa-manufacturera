from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db

router = APIRouter()

@router.get("/")
async def get_mantenimientos(
    limit: int = Query(100, ge=1, le=1000),
    maquina_id: Optional[str] = None
):
    """Obtiene todos los mantenimientos"""
    query = {}
    if maquina_id:
        query['maquina_id'] = maquina_id
    
    data = db.find('mantenimientos', query, limit)
    return {"data": data, "count": len(data), "status": "success"}

@router.get("/{mantenimiento_id}")
async def get_mantenimiento(mantenimiento_id: str):
    """Obtiene un mantenimiento por ID"""
    data = db.find_one('mantenimientos', {'mantenimiento_id': mantenimiento_id})
    if not data:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return {"data": data, "status": "success"}

@router.post("/")
async def create_mantenimiento(data: dict):
    """Crea un nuevo mantenimiento"""
    if 'mantenimiento_id' not in data:
        from datetime import datetime
        data['mantenimiento_id'] = f"MANT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    result = db.insert_one('mantenimientos', data)
    return {"message": "Mantenimiento creado", "id": str(result), "data": data, "status": "success"}

@router.delete("/{mantenimiento_id}")
async def delete_mantenimiento(mantenimiento_id: str):
    """Elimina un mantenimiento"""
    result = db.delete_one('mantenimientos', {'mantenimiento_id': mantenimiento_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return {"message": "Mantenimiento eliminado", "status": "success"}