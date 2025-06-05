from pyniryo import *
import cv2
import numpy as np
from pyniryo import uncompress_image
from pyniryo.vision import threshold_hsv, ColorHSV, show_img, show_img_and_wait_close
import time
from datetime import datetime
from bbdd_robot.bbdd_functions import registrar_historial, registrar_error
from GemeloDigital.dt_helper import reportar_error_estado

# Conectar al robot
robot = NiryoRobot("192.168.217.107")  # Cambia esta IP por la del robot Niryo Ned2 (ae)
conveyor_id = robot.set_conveyor()  # Configurar la cinta transportadora

def encender_cinta():
    """Encender la cinta transportadora si no está encendida."""    
    robot.run_conveyor(conveyor_id, speed=100, direction=ConveyorDirection.BACKWARD)
    
    print("Cinta transportadora encendida")
    print("La cinta ya está encendida")

def apagar_cinta():
    """Apagar la cinta transportadora si está encendida."""
    robot.stop_conveyor(conveyor_id)  # Detener la cinta
        
    print("Cinta transportadora apagada")
    print("La cinta ya está apagada")

# The neutral pose
neutral_pose = JointsPosition(-0.001,0.4999,-1.251,0,-0.006,-0.001)

# The observer pose
#observer_pose = JointsPosition(0.062,-0.160,-0.578,-0.006,-1.267,0.180)
observer_pose = JointsPosition(0.077,-0.046,-0.904,0.117,-0.750,-0.101)
observer_worspace_pose = JointsPosition(0.062,0.563,-0.634,0.000,-1.448,-0.049)

pick_pose = JointsPosition(-1.062,-0.613,0.055,-0.216,-1.289,-1.020)
pick_pose_arriba = JointsPosition(-1.083,-0.257,0.010,-0.020,-1.246,-1.129)

place_pose = JointsPosition(-0.925,-0.782,0.276,0.008,-1.103,-2.490)

# Posiciones de recogida y colocación en la cinta
#pick_pose_cinta = JointsPosition(0.130,-0.273,-0.664,0.049,-0.629,0.026)
pick_pose_cinta_arriba = JointsPosition(0.130,0.372,-0.725,-0.034,-0.517,0.049)
place_pose_cinta = JointsPosition(-1.544,-0.261,-0.142,-0.351,-1.322,-1.450)
place_pose_cinta_arriba = JointsPosition(-1.527,-0.128,-0.061,-0.232,-1.345,-1.539)

def detectar_pieza(robot):
    """Detecta si hay una pieza y su color. Devuelve 'rojo', 'verde' o None."""

    # Capturar imagen de la cámara del Niryo
    img_compressed = robot.get_img_compressed()
    img = uncompress_image(img_compressed)

    # Detectar color rojo usando los rangos HSV predefinidos
    mask_red = threshold_hsv(img, *ColorHSV.RED.value)

    # Rango HSV para verde
    green_min_hsv = [45, 100, 100]
    green_max_hsv = [80, 255, 255]
    mask_green = threshold_hsv(img, list_min_hsv=green_min_hsv, list_max_hsv=green_max_hsv)

    # Verificar si hay suficientes píxeles blancos en las máscaras
    if np.sum(mask_red) > 5000:
        return 'rojo'

    elif np.sum(mask_green) > 5000:
        return 'verde'

    else:
        return None

'''def ejecutar():
    """Ejecutar el flujo completo del programa."""
    apagar_cinta()  # Apagar la cinta al inicio
    robot.clear_collision_detected()  # Limpiar colisiones detectadas
    robot.calibrate_auto()  # Calibrar el robot automáticamente
    robot.move(neutral_pose)  # Mover el robot a la posición neutral
    robot.release_with_tool()
    robot.move(pick_pose_arriba)  # Mover el robot a la posición de recogida
    robot.move(pick_pose)  # Mover el robot a la posición de recogida
    robot.grasp_with_tool()  # Agarrar la pieza con la herramienta
    robot.move(pick_pose_arriba)  # Volver a la posición neutral
    robot.move(place_pose)
    robot.release_with_tool()  # Soltar la pieza en la posición de colocación
    robot.move(pick_pose_arriba)  # Volver a la posición neutral
    robot.move(neutral_pose)  # Volver a la posición neutral
    robot.move(observer_pose)  # Mover el robot a la posición de observación
    time.sleep(1)  # Esperar un segundo para estabilizar la cámara
    encender_cinta()  # Encender la cinta transportadora

    print("Cinta encendida. Observando...")

    while True:
        try:
            color = detectar_pieza(robot)

            if color:
                print(f"Pieza {color} detectada.")
                time.sleep(1)
                apagar_cinta()  # Apagar la cinta al detectar una pieza

                if color == 'rojo':
                    print("Es roja: dejarla pasar por 5 segundos.")
                    time.sleep(2)
                    encender_cinta()
                    time.sleep(5)
                    apagar_cinta()
                    print("Fin del proceso con pieza roja.")
                    break

                else:
                    print(f"Es {color}: proceder a recoger y colocar.")
                    # Intentar detectar y agarrar la pieza
                    robot.clear_collision_detected()  # Limpiar colisiones detectadas
                    robot.move(observer_worspace_pose)
                    # Intentar detectar y agarrar la pieza
                    obj_found, shape, detected_color = robot.vision_pick("color_pick2")

                    if obj_found and shape:
                        print(f"Pieza detectada")
                        robot.move(place_pose_cinta_arriba)
                        robot.move(place_pose_cinta)
                        # Colocar la pieza
                        robot.place(place_pose_cinta)

                        print("Pieza colocada correctamente.")
                        robot.move(place_pose_cinta_arriba)
                        robot.move(neutral_pose)
                    else:
                        print("No se pudo detectar ninguna pieza para agarrar.")

                    break

            else:
                print("Aún sin pieza detectada...")

        except Exception as e:
            print(f"Error durante la detección: {e}")

        time.sleep(1.5)
'''

def ejecutar():
    """Ejecutar el flujo completo del programa (base roja)."""
    inicio = time.time()
    resultado = "Éxito"
    errores = 0

    try:
        apagar_cinta()
        robot.clear_collision_detected()
        robot.calibrate_auto()
        robot.move(neutral_pose)
        robot.release_with_tool()
        robot.move(pick_pose_arriba)
        robot.move(pick_pose)
        robot.grasp_with_tool()
        robot.move(pick_pose_arriba)
        robot.move(place_pose)
        robot.release_with_tool()
        robot.move(pick_pose_arriba)
        robot.move(neutral_pose)
        robot.move(observer_pose)
        time.sleep(1)
        encender_cinta()

        print("Cinta encendida. Observando...")

        while True:
            try:
                color = detectar_pieza(robot)

                if color:
                    print(f"Pieza {color} detectada.")
                    time.sleep(1)
                    apagar_cinta()

                    if color == 'rojo':
                        print("Es roja: dejarla pasar por 5 segundos.")
                        time.sleep(2)
                        encender_cinta()
                        time.sleep(5)
                        apagar_cinta()
                        print("Fin del proceso con pieza roja.")
                        break
                    else:
                        print(f"Es {color}: proceder a recoger y colocar.")
                        robot.clear_collision_detected()
                        robot.move(observer_worspace_pose)

                        obj_found, shape, detected_color = robot.vision_pick("color_pick2")

                        if obj_found and shape:
                            print(f"Pieza detectada")
                            robot.move(place_pose_cinta_arriba)
                            robot.move(place_pose_cinta)
                            robot.place(place_pose_cinta)
                            print("Pieza colocada correctamente.")
                            robot.move(place_pose_cinta_arriba)
                            robot.move(neutral_pose)
                        else:
                            raise Exception("No se pudo detectar ninguna pieza para agarrar.")

                        break
                else:
                    print("Aún sin pieza detectada...")

                time.sleep(1.5)

            except Exception as e:
                resultado = "Fallo"
                errores = 1
                ahora = datetime.now()
                registrar_error(
                    fecha=ahora.strftime("%d/%m/%Y"),
                    hora=ahora.strftime("%H:%M"),
                    codigo="E004",
                    descripcion=str(e),
                    programa="programa_base_rojo"
                )
                print(f"Error durante la detección registrado: {e}")
                break

    except Exception as e:
        resultado = "Fallo"
        errores = 1
        ahora = datetime.now()
        registrar_error(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M"),
            codigo="E001",
            descripcion=str(e),
            programa="programa_base_rojo"
        )
        print(f"Error inicial registrado: {e}")
        reportar_error_estado()
    finally:
        duracion = int(time.time() - inicio)
        ahora = datetime.now()
        registrar_historial(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M"),
            programa="programa_base_rojo",
            duracion=duracion,
            resultado=resultado,
            errores=errores
        )

if __name__ == "__main__":
    ejecutar()  # Ejecutar el programa principal
