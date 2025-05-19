from pyniryo import NiryoRobot

ROBOT_IP = "192.168.217.107"

try:
    robot = NiryoRobot(ROBOT_IP)
    print("ok")
except Exception as e:
    print("error")