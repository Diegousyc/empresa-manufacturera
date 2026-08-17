"""
Script para insertar datos de ejemplo en MongoDB
Ejecutar desde la carpeta backend: python insertar_datos_ejemplo.py
"""

import sys
import os

# Agregar el directorio actual al path para poder importar database
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db
from datetime import datetime, timedelta
import random

def generar_datos_ejemplo():
    """Genera datos de ejemplo para todas las colecciones"""
    
    print("=" * 60)
    print("📝 Generando datos de ejemplo...")
    print("=" * 60)
    
    # 1. Productos
    productos = [
        {
            "producto_id": "PROD-001",
            "nombre": "Arandela Acero",
            "categoria": "Metales",
            "descripcion": "Arandela de acero inoxidable 1/2 pulgada",
            "precio_unitario": 15.50,
            "costo_produccion": 8.75,
            "tiempo_estimado": 45,
            "fecha_creacion": datetime.now().isoformat(),
            "activo": True
        },
        {
            "producto_id": "PROD-002",
            "nombre": "Eje Transmisión",
            "categoria": "Mecánica",
            "descripcion": "Eje para transmisión de potencia",
            "precio_unitario": 250.00,
            "costo_produccion": 180.00,
            "tiempo_estimado": 120,
            "fecha_creacion": datetime.now().isoformat(),
            "activo": True
        },
        {
            "producto_id": "PROD-003",
            "nombre": "Placa Electrónica",
            "categoria": "Electrónica",
            "descripcion": "Placa PCB para control industrial",
            "precio_unitario": 320.50,
            "costo_produccion": 210.00,
            "tiempo_estimado": 90,
            "fecha_creacion": datetime.now().isoformat(),
            "activo": True
        },
        {
            "producto_id": "PROD-004",
            "nombre": "Empaque Plástico",
            "categoria": "Plásticos",
            "descripcion": "Empaque de plástico moldeado",
            "precio_unitario": 5.75,
            "costo_produccion": 3.20,
            "tiempo_estimado": 30,
            "fecha_creacion": datetime.now().isoformat(),
            "activo": True
        },
        {
            "producto_id": "PROD-005",
            "nombre": "Lubricante Industrial",
            "categoria": "Química",
            "descripcion": "Lubricante para maquinaria pesada",
            "precio_unitario": 45.00,
            "costo_produccion": 28.50,
            "tiempo_estimado": 60,
            "fecha_creacion": datetime.now().isoformat(),
            "activo": True
        }
    ]
    
    # 2. Máquinas
    maquinas = [
        {
            "maquina_id": "MAQ-001",
            "nombre": "Torno CNC-1000",
            "tipo": "CNC",
            "modelo": "MX-2000",
            "fabricante": "Siemens",
            "año_fabricacion": 2020,
            "capacidad_produccion": 150,
            "consumo_energetico": 5.5,
            "temperatura_operacion": 45,
            "presion_operacion": 6.5,
            "estado": "Operativa",
            "ultimo_mantenimiento": (datetime.now() - timedelta(days=30)).isoformat(),
            "proximo_mantenimiento": (datetime.now() + timedelta(days=30)).isoformat(),
            "horas_operacion": 1500,
            "fecha_instalacion": "2022-06-15",
            "activa": True
        },
        {
            "maquina_id": "MAQ-002",
            "nombre": "Fresadora F-500",
            "tipo": "Fresadora",
            "modelo": "F-500",
            "fabricante": "Haas",
            "año_fabricacion": 2021,
            "capacidad_produccion": 120,
            "consumo_energetico": 4.2,
            "temperatura_operacion": 50,
            "presion_operacion": 5.0,
            "estado": "Operativa",
            "ultimo_mantenimiento": (datetime.now() - timedelta(days=45)).isoformat(),
            "proximo_mantenimiento": (datetime.now() + timedelta(days=15)).isoformat(),
            "horas_operacion": 1200,
            "fecha_instalacion": "2022-08-10",
            "activa": True
        },
        {
            "maquina_id": "MAQ-003",
            "nombre": "Rectificadora R-300",
            "tipo": "Rectificadora",
            "modelo": "R-300",
            "fabricante": "Makino",
            "año_fabricacion": 2021,
            "capacidad_produccion": 80,
            "consumo_energetico": 3.8,
            "temperatura_operacion": 55,
            "presion_operacion": 4.5,
            "estado": "Mantenimiento",
            "ultimo_mantenimiento": (datetime.now() - timedelta(days=5)).isoformat(),
            "proximo_mantenimiento": (datetime.now() + timedelta(days=60)).isoformat(),
            "horas_operacion": 800,
            "fecha_instalacion": "2022-09-20",
            "activa": True
        },
        {
            "maquina_id": "MAQ-004",
            "nombre": "Taladro T-200",
            "tipo": "Taladro",
            "modelo": "T-200",
            "fabricante": "Bosch",
            "año_fabricacion": 2022,
            "capacidad_produccion": 200,
            "consumo_energetico": 2.5,
            "temperatura_operacion": 40,
            "presion_operacion": 3.0,
            "estado": "Operativa",
            "ultimo_mantenimiento": (datetime.now() - timedelta(days=20)).isoformat(),
            "proximo_mantenimiento": (datetime.now() + timedelta(days=40)).isoformat(),
            "horas_operacion": 500,
            "fecha_instalacion": "2023-01-15",
            "activa": True
        },
        {
            "maquina_id": "MAQ-005",
            "nombre": "CNC Multieje X-1000",
            "tipo": "CNC",
            "modelo": "X-1000",
            "fabricante": "FANUC",
            "año_fabricacion": 2022,
            "capacidad_produccion": 180,
            "consumo_energetico": 6.0,
            "temperatura_operacion": 48,
            "presion_operacion": 7.0,
            "estado": "Operativa",
            "ultimo_mantenimiento": (datetime.now() - timedelta(days=10)).isoformat(),
            "proximo_mantenimiento": (datetime.now() + timedelta(days=50)).isoformat(),
            "horas_operacion": 1000,
            "fecha_instalacion": "2022-11-01",
            "activa": True
        }
    ]
    
    # 3. Operadores
    operadores = [
        {
            "operador_id": "OP-001",
            "nombre": "Juan Pérez",
            "especialidad": "CNC",
            "experiencia": 8,
            "certificaciones": ["CNC Nivel 3", "Seguridad Industrial"],
            "activo": True,
            "fecha_contratacion": "2020-03-15"
        },
        {
            "operador_id": "OP-002",
            "nombre": "María García",
            "especialidad": "Fresadora",
            "experiencia": 6,
            "certificaciones": ["Fresado Avanzado"],
            "activo": True,
            "fecha_contratacion": "2021-06-01"
        },
        {
            "operador_id": "OP-003",
            "nombre": "Carlos López",
            "especialidad": "Mantenimiento",
            "experiencia": 10,
            "certificaciones": ["Mantenimiento Predictivo", "Electrónica Industrial"],
            "activo": True,
            "fecha_contratacion": "2019-01-10"
        },
        {
            "operador_id": "OP-004",
            "nombre": "Ana Martínez",
            "especialidad": "Control Calidad",
            "experiencia": 5,
            "certificaciones": ["ISO 9001", "Control Estadístico"],
            "activo": True,
            "fecha_contratacion": "2021-09-20"
        }
    ]
    
    # 4. Producciones (generar 20 registros)
    producciones = []
    productos_ids = ["PROD-001", "PROD-002", "PROD-003", "PROD-004", "PROD-005"]
    maquinas_ids = ["MAQ-001", "MAQ-002", "MAQ-003", "MAQ-004", "MAQ-005"]
    operadores_ids = ["OP-001", "OP-002", "OP-003", "OP-004"]
    
    for i in range(20):
        producto_id = random.choice(productos_ids)
        maquina_id = random.choice(maquinas_ids)
        operador_id = random.choice(operadores_ids)
        cantidad = random.randint(50, 200)
        defectos = random.randint(0, 10)
        tiempo = random.randint(30, 120)
        
        fecha = datetime.now() - timedelta(days=random.randint(0, 30))
        
        if tiempo > 0:
            eficiencia = round(cantidad / tiempo, 2)
        else:
            eficiencia = 0
        
        if cantidad > 0:
            calidad = round(100 - (defectos / cantidad * 100), 2)
        else:
            calidad = 100
        
        producciones.append({
            "produccion_id": f"PROD-{str(i+1).zfill(4)}",
            "producto_id": producto_id,
            "maquina_id": maquina_id,
            "operador_id": operador_id,
            "lote": f"LOTE-2026-{str(i+1).zfill(4)}",
            "cantidad_producida": cantidad,
            "cantidad_defectuosa": defectos,
            "tiempo_produccion": tiempo,
            "temperatura": round(random.uniform(20, 60), 1),
            "presion": round(random.uniform(3, 8), 1),
            "velocidad": random.randint(500, 3000),
            "fecha_inicio": fecha.isoformat(),
            "fecha_fin": (fecha + timedelta(minutes=tiempo)).isoformat(),
            "eficiencia": eficiencia,
            "calidad": calidad,
            "observaciones": None
        })
    
    # 5. Calidad (registros de control de calidad)
    calidad_registros = []
    for i, prod in enumerate(producciones[:10]):
        calidad_registros.append({
            "calidad_id": f"CAL-{str(i+1).zfill(3)}",
            "produccion_id": prod["produccion_id"],
            "producto_id": prod["producto_id"],
            "inspector": random.choice(operadores_ids),
            "fecha_inspeccion": datetime.now().isoformat(),
            "calidad": round(random.uniform(85, 99.9), 2),
            "defectos": random.randint(0, 5),
            "defectos_tipo": random.choice(["Dimensional", "Superficial", "Material", "Montaje"]),
            "especificaciones_cumplidas": True,
            "acciones_correctivas": [],
            "observaciones": None
        })
    
    # 6. Mantenimientos
    mantenimientos = [
        {
            "mantenimiento_id": "MANT-001",
            "maquina_id": "MAQ-001",
            "tipo": "Preventivo",
            "descripcion": "Cambio de aceite y filtros",
            "fecha_inicio": (datetime.now() - timedelta(days=30)).isoformat(),
            "fecha_fin": (datetime.now() - timedelta(days=29)).isoformat(),
            "duracion": 2.5,
            "tecnico": "Carlos López",
            "costo": 350.00,
            "piezas_reemplazadas": ["Filtro A", "Aceite 10W-40"],
            "observaciones": "Mantenimiento programado",
            "completado": True
        },
        {
            "mantenimiento_id": "MANT-002",
            "maquina_id": "MAQ-003",
            "tipo": "Correctivo",
            "descripcion": "Reparación de sistema hidráulico",
            "fecha_inicio": (datetime.now() - timedelta(days=5)).isoformat(),
            "fecha_fin": (datetime.now() - timedelta(days=3)).isoformat(),
            "duracion": 8.0,
            "tecnico": "Carlos López",
            "costo": 1250.00,
            "piezas_reemplazadas": ["Válvula hidráulica", "Mangueras"],
            "observaciones": "Falla en bomba hidráulica",
            "completado": True
        },
        {
            "mantenimiento_id": "MANT-003",
            "maquina_id": "MAQ-005",
            "tipo": "Predictivo",
            "descripcion": "Análisis de vibraciones",
            "fecha_inicio": (datetime.now() - timedelta(days=10)).isoformat(),
            "fecha_fin": (datetime.now() - timedelta(days=9)).isoformat(),
            "duracion": 1.5,
            "tecnico": "Juan Pérez",
            "costo": 450.00,
            "piezas_reemplazadas": [],
            "observaciones": "Todo en orden",
            "completado": True
        }
    ]
    
    # 7. Paros de producción
    paros = [
        {
            "paro_id": "PARO-001",
            "maquina_id": "MAQ-002",
            "fecha_paro": (datetime.now() - timedelta(days=15)).isoformat(),
            "duracion_paro": 2.0,
            "causa": "Falla eléctrica",
            "descripcion": "Corto circuito en panel de control",
            "accion_correctiva": "Reemplazo de fusibles",
            "costo": 200.00
        },
        {
            "paro_id": "PARO-002",
            "maquina_id": "MAQ-003",
            "fecha_paro": (datetime.now() - timedelta(days=7)).isoformat(),
            "duracion_paro": 4.5,
            "causa": "Falta de material",
            "descripcion": "Sin materia prima para procesar",
            "accion_correctiva": "Solicitud urgente de material",
            "costo": 0.00
        },
        {
            "paro_id": "PARO-003",
            "maquina_id": "MAQ-001",
            "fecha_paro": (datetime.now() - timedelta(days=3)).isoformat(),
            "duracion_paro": 1.0,
            "causa": "Cambio de herramienta",
            "descripcion": "Cambio de broca programado",
            "accion_correctiva": "Cambio de herramienta",
            "costo": 0.00
        }
    ]
    
    # 8. Materia Prima
    materia_prima = [
        {
            "material_id": "MAT-001",
            "nombre": "Acero Inoxidable 304",
            "tipo": "Metal",
            "unidad": "kg",
            "cantidad": 500,
            "costo_unitario": 2.50,
            "proveedor": "Aceros Nacionales",
            "fecha_compra": (datetime.now() - timedelta(days=10)).isoformat(),
            "stock_minimo": 100,
            "ubicacion": "Almacén A-1"
        },
        {
            "material_id": "MAT-002",
            "nombre": "Resina Plástica",
            "tipo": "Plástico",
            "unidad": "kg",
            "cantidad": 300,
            "costo_unitario": 1.80,
            "proveedor": "Plásticos Industriales",
            "fecha_compra": (datetime.now() - timedelta(days=5)).isoformat(),
            "stock_minimo": 50,
            "ubicacion": "Almacén A-2"
        },
        {
            "material_id": "MAT-003",
            "nombre": "Lubricante Sintético",
            "tipo": "Químico",
            "unidad": "L",
            "cantidad": 100,
            "costo_unitario": 15.00,
            "proveedor": "Lubricantes SA",
            "fecha_compra": (datetime.now() - timedelta(days=15)).isoformat(),
            "stock_minimo": 20,
            "ubicacion": "Almacén B-1"
        }
    ]
    
    # 9. Sensores
    sensores = [
        {
            "sensor_id": "SENS-001",
            "maquina_id": "MAQ-001",
            "tipo": "Temperatura",
            "ubicacion": "Motor principal",
            "valor_min": 20,
            "valor_max": 80,
            "unidad": "°C",
            "fecha_instalacion": "2022-06-15"
        },
        {
            "sensor_id": "SENS-002",
            "maquina_id": "MAQ-001",
            "tipo": "Vibración",
            "ubicacion": "Eje principal",
            "valor_min": 0,
            "valor_max": 10,
            "unidad": "mm/s",
            "fecha_instalacion": "2022-06-15"
        },
        {
            "sensor_id": "SENS-003",
            "maquina_id": "MAQ-002",
            "tipo": "Presión",
            "ubicacion": "Sistema hidráulico",
            "valor_min": 0,
            "valor_max": 100,
            "unidad": "bar",
            "fecha_instalacion": "2022-08-10"
        },
        {
            "sensor_id": "SENS-004",
            "maquina_id": "MAQ-005",
            "tipo": "Velocidad",
            "ubicacion": "Eje rotatorio",
            "valor_min": 0,
            "valor_max": 5000,
            "unidad": "RPM",
            "fecha_instalacion": "2022-11-01"
        }
    ]
    
    print("📤 Insertando datos en MongoDB...")
    
    # Insertar todos los datos
    try:
        db.insert_many("productos", productos)
        print(f"   ✅ Productos insertados: {len(productos)}")
        
        db.insert_many("maquinas", maquinas)
        print(f"   ✅ Máquinas insertadas: {len(maquinas)}")
        
        db.insert_many("operadores", operadores)
        print(f"   ✅ Operadores insertados: {len(operadores)}")
        
        db.insert_many("producciones", producciones)
        print(f"   ✅ Producciones insertadas: {len(producciones)}")
        
        db.insert_many("calidad", calidad_registros)
        print(f"   ✅ Calidad insertada: {len(calidad_registros)}")
        
        db.insert_many("mantenimientos", mantenimientos)
        print(f"   ✅ Mantenimientos insertados: {len(mantenimientos)}")
        
        db.insert_many("paros", paros)
        print(f"   ✅ Paros insertados: {len(paros)}")
        
        db.insert_many("materia_prima", materia_prima)
        print(f"   ✅ Materia Prima insertada: {len(materia_prima)}")
        
        db.insert_many("sensores", sensores)
        print(f"   ✅ Sensores insertados: {len(sensores)}")
        
        print("\n" + "=" * 60)
        print("✅ ¡Todos los datos insertados exitosamente!")
        print("=" * 60)
        print("\n📊 Resumen:")
        print(f"   📄 Productos: {len(productos)}")
        print(f"   📄 Máquinas: {len(maquinas)}")
        print(f"   📄 Operadores: {len(operadores)}")
        print(f"   📄 Producciones: {len(producciones)}")
        print(f"   📄 Calidad: {len(calidad_registros)}")
        print(f"   📄 Mantenimientos: {len(mantenimientos)}")
        print(f"   📄 Paros: {len(paros)}")
        print(f"   📄 Materia Prima: {len(materia_prima)}")
        print(f"   📄 Sensores: {len(sensores)}")
        
    except Exception as e:
        print(f"\n❌ Error al insertar datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generar_datos_ejemplo()