from pyniryo import *
import cv2
import numpy as np
from pyniryo import uncompress_image
from pyniryo.vision import threshold_hsv, ColorHSV, show_img, show_img_and_wait_close
import time

# Conectar al robot
robot = NiryoRobot("192.168.217.107")  # Cambia esta IP por la del robot Niryo Ned2 (ae)
robot.calibrate_auto()  # Calibrar el robot automáticamente
status = robot.get_hardware_status()  # Obtener el estado del hardware
print(status)