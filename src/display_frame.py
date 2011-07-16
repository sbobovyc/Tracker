"""
Created on June 28, 2011

@author: sbobovyc
"""
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class GUI_display_frame(tk.Frame):
    
    def __init__(self, parent, controller):
        # register with controller
        self.name = "display_frame"
        self.controller = controller
        self.controller.register(self, self.name)
        
        # create a scrollable canvas
        tk.Frame.__init__(self, parent, bd=2, relief=tk.FLAT, background="grey")
#        self.label = tk.Label(self, image=tk.PhotoImage(width=32, height=32))
#        self.label.pack()
        self.xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)      
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)  
        
        self.yscrollbar = tk.Scrollbar(self)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(self, background="grey", bd=0, height=0, width=0,
                        xscrollcommand=self.xscrollbar.set,
                        yscrollcommand=self.yscrollbar.set)
        self.canvas.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)
        
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)
        

  


        
