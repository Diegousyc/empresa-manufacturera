from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.productos import Producto
from database import db

router = APIRouter()

@router.get("/")
async def get_productos(
    limit: int = Query(100, ge=1, le=1000),
    categoria: Optional[str] = None
):
    """Obtiene todos los productos"""
    query = {}
    if categoria:
        query['categoria'] = categoria
    
    data = db.find('productos', query, limit)
    return {"data": data, "count": len(data), "status": "success"}

@router.get("/{producto_id}")
async def get_producto(producto_id: str):
    """Obtiene un producto por ID"""
    data = db.find_one('productos', {'producto_id': producto_id})
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"data": data, "status": "success"}

@router.post("/")
async def create_producto(producto: Producto):
    """Crea un nuevo producto"""
    data = producto.dict()
    if 'fecha_creacion' in data and data['fecha_creacion']:
        data['fecha_creacion'] = data['fecha_creacion'].isoformat()
    
    result = db.insert_one('productos', data)
    return {"message": "Producto creado", "id": str(result), "data": data, "status": "success"}

@router.put("/{producto_id}")
async def update_producto(producto_id: str, producto: Producto):
    """Actualiza un producto"""
    data = producto.dict()
    if 'fecha_creacion' in data and data['fecha_creacion']:
        data['fecha_creacion'] = data['fecha_creacion'].isoformat()
    
    result = db.update_one('productos', {'producto_id': producto_id}, data)
    if result == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto actualizado", "data": data, "status": "success"}

@router.delete("/{producto_id}")
async def delete_producto(producto_id: str):
    """Elimina un producto"""
    result = db.delete_one('productos', {'producto_id': producto_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado", "status": "success"}