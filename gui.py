import tkinter as tk
import matplotlib
import multiprocessing
from ctypes import c_bool

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.grid()
        # this can last about 1 sec
        #self.mutexRun = multiprocessing.Lock()
        #self.mutexRes = multiprocessing.Lock()
        #self.mutexPlt = multiprocessing.Lock()
        self.is_running = multiprocessing.Value(c_bool, False)
        self.restart = multiprocessing.Value(c_bool, False)
        self.need_plot = multiprocessing.Value(c_bool, False)
        self.create_widgets(self.need_plot)
        self.t = multiprocessing.Process(target=self.mainloop)
        self.t.start()

    def __del__(self):
        self.t.join()

    def create_widgets(self, need_plot):
        self.button1 = tk.Button(self, text="Start", command=self.do_start)
        self.button1["padx"] = 13
        self.button1.grid(row=0, column=0, padx=20)
        
        self.button2 = tk.Button(self, text="Stop", command=self.do_stop,
                                 state=tk.DISABLED)
        self.button2["padx"] = 14
        self.button2.grid(row=1, column=0, padx=20)
        
        self.button3 = tk.Button(self, text="Restart", command=self.do_restart,
                                 state=tk.DISABLED)
        self.button3["padx"] = 7
        self.button3.grid(row=2, column=0, padx=20)
        self.label1 = tk.Label(self,
                               text="                                "+
                               "                         ")
        self.label1.grid(row=1, column=2)

        #self.var = tk.BooleanVar()
        self.cbutton1 = tk.Checkbutton(self, text="Show plot",
                                       variable=need_plot.value,
                                       command=self.plot_change)
        self.cbutton1.deselect()
        self.cbutton1.grid(row=4, column=0)        
        self.quit = tk.Button(self, text = "QUIT", fg = "red",
                              padx=15, command = self.master.destroy)
        self.quit.grid(row=4, column=3, padx=20, pady=20)


    def set_running(self, value):
        with self.is_running.get_lock():
            self.is_running.value = value

    def get_running(self):
        with self.is_running.get_lock():
            return self.is_running.value

    def set_restart(self, value):
        with self.restart.get_lock():
            self.restart.value = value

    def get_restart(self):
        with self.restart.get_lock():
            return self.restart.value
        
    def do_stop(self):
        self.button1["state"] = tk.NORMAL
        self.button2["state"] = tk.DISABLED
        self.button3["state"] = tk.NORMAL
        self.set_running(False)
        print(self.get_running())

    def do_start(self):
        self.button1["state"] = tk.DISABLED
        self.button2["state"] = tk.NORMAL
        self.button3["state"] = tk.NORMAL
        self.set_running(True)
        print(self.get_running())

    def do_restart(self):
        self.button1["state"] = tk.NORMAL
        self.button2["state"] = tk.DISABLED
        self.button3["state"] = tk.DISABLED
        self.set_restart(True)
        print(self.get_restart())

    def get_need_plot(self):
        with self.need_plot.get_lock():
            return self.need_plot.value

    def toggle_var_plot(self):
        if(self.get_need_plot() == True):
            with self.need_plot.get_lock():
                self.need_plot.value = False
        else:
            with self.need_plot.get_lock():
                self.need_plot.value = True
        
    def plot_change(self):
        self.toggle_var_plot()
        print(self.get_need_plot())
        
    

