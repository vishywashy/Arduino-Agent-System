import serial
import time
def LEDController(state:str, light:str):
    com = "COM5"
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = com
    serialInst.open()
    command = light+" "+state
    time.sleep(2)
    serialInst.write((command+"\n").encode("utf-8"))
    serialInst.close()

def DistanceCalculator():
    serialInsta = serial.Serial()
    serialInsta.port = "COM5"
    serialInsta.baudrate = 9600
    serialInsta.open()
    time.sleep(5)
    if serialInsta.in_waiting > 0:
            line = serialInsta.readline()
            data_string = line.decode('utf-8').strip() 
            return f"{data_string}"
    serialInsta.close()
    return "No connection established"


