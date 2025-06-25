import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pyniryo import NiryoRobot
import cv2
import time
from GemeloDigital.dt_helper import reportar_error_estado

robot_ip = "192.168.183.107"

def generate_frames(stop_event):
    robot = NiryoRobot(robot_ip)  # Cambia esta IP por la del robot Niryo Ned2 (ae)
    robot.clear_collision_detected()  # Limpiar colisiones detectadas
    while not stop_event.is_set():
        try:
            frame = robot.get_img_compressed()  # bytes JPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        except Exception as e:
            reportar_error_estado()
            print(f"[STREAM] Error capturando imagen: {e}")
            break