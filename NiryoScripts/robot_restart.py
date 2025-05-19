from pyniryo import *
import cv2
import numpy as np
from pyniryo import uncompress_image
from pyniryo.vision import threshold_hsv, ColorHSV, show_img, show_img_and_wait_close
import time

# Conectar al robot
robot = NiryoRobot("192.168.217.107")  # Cambia esta IP por la del robot Niryo Ned2 (ae)
conveyor_id = robot.set_conveyor()  # Configurar la cinta transportadora
# The neutral pose
neutral_pose = JointsPosition(-0.001,0.4999,-1.251,0,-0.006,-0.001)

def apagar_cinta():
    """Apagar la cinta transportadora si está encendida."""
    robot.stop_conveyor(conveyor_id)  # Detener la cinta
        
    print("Cinta transportadora apagada")
    print("La cinta ya está apagada")

if __name__ == "__main__":
    # Apagar la cinta transportadora
    apagar_cinta()
    # Volver a la posición neutral
    robot.move(neutral_pose)
    robot.open_gripper()