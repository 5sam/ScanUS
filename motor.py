import serial as serial
import time

# open the serial communication
#COMMUNICATION_PORT = serial.Serial('/dev/ttyACM0', 9600, timeout=.3)
COMMUNICATION_PORT = serial.Serial('COM6', 9600, timeout=.3)


# give you back the motor angle of the input motor (1,2 or 3)
def get_angle_motor(motor_number):
    COMMUNICATION_PORT.reset_input_buffer()
    while COMMUNICATION_PORT.inWaiting() == 0:
        time.sleep(0.001)
    angle_serial1 = COMMUNICATION_PORT.readline()
    while COMMUNICATION_PORT.inWaiting() == 0:
        time.sleep(0.001)
    angle_serial2 = COMMUNICATION_PORT.readline()
    while COMMUNICATION_PORT.inWaiting() == 0:
        time.sleep(0.001)
    angle_serial3 = COMMUNICATION_PORT.readline()

    angle_rad1 = float(angle_serial1)
    angle_rad2 = float(angle_serial2)
    angle_rad3 = float(angle_serial3)

    if motor_number == 1:
        return angle_rad1
    if motor_number == 2:
        return angle_rad2
    if motor_number == 3:
        return angle_rad3


# start the motor of the scoop
def start_motor_scoop():
    COMMUNICATION_PORT.write(bytes(b'-1'))


# stop the motorof the scoop
def stop_motor_scoop():
    COMMUNICATION_PORT.write(bytes(b'-2'))


# make the motor of the scoop go to position 0 then stop it
def restart_motor_scoop():
    COMMUNICATION_PORT.write(bytes(b'-3'))


# start the motor of the screw
def start_motor_screw():
    COMMUNICATION_PORT.write(bytes(b'-4'))


# stop the motorof the screw
def stop_motor_screw():
    COMMUNICATION_PORT.write(bytes(b'-5'))


# make the motor of the screw go to position 0 then stop it
def restart_motor_screw():
    COMMUNICATION_PORT.write(bytes(b'-6'))


# start the motor of the screw
def start_motor_laser():
    COMMUNICATION_PORT.write(bytes(b'-7'))


# stop the motorof the screw
def stop_motor_laser():
    COMMUNICATION_PORT.write(bytes(b'-8'))


# make the motor of the screw go to position 0 then stop it
def restart_motor_laser():
    COMMUNICATION_PORT.write(bytes(b'-9'))


# make the motor go to input angle (in radian from 0 to 6.28)
def position_motor_scoop(number):
    number = int(number/2/3.1416*4096)

    bytenumber = "b'" + str(number) + "'"
    print(bytenumber)
    COMMUNICATION_PORT.write(bytes(bytenumber, 'utf-8'))


