from pyniryo import NiryoRobot

robot_ip = "192.168.183.107"

try:
    robot = NiryoRobot(robot_ip)
    print("ok")
except Exception as e:
    print("error")