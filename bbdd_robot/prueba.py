import datetime
from bbdd_functions import registrar_historial, registrar_error, registrar_tiempos_diarios

# Fecha y hora actuales
ahora = datetime.datetime.now()
fecha = ahora.strftime('%d/%m/%Y')
hora = ahora.strftime('%H:%M:%S')

# --- Prueba 1: registrar_historial ---
registrar_historial(
    fecha=fecha,
    hora=hora,
    programa="programa_prueba",
    duracion=12.5,
    resultado="Éxito",
    errores="Ninguno"
)

print("✅ Historial registrado.")

# --- Prueba 2: registrar_error ---
registrar_error(
    fecha=fecha,
    hora=hora,
    codigo="E001",
    descripcion="Error simulado en conexión",
    programa="programa_prueba"
)

print("✅ Error registrado.")

# --- Prueba 3: registrar_tiempos_diarios ---
tiempo_activo = 85.3  # minutos
tiempo_inactivo = 34.7  # minutos

registrar_tiempos_diarios(
    fecha=ahora,
    tiempo_activo_min=tiempo_activo,
    tiempo_inactivo_min=tiempo_inactivo
)

print("✅ Tiempos diarios registrados.")