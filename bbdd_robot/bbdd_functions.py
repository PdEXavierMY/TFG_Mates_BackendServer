import os
import pandas as pd

def registrar_historial(fecha, hora, programa, duracion, resultado, errores, archivo='bbdd_robot/simulacion_datos_robot.xlsx'):
    """Agrega un nuevo registro al historial de programas ejecutados."""
    nueva_fila = {
        'Fecha': fecha,
        'Hora': hora,
        'Programa': programa,
        'Duración (s)': duracion,
        'Resultado': resultado,
        'Errores': errores
    }

    if os.path.exists(archivo):
        with pd.ExcelWriter(archivo, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            df_existente = pd.read_excel(archivo, sheet_name='Historial Programas')
            df_nuevo = df_existente._append(nueva_fila, ignore_index=True)
            writer.book.remove(writer.book['Historial Programas'])
            df_nuevo.to_excel(writer, sheet_name='Historial Programas', index=False)
    else:
        df = pd.DataFrame([nueva_fila])
        with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Historial Programas', index=False)

def registrar_error(fecha, hora, codigo, descripcion, programa, archivo='bbdd_robot/simulacion_datos_robot.xlsx'):
    """Agrega un nuevo registro al log de errores."""
    nueva_fila = {
        'Fecha': fecha,
        'Hora': hora,
        'Código Error': codigo,
        'Descripción': descripcion,
        'Programa Relacionado': programa
    }

    if os.path.exists(archivo):
        with pd.ExcelWriter(archivo, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            df_existente = pd.read_excel(archivo, sheet_name='Logs de Errores')
            df_nuevo = df_existente._append(nueva_fila, ignore_index=True)
            writer.book.remove(writer.book['Logs de Errores'])
            df_nuevo.to_excel(writer, sheet_name='Logs de Errores', index=False)
    else:
        df = pd.DataFrame([nueva_fila])
        with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Logs de Errores', index=False)

def registrar_tiempos_diarios(fecha, tiempo_activo_min, tiempo_inactivo_min, archivo='bbdd_robot/simulacion_datos_robot.xlsx'):
    nueva_fila = {
        'Fecha': fecha.strftime('%d/%m/%Y'),
        'Tiempo Activo (min)': round(tiempo_activo_min),
        'Tiempo Inactivo (min)': round(tiempo_inactivo_min)
    }

    if os.path.exists(archivo):
        with pd.ExcelWriter(archivo, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            df_existente = pd.read_excel(archivo, sheet_name='Tiempo Activo Inactivo')
            df_nuevo = pd.concat([df_existente, pd.DataFrame([nueva_fila])], ignore_index=True)
            writer.book.remove(writer.book['Tiempo Activo Inactivo'])
            df_nuevo.to_excel(writer, sheet_name='Tiempo Activo Inactivo', index=False)
    else:
        df = pd.DataFrame([nueva_fila])
        with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Tiempo Activo Inactivo', index=False)