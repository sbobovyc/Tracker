'''
Created on Jan 12, 2011

@author: sbobovyc
'''

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class GUI_spin_label(tk.Frame):
    '''
    classdocs
    '''

    def __init__(self, parent, text, from_, to, increment, command, state=tk.NORMAL, default=0):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, parent, width=20) 
        self.parent = parent
        self.text = text
        self.from_ = from_
        self.to = to
        self.increment = increment
        self.default = default
        self.state = state
        self.command = command
        self.pack(expand=tk.TRUE, fill=tk.X)
        self.initialize()
        
        
    def initialize(self):
        self.label = tk.Label(self, text=self.text, bg="grey", relief="sunken")
        self.label.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X)
        self.spinbox = tk.Spinbox(self, from_=self.from_, to=self.to, increment=self.increment, state=self.state, width=4, command=self.command)
        self.spinbox.delete(0,"end")
        self.spinbox.insert(0,self.default)
        self.spinbox.pack(side=tk.RIGHT)
#        self.spinbox.grid_columnconfigure(0, weight=1)
#        self.spinbox.grid_rowconfigure(0, weight=1)
#        self.spinbox.grid(row=0,column=1)
        
    def get(self):
        return self.spinbox.get()
    
    def clear(self):
        self.spinbox.delete(0, "end")
    
    def set(self, value):        
        self.spinbox.insert(0, value)
        
        