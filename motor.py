import serial as serial
import time

# We need roughly 1.5 seconds between 2 different commands, except for the get_angle_motor function

# open the serial communication
# line under is for raspberrypi
# COMMUNICATION_PORT = serial.Serial('/dev/ttyACM0', 9600, timeout=.3)
# line under is for PC
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


# start the motor at designated speed, speed must be between 0 and 265, input normal or reverse for sens
def start_motor(motor_number, speed, sens):
    if sens == "reverse":
        speed = speed + 1000
    bytenumber = str(motor_number) + "-start-" + str(speed) + "\n"
    COMMUNICATION_PORT.write(bytes(bytenumber, 'utf-8'))


# stop the motor
def stop_motor(motor_number):
    bytenumber = str(motor_number) + "-stop-" + "0" + "\n"
    COMMUNICATION_PORT.write(bytes(bytenumber, 'utf-8'))


# make the motor go to input angle (in radian from 0 to 6.28)
def position_motor(motor_number, angle):
    number = int(angle/2/3.1416*4096)

    bytenumber = str(motor_number) + "-position-" + str(number) + "\n"
    COMMUNICATION_PORT.write(bytes(bytenumber, 'utf-8'))


