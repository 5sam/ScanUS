# gui.py
Contains the class Application used to generate the UI **Université de Sherbrooke**

## Code
### Common usage
- import tkinter as tk
- create an instance of tk.Tk() i.e.: your_instance=tk.Tk()
- Optionally, give the window a name using: your_instance.title('Your_title') 
- Create an instance of the user interface with gui_instance = gui.Application(master=your_instance)
## Functions

# def __init__(self, master=none):
- Constructor to create window and buttons for the gui
- Creates thread safe objets that are to be shares with other sections of code outside of UI
- Creates the thread to handle the window events

# def create_widgets(self, need_plot):
- Creates the different buttons including their positions and actions when pressed
- Receives the variable to be toggled by the checkbox 

# def set_running(self, value): 
- sets value of is_running to value using the lock to prevent issue with threads

# def get_running(self):
- returns value of is_running using the lock to prevent issue with threads

# def set_cancel(self, value):
- sets value of cancel to value using the lock to prevent issue with threads

# def get_cancel(self):
- returns value of canel using the lock to prevent issue with threads

# def get_need_plot(self):
- returns value of need plot using the lock to prevent issue with threads

# def toggle_var_plot(self):
- Changes value of plot from False to True according to it's previous value using the lock to prevent issues with threads

# def do_stop(self):
- Called by stop button
- Deactivates the stop button and activates the buttons start and cancel
- Sets is_running to false

# def do_start(self):
- Called by start button
- Deactivates the start button and activates the buttons stop and cancel
- Sets is_running to true and cancel to false 

# def do_cancel(self):
- Called by cancel button
- Deactivates the buttons cancel and stop (if necessary) and activates the start button
- Sets cancel to true

# def plot_change(self):
- Called when clicking the checkbox
- Toggles need_plot to the correct value according to the checkbox
