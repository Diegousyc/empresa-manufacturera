from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db

router = APIRouter()

@router.get("/")
async def get_materia_prima(
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[str] = None
):
    """Obtiene toda la materia prima"""
    query = {}
    if tipo:
        query['tipo'] = tipo
    
    data = db.find('materia_prima', query, limit)
    return {"data": data, "count": len(data), "status": "success"}

@router.post("/")
async def create_material(data: dict):
    """Crea un nuevo material"""
    if 'material_id' not in data:
        from datetime import datetime
        data['material_id'] = f"MAT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    result = db.insert_one('materia_prima', data)
    return {"message": "Material creado", "id": str(result), "data": data, "status": "success"}

@router.delete("/{material_id}")
async def delete_material(material_id: str):
    """Elimina un material"""
    result = db.delete_one('materia_prima', {'material_id': material_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return {"message": "Material eliminado", "status": "success"}