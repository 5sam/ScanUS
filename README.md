# ScanUS
Projet de session robotique S4 robot scanneur

## Code
### Common usage
- Open a picture containing a red dot using cv2.imread()
- Find the red dot coordinates with find_red_dot() in camera.py
- Calculate point and vector from camera to red dot using get_red_dot_point_vector_in_world() in camera.py 
- Determine line of red_dot relative to the rotating table
- Use intersect() to find the intersection point between the two lines
- Repeat for new image and table angle
- Use plot() from plot.py to visualize the point cloud