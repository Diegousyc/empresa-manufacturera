"""
Inicialización de rutas
"""

from . import productos
from . import maquinas
from . import produccion
from . import calidad
from . import mantenimiento
from . import paros
from . import materia_prima
from . import analisis

__all__ = [
    'productos',
    'maquinas',
    'produccion',
    'calidad',
    'mantenimiento',
    'paros',
    'materia_prima',
    'analisis'
]