import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
import shutil
import pandas as pd
from datetime import datetime, timedelta
from bbdd_functions import registrar_historial, registrar_error, registrar_tiempos_diarios
from csv_handler import guardar_tiempos_en_csv, procesar_csv_tiempos

# Fecha y hora actuales
ahora = datetime.now()
fecha = ahora.strftime('%d/%m/%Y')
hora = ahora.strftime('%H:%M:%S')

'''#--- Prueba 1: registrar_historial ---
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

print("✅ Tiempos diarios registrados.")'''

# Importar tus funciones (ajusta el import al nombre de tu archivo si es necesario)
from bbdd_robot import csv_handler as modulo

# Reemplazar la ruta del CSV original por una temporal
def run_manual_test():
    print("🧪 Iniciando test manual de tiempos...")

    temp_dir = tempfile.mkdtemp()
    temp_csv = os.path.join(temp_dir, "tiempos_diarios.csv")
    modulo.TIEMPOS_CSV = temp_csv  # redirigir el path al temporal

    ayer = datetime.now().date() - timedelta(days=1)

    print(f"✅ Guardando datos de prueba para la fecha: {ayer}")
    modulo.guardar_tiempos_en_csv(ayer, 25, 10)
    modulo.guardar_tiempos_en_csv(ayer, 15, 20)

    # Verificar contenido del CSV
    if os.path.exists(temp_csv):
        df = pd.read_csv(temp_csv)
        print("\n📄 Contenido del CSV:")
        print(df)

        total_activo = df['activo_minutos'].sum()
        total_inactivo = df['inactivo_minutos'].sum()
        print(f"\n🔎 Total activo: {total_activo} min")
        print(f"🔎 Total inactivo: {total_inactivo} min")

        # Mock manual de la función registrar_tiempos_diarios
        def mock_registrar_tiempos_diarios(fecha, activo, inactivo):
            print(f"\n📤 Llamada simulada a registrar_tiempos_diarios(fecha={fecha}, activo={activo}, inactivo={inactivo})")

        # Sustituir la función real por el mock
        modulo.registrar_tiempos_diarios = mock_registrar_tiempos_diarios

        print("\n⚙️ Ejecutando procesamiento del CSV...")
        modulo.procesar_csv_tiempos()
    else:
        print("❌ Error: No se creó el archivo CSV")

    # Limpiar
    shutil.rmtree(temp_dir)
    print("\n🧹 Limpieza completada. Test finalizado.")

if __name__ == "__main__":
    run_manual_test()