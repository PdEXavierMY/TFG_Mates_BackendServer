from pyniryo import NiryoRobot
import cv2
import time

robot_ip = "192.168.217.107"
robot = NiryoRobot(robot_ip)

def generate_frames(stop_event):
    while not stop_event.is_set():
        try:
            frame = robot.get_color_image()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)
        except Exception as e:
            print(f"[STREAM] Error capturando imagen: {e}")
            break