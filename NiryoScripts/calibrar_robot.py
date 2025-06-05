from pyniryo import *
import cv2
import numpy as np
from pyniryo import uncompress_image
from pyniryo.vision import threshold_hsv, ColorHSV, show_img, show_img_and_wait_close
import time
from datetime import datetime
from bbdd_robot.bbdd_functions import registrar_historial, registrar_error
from GemeloDigital.dt_helper import reportar_error_estado

# Se asume que ya tienes estas funciones definidas en otro módulo o archivo:
# from helpers import registrar_error, registrar_historial

def ejecutar():
    """Calibrar el robot y registrar estado."""
    inicio = time.time()
    resultado = "Éxito"
    errores = 0

    try:
        robot = NiryoRobot("192.168.217.107")  # Cambiar según IP real
        robot.calibrate_auto()
        status = robot.get_hardware_status()
        print(status)

        # Guardar estado del hardware en log.txt
        with open("log.txt", "a") as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Hardware status:\n")
            log_file.write(str(status) + "\n\n")

    except Exception as e:
        resultado = "Fallo"
        errores = 1
        ahora = datetime.now()
        registrar_error(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M"),
            codigo="E005",
            descripcion=str(e),
            programa="calibrar_robot"
        )
        print(f"Error durante calibración: {e}")
        reportar_error_estado()

    finally:
        duracion = int(time.time() - inicio)
        ahora = datetime.now()
        registrar_historial(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M"),
            programa="calibrar_robot",
            duracion=duracion,
            resultado=resultado,
            errores=errores
        )

# Para ejecución directa
if __name__ == "__main__":
    ejecutar()