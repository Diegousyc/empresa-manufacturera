from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db

router = APIRouter()

@router.get("/")
async def get_calidad(
    limit: int = Query(100, ge=1, le=1000),
    producto_id: Optional[str] = None
):
    """Obtiene todos los registros de calidad"""
    query = {}
    if producto_id:
        query['producto_id'] = producto_id
    
    data = db.find('calidad', query, limit)
    return {"data": data, "count": len(data), "status": "success"}

@router.get("/{calidad_id}")
async def get_calidad_by_id(calidad_id: str):
    """Obtiene un registro de calidad por ID"""
    data = db.find_one('calidad', {'calidad_id': calidad_id})
    if not data:
        raise HTTPException(status_code=404, detail="Registro de calidad no encontrado")
    return {"data": data, "status": "success"}

@router.post("/")
async def create_calidad(data: dict):
    """Crea un nuevo registro de calidad"""
    if 'calidad_id' not in data:
        from datetime import datetime
        data['calidad_id'] = f"CAL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    result = db.insert_one('calidad', data)
    return {"message": "Registro de calidad creado", "id": str(result), "data": data, "status": "success"}

@router.delete("/{calidad_id}")
async def delete_calidad(calidad_id: str):
    """Elimina un registro de calidad"""
    result = db.delete_one('calidad', {'calidad_id': calidad_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Registro de calidad no encontrado")
    return {"message": "Registro de calidad eliminado", "status": "success"}