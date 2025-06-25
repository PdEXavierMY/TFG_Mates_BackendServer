import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pyniryo import *
import cv2
import numpy as np
from pyniryo import uncompress_image
from pyniryo.vision import threshold_hsv, ColorHSV, show_img, show_img_and_wait_close
import time
from datetime import datetime
from bbdd_robot.bbdd_functions import registrar_historial, registrar_error
from GemeloDigital.dt_helper import reportar_error_estado

robot_ip = "192.168.183.107"

def ejecutar():
    """Reiniciar el robot: detener cinta, abrir garra y volver a posición neutral."""
    inicio = time.time()
    resultado = "Éxito"
    errores = 0

    try:
        robot = NiryoRobot(robot_ip)  # Cambia la IP si es necesario
        robot.clear_collision_detected()
        conveyor_id = robot.set_conveyor()

        # The neutral pose
        neutral_pose = JointsPosition(-0.001, 0.4999, -1.251, 0, -0.006, -0.001)

        # Detener la cinta
        robot.stop_conveyor(conveyor_id)
        print("Cinta transportadora apagada")
        print("La cinta ya está apagada")

        # Volver a posición neutral y abrir garra
        robot.move(neutral_pose)
        robot.open_gripper()

    except Exception as e:
        resultado = "Fallo"
        errores = 1
        ahora = datetime.now()
        registrar_error(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M"),
            codigo="E005",
            descripcion=str(e),
            programa="restart"
        )
        print(f"Error al reiniciar el robot: {e}")
        reportar_error_estado()

    finally:
        duracion = int(time.time() - inicio)
        ahora = datetime.now()
        registrar_historial(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M"),
            programa="restart",
            duracion=duracion,
            resultado=resultado,
            errores=errores
        )

# Para ejecución directa
if __name__ == "__main__":
    ejecutar()