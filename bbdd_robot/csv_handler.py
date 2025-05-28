import os
import pandas as pd
from datetime import datetime, timedelta
from bbdd_robot.bbdd_functions import registrar_tiempos_diarios

TIEMPOS_CSV = "tiempos_diarios.csv"

def guardar_tiempos_en_csv(fecha, activo_minutos, inactivo_minutos):
    nuevos_datos = pd.DataFrame([{
        'fecha': fecha.isoformat(),
        'activo_minutos': activo_minutos,
        'inactivo_minutos': inactivo_minutos
    }])

    if os.path.exists(TIEMPOS_CSV):
        df_actual = pd.read_csv(TIEMPOS_CSV)
        df_actual = pd.concat([df_actual, nuevos_datos], ignore_index=True)
    else:
        df_actual = nuevos_datos

    df_actual.to_csv(TIEMPOS_CSV, index=False)

def procesar_csv_tiempos():
    if not os.path.exists(TIEMPOS_CSV):
        return

    hoy = datetime.now().date()
    ayer = hoy - timedelta(days=1)

    df = pd.read_csv(TIEMPOS_CSV, parse_dates=['fecha'])
    df['fecha'] = pd.to_datetime(df['fecha']).dt.date
    df_ayer = df[df['fecha'] == ayer]

    if not df_ayer.empty:
        suma_activo = df_ayer['activo_minutos'].sum()
        suma_inactivo = df_ayer['inactivo_minutos'].sum()
        registrar_tiempos_diarios(ayer, suma_activo, suma_inactivo)