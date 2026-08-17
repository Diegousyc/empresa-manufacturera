from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db

router = APIRouter()

@router.get("/")
async def get_paros(
    limit: int = Query(100, ge=1, le=1000),
    maquina_id: Optional[str] = None
):
    """Obtiene todos los paros"""
    query = {}
    if maquina_id:
        query['maquina_id'] = maquina_id
    
    data = db.find('paros', query, limit)
    return {"data": data, "count": len(data), "status": "success"}

@router.post("/")
async def create_paro(data: dict):
    """Crea un nuevo paro"""
    if 'paro_id' not in data:
        from datetime import datetime
        data['paro_id'] = f"PARO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    result = db.insert_one('paros', data)
    return {"message": "Paro creado", "id": str(result), "data": data, "status": "success"}

@router.delete("/{paro_id}")
async def delete_paro(paro_id: str):
    """Elimina un paro"""
    result = db.delete_one('paros', {'paro_id': paro_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Paro no encontrado")
    return {"message": "Paro eliminado", "status": "success"}