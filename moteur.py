import serial as serial
import time

COMMUNICATION_PORT = serial.Serial('COM6', 9600, timeout=.3)


def get_angle_moteur():
    COMMUNICATION_PORT.reset_input_buffer()
    while COMMUNICATION_PORT.inWaiting() == 0:
        time.sleep(0.001)
    angle_serial = COMMUNICATION_PORT.readline()
    angle_rad = float(angle_serial)
    print(angle_rad)
    return angle_rad


def start_moteur():
    COMMUNICATION_PORT.write(bytes(b'run\n'))


def stop_moteur():
    COMMUNICATION_PORT.write(bytes(b'stop\n'))


def restart_moteur():
    COMMUNICATION_PORT.write(bytes(b'restart\n'))
