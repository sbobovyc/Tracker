"""
Created on July 13, 2011

@author: sbobovyc
"""

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class GUI_work_frame(tk.Frame):
    
    def __init__(self, parent, controller):
        self.name = "work_frame"
        self.controller = controller
        self.controller.register(self, "work_frame")
        
        #TODO move default initialization to a separate function
        self.width = 400
        self.height = 400
        self.num_colors = 3
        self.selected_layer = tk.ANCHOR
        
        
        # initialize the frame
        tk.Frame.__init__(self, parent, bd=2, relief=tk.FLAT, background="grey")
                        
        # add widgets to frame
        
        #top of frame, mostly static        
        #put a text area in it        
        self.text=tk.Text(self, height=10, background='white')
        
        # put a scroll bar in the frame
        self.scroll=tk.Scrollbar(self)
        # set scrolling properties
        self.scroll.configure(command=self.text.yview)        
        self.text.configure(yscrollcommand=self.scroll.set)
        
        #pack everything
        self.text.pack(anchor=tk.W, side=tk.LEFT)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.pack(side=tk.TOP)
    
        
    def get(self):
        return {"width":self.width_label.get(), "height":self.height_label.get(), 
                "num_colors":self.num_colors_label.get(), "octave_count":self.octave_count.get(),
                "frequency":self.frequency.get(), "persistence":self.persistence.get(),
                "seed":self.seed.get(), "threshold":self.threshold.get(), "z":self.z.get()}
        
    def clear_fields(self):
        self.octave_count.clear()
        self.frequency.clear()
        self.persistence.clear()
        self.seed.clear()
        self.threshold.clear()
        self.z.clear()
        
    def set_fields(self, layer):
        self.octave_count.set(layer.octave_count)
        self.frequency.set(layer.frequency)
        self.persistence.set(layer.persistence)
        self.seed.set(layer.seed)
        self.threshold.set(layer.threshold)
        self.z.set(layer.z)
        
    def update_current_layer(self):
        self.controller.update_layer(self.layer_list.get_currently_selected_layer())