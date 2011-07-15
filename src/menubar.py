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
    
import tkFileDialog
import os

class GUI_menubar(tk.Menu):
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.name = "menubar"
        self.controller = controller
        self.controller.register(self, self.name)
        # file types
        self.file_types = [('all files', '.*'), ('', '.shp')]
        
        # create a menu
        tk.Menu.__init__(self, parent)
                
        filemenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=filemenu)
#        filemenu.add_command(label="New Project", command=self.callback())
#        filemenu.add_command(label="Open Project", command=self.callback())
        filemenu.add_command(label="Add Shapefile...", command=self.file_open)
        filemenu.add_command(label="Add Raster...", command=self.file_open)
        
#        filemenu.add_command(label="Save", command=self.callback())
#        filemenu.add_command(label="Save as", command=self.file_save)
#        filemenu.add_command(label="Save Layers", command=self.file_save_layer)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_callback)
        
        helpmenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.callback)
        
    def callback(self):
        print "called the callback!"
    
    def file_open(self):                
        source_image_path = tkFileDialog.askopenfilename()
        self.controller.open_image(source_image_path) 
    
    def file_save(self):
        output_image_path = tkFileDialog.asksaveasfilename(filetypes=self.file_types)
        self.controller.save_image(output_image_path)
        
    def file_save_layer(self):
        output_path = tkFileDialog.asksaveasfilename(filetypes=self.file_types)
        basename, extension = os.path.splitext(output_path)
        self.controller.save_layers(basename, extension)
         
    def exit_callback(self):
        self.parent.quit()
        