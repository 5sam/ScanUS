import serial as serial
import time

# open the serial communication
COMMUNICATION_PORT = serial.Serial('/dev/ttyACM0', 9600, timeout=.3)
#COMMUNICATION_PORT = serial.Serial('COM6', 9600, timeout=.3)


# give you back the motor angle
def get_angle_motor():
    COMMUNICATION_PORT.reset_input_buffer()
    while COMMUNICATION_PORT.inWaiting() == 0:
        time.sleep(0.001)
    angle_serial = COMMUNICATION_PORT.readline()
    angle_rad = float(angle_serial)
    print(angle_rad)
    return angle_rad


# start the motor
def start_motor():
    COMMUNICATION_PORT.write(bytes(b'run\n'))


# stop the motor
def stop_motor():
    COMMUNICATION_PORT.write(bytes(b'stop\n'))


# make the motor go to position 0 then stop it
def restart_motor():
    COMMUNICATION_PORT.write(bytes(b'restart\n'))
