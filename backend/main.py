"""
API Principal del Sistema de Producción Industrial
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
import uvicorn
import logging
import os
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Producción Industrial API",
    description="API para gestión y análisis de producción industrial",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# IMPORTAR RUTAS
# ============================================
try:
    from routes import (
        productos, maquinas, produccion, calidad,
        mantenimiento, paros, materia_prima, analisis
    )
    logger.info("✅ Rutas importadas correctamente")
except ImportError as e:
    logger.error(f"❌ Error importando rutas: {e}")
    raise

# ============================================
# REGISTRAR RUTAS DE LA API
# ============================================
app.include_router(productos.router, prefix="/api/productos", tags=["Productos"])
app.include_router(maquinas.router, prefix="/api/maquinas", tags=["Máquinas"])
app.include_router(produccion.router, prefix="/api/produccion", tags=["Producción"])
app.include_router(calidad.router, prefix="/api/calidad", tags=["Calidad"])
app.include_router(mantenimiento.router, prefix="/api/mantenimiento", tags=["Mantenimiento"])
app.include_router(paros.router, prefix="/api/paros", tags=["Paros"])
app.include_router(materia_prima.router, prefix="/api/materia-prima", tags=["Materia Prima"])
app.include_router(analisis.router, prefix="/api/analisis", tags=["Análisis"])

logger.info("✅ Rutas registradas correctamente")

# ============================================
# LISTAR TODAS LAS RUTAS (DEBUG)
# ============================================
def listar_rutas():
    """Lista todas las rutas registradas para depuración"""
    rutas = []
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = getattr(route, 'methods', set())
            rutas.append(f"{', '.join(methods)} {route.path}")
    return rutas

# ============================================
# CONFIGURACIÓN PARA SERVIR HTML
# ============================================

FRONTEND_DIR = Path("../frontend").resolve()

if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path("./frontend").resolve()

if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path(".") / "frontend"
    FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

logger.info(f"📁 Frontend: {FRONTEND_DIR}")

def servir_html(nombre_archivo):
    """Sirve un archivo HTML desde la carpeta frontend"""
    file_path = FRONTEND_DIR / nombre_archivo
    if file_path.exists():
        return FileResponse(file_path)
    return RedirectResponse(url="/")

# ============================================
# RUTAS PARA PÁGINAS HTML
# ============================================

@app.get("/")
async def root():
    return servir_html("index.html")

@app.get("/dashboard")
async def dashboard():
    return servir_html("dashboard.html")

@app.get("/produccion")
async def produccion_page():
    return servir_html("produccion.html")

@app.get("/maquinas")
async def maquinas_page():
    return servir_html("maquinas.html")

@app.get("/productos")
async def productos_page():
    return servir_html("productos.html")

@app.get("/calidad")
async def calidad_page():
    return servir_html("calidad.html")

@app.get("/mantenimiento")
async def mantenimiento_page():
    return servir_html("mantenimiento.html")

@app.get("/paros")
async def paros_page():
    return servir_html("paros.html")

@app.get("/materia-prima")
async def materia_prima_page():
    return servir_html("materia_prima.html")

@app.get("/reportes")
async def reportes_page():
    return servir_html("reportes.html")

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check():
    from database import db
    try:
        db.client.admin.command('ping')
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "OK",
        "database": db_status,
        "frontend": str(FRONTEND_DIR),
        "version": "1.0.0"
    }

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    # Crear carpetas necesarias
    os.makedirs("models/saved", exist_ok=True)
    
    # Mostrar información de inicio
    print("\n" + "=" * 60)
    print("🚀 SISTEMA DE PRODUCCIÓN INDUSTRIAL")
    print("=" * 60)
    print(f"📁 Frontend: {FRONTEND_DIR}")
    print("📚 Documentación API: http://localhost:8000/docs")
    print("🌐 Página principal: http://localhost:8000")
    print("=" * 60)
    print("\n📋 RUTAS REGISTRADAS:")
    for ruta in listar_rutas():
        print(f"   {ruta}")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )