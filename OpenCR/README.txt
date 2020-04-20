- Follow the steps in this guide to properly set up your OpenCr:
	http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/

-Change the DXL_IDs in communication.ino to fit your motor, you can find them by using one of the tutorial's function
in the previously downloaded library called <Find>.

-Upload communication.ino on your OpenCr.

-Plug 2 motors directly into the Opencr (1 XM,it is going to be motor 1 and 1 XL, it is going to be motor 2) and one motor in serial with one that is plug into the OpenCr (motor 3)

-Connect your OpenCr with a Pi or a computer by a serial port.

-run a code with motor.py to make a motor run, stop, go to a position or to get its angle.