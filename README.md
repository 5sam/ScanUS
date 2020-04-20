# ScanUS
4th semester project of Robotics Engineering at **Université de Sherbrooke**

This project is a simple and cheap solution to 3D scanning
## Calibration
### Intrinsic Parameters
- To calibrate the intrinsic parameters of your Picamera, you should take at least 20-30 pictures of a calibration grid
- Chessboard calibration grid patterns can be found [here](https://markhedleyjones.com/projects/calibration-checkerboard-collection)
- The parameters of the chosen grid can be set in the calibration.py header or can be inputs when you call calib_camera()
- The outputed values of **mtx** and **dist** should then be written in the header of camera.py
### Extrinsic Parameters
- To calibrate the extrinsic parameters of the camera, use calib_camera_ext() with a picture containing known positions in world
- Enter known points in points_in_world array
- Locate points in the same order using the zooming option if necessary (using **z** key)
- Double-click to save point
- Once all points are saved press **esc** to exit and plug the output to CAMERA_POS in camera.py if the error is acceptable
- If the error is unacceptable, repeat this process with more known points

### Note
- The camera must have its y axis pointing towards the center of the image when calculating the **CAMERA_POS** and **CAMERA_ANGLES** 

## Setting up the Pi
### Material needed:
- A Raspberry Pi 3B/3B+
- A working internet connection
- A fan

### Note: 
OpenCV is the library that allows the image analysis portion of the software. 
However, installation on the Raspberry Pi as of 2020/02/25 is difficult due to there not being
precompiled binaries in PyPi. 
An Pi image with a compiled version of OpenCV was included to make the installation easier for future users. 
The manual compilation will be explained further bellow. 

### Recommended installation:
1. Download the image of the Pi contained in the [link](currently missing:we did not find a good way to share 32Gb)
2. Install BalenaEtcher to flash the image to your microSD card.
3. All of the libraries used will already be installed. So the installation is now complete.
4. To use the virtual environment. Type the following commands into the terminal:
- source ~/.profile
- workon cv 
5. If you see (cv) on the command line. You are now working on the virtual environment set up to work with openCV. 
6. Head to your project directory and run your code by calling your main:
python file_name.py
7. If done correctly. The libraries should be accessible and the code should run without a hastle.

### Manual installation:
1. Start by opening a terminal.
2. Check if a compiled binary exists by typing:
sudo pip install opencv-contrib-python
If there installation begins. SKIP to step 6.
2. To manually install/compile OpenCV an internet guide will be used with a few changes. Note that any 
version can be installed. The guide installs version 4.0.0 but we installed the lastest version as of today (4.2.0).
3. The guide can be found [here](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/?fbclid=IwAR2Ive8JRk1Rmsd-L2Q14sKA6e-RKXLADuGuhVXQ_LvJyMGnPrbBibMMPN0)
4. First change to be aware of. make -j4 command should be used as stated in the guide. Be careful, our Pi
3B+ managed to overheat during the installation despite having a heatsink. If you have a fan, make it blow air 
towards your Pi to keep it cool. It is possible for your Pi to shutdown or throttle if it is not cooled properly 
slowing down the installation. Despite the installation working well. Your Pi may hang due to a race condition 
towards the end. If so, press ctrl+C to terminate compilation (ours did around 80% and then around 98%). 
Don't worry, the files that are already compiled will not be compiled again. Then modify the command to: 
make -j1 
The compilation will be slower but will no longer hang indefinately in the critical sections. 
5. In step 6, make sure to browse your Pi's directory for the files mentionned. Your 
cv2.cpython-35m-arm-linux-gnueabihf.so and cv2.so files might be in different folders depending on your python
version and location of your python files inside your Pi. Search for them through your files and use the correct 
path to avoir errors in creating the link to your virtual environment.
6. With your environment set up. Open a terminal and call the following 2 commands:
source ~/.profile
workon cv
The first one allows you to use workon cv command to open the virtual environment set up with openCV in the current 
terminal. The second is the activation of the environment.
7. Many external libraries are used with this project. The following steps are necessary if they haven't yet been 
installed on your Pi. 
8. Open a terminal and open your virtual environment.
9. Go to your project's path and run the main with:
python main.py
10. If you get a message saying an import could not be found. Type the name of the library on google as follows:
"library_name pypi"
PyPI contains all the libraries used and will show the correct pip install command to download the latest version of
each library.
