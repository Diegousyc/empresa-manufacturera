"""
Rutas de depuración para verificar estado de DB
"""
from fastapi import APIRouter, HTTPException
from database import db

router = APIRouter()

@router.get("/db")
async def debug_db():
    """Devuelve estado de conexión y conteos por colección"""
    try:
        connected = db.db is not None
        collections = []
        counts = {}
        if connected:
            all_collections = db.db.list_collection_names()
            # Excluir colecciones que no usamos
            collections = [c for c in all_collections if c not in {'sensores'}]
            for c in collections:
                try:
                    counts[c] = db.count(c)
                except Exception:
                    counts[c] = None
        return {"connected": connected, "collections": collections, "counts": counts, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
