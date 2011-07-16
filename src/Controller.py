import Queue
import mapnik
from PIL import Image,ImageTk
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
    
width = 1000
height = 1000

import threading
import time
import random
class Supplier_Thread(threading.Thread):
    
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        

    def run(self):
        while True:                                                            
            #puts gps string to output queue            
            self.queue.put((random.randint(-80,80),random.randint(-80,80)))            
            #signals to output queue job is done
            self.queue.task_done()
                     
            
class Render_Thread(threading.Thread):
    
    def __init__(self, object_map, queue, map, layer_list):
        threading.Thread.__init__(self)
        
        self.object_map = object_map
        self.queue = queue
        
        self.map = map
        
        for layer in layer_list:
            self.map.layers.append(layer)
        self.map.zoom_all()
        self.draw()
        
    def run(self):
        while True:                      
            if not self.queue.empty(): 
                # get point from queue
                point = self.queue.get()            #point is a tuple
    
                # print point in gui
                self.object_map["work_frame"].text.insert(tk.END, "%i,%i\n" % (point[0],point[1]))
                self.object_map["work_frame"].text.yview(tk.END)
                
                # make point
                pds = mapnik.PointDatasource()
                pds.add_point(point[0], point[1],'Name','d')            
                
                # create point symbolizer for blue icons
                if mapnik.mapnik_version() >= 800:
                    point = mapnik.PointSymbolizer(mapnik.PathExpression('y2.png'))
                else:
                    point = mapnik.PointSymbolizer('y2.png','png',25,25)
    
    
                point.allow_overlap = True
        
                s = mapnik.Style()
                r = mapnik.Rule()
                r.symbols.append(point)
                     
                s.rules.append(r)

                self.layer2 = mapnik.Layer('GPS Coord')
                self.layer2.datasource = pds
                self.layer2.styles.append('Style')
                self.map.append_style('Style',s)
                
                self.map.layers.append(self.layer2)
                self.draw()
    def draw(self):                          
        # get image from mapnik and render to canvas
        img = mapnik.Image(width, height)
        mapnik.render(self.map, img)
        # convert to PIL image
        pil_img = Image.fromstring('RGBA', (width, height), img.tostring())
        # convert to ImageTk
        self.imagetk=ImageTk.PhotoImage(pil_img)                               
        self.object_map["display_frame"].canvas.create_image(0,0,image=self.imagetk, anchor=tk.NW)            
        # to prevent flickering, update
        self.object_map["display_frame"].canvas.update_idletasks()
        time.sleep(float(1/7))
            
            
class Controller(object):
    
    def __init__(self):
        self.layer_list = []        #list that contains mapnik layers
        self.imagetk = None         #image to be displayed on canvas
        self.map = mapnik.Map(width, height)         
        self.object_map = {}        #dictionary of gui components
        self.queue = Queue.Queue()
        
    ##
    # @param object: a tkinter gui object
    # @param name: a string that represent the name of the object
    def register(self, object, name):        
        self.object_map[name] = object
    
    def add_shapefile(self, path):                
        symbolizer = mapnik.PolygonSymbolizer(mapnik.Color("darkgreen"))
        rule = mapnik.Rule()
        rule.symbols.append(symbolizer)
        style = mapnik.Style()
        style.rules.append(rule)
        layer = mapnik.Layer("mapLayer")
        layer.datasource = mapnik.Shapefile(file=path)
        layer.styles.append("mapStyle")        
        self.map.background = mapnik.Color("steelblue")
        self.map.append_style("mapStyle", style)        
        
        self.layer_list.append(layer)
        
        
    def add_raster(self, path):
        datasource = mapnik.Gdal(file=path)
        layer = mapnik.Layer("myLayer")
        layer.datasource = datasource
        layer.styles.append("myLayerStyle")
        self.layer_list.append(layer)

    def open_image(self, path):
        
        ### Raster
        self.map = mapnik.Map(width, height)
        datasource = mapnik.Gdal(file=path)
        layer = mapnik.Layer("myLayer")
        layer.datasource = datasource
        layer.styles.append("myLayerStyle")
        symbol = mapnik.RasterSymbolizer()
        rule = mapnik.Rule()
        rule.symbols.append(symbol)
        style = mapnik.Style()
        style.rules.append(rule)
        self.map.append_style("myLayerStyle", style)
        self.map.layers.append(layer)
        self.map.zoom_all()                

        # get image from mapnik
        img = mapnik.Image(width, height)
        mapnik.render(self.map, img)
        # convert to PIL image
        pil_img = Image.fromstring('RGBA', (width, height), img.tostring())
        # convert to ImageTk
        self.imagetk=ImageTk.PhotoImage(pil_img)                       
        self.object_map["display_frame"].canvas.create_image(0,0,image=self.imagetk, anchor=tk.NW)
        
        
    def render(self):        
        render_thread = Render_Thread(self.object_map, self.queue, self.map, self.layer_list)
        render_thread.setDaemon(True)
        render_thread.start()        
        supply_thread = Supplier_Thread(self.queue)
        supply_thread.setDaemon(True)
        supply_thread.start()        
        self.queue.join()
        
        
        
        ### Shape
#        symbolizer = mapnik.PolygonSymbolizer(mapnik.Color("darkgreen"))
#        rule = mapnik.Rule()
#        rule.symbols.append(symbolizer)
#        style = mapnik.Style()
#        style.rules.append(rule)
#        layer = mapnik.Layer("mapLayer")
#        layer.datasource = mapnik.Shapefile(file=path)
#        layer.styles.append("mapStyle")
#        map = mapnik.Map(width, height)
#        map.background = mapnik.Color("steelblue")
#        map.append_style("mapStyle", style)
#        map.layers.append(layer)
#        map.zoom_all()
    
    #        self.map = mapnik.Map(width, height)
#        datasource = mapnik.Gdal(file=path)
#        layer = mapnik.Layer("myLayer")
#        layer.datasource = datasource
#        layer.styles.append("myLayerStyle")
#        symbol = mapnik.RasterSymbolizer()
#        rule = mapnik.Rule()
#        rule.symbols.append(symbol)
#        style = mapnik.Style()
#        style.rules.append(rule)
#        self.map.append_style("myLayerStyle", style)
#        self.map.layers.append(layer)
#        self.map.zoom_all()        
#        self.render_map()

#        # make point
#        pds = mapnik.PointDatasource()
#        pds.add_point(-50.0, 30.0,'Name','d')
#        pds.add_point(-40.0, 30.0,'Name','d')
#        
#        # create point symbolizer for blue icons
#        if mapnik.mapnik_version() >= 800:
#            point = mapnik.PointSymbolizer(mapnik.PathExpression('y.png'))
#        else:
#            point = mapnik.PointSymbolizer('y.png','png',50,50)
#
#
#        point.allow_overlap = True
#        
#        s = mapnik.Style()
#        r = mapnik.Rule()
#        r.symbols.append(point)
#             
#        s.rules.append(r)
#
#        layer2 = mapnik.Layer('GPS Coord')
#        layer2.datasource = pds
#        layer2.styles.append('Style')
#        self.map.layers.append(layer)
#        self.map.layers.append(layer2)
#        self.map.append_style('Style',s)

        # get image from mapnik
#        img = mapnik.Image(width, height)
#        mapnik.render(map, img)
#        # convert to PIL image
#        pil_img = Image.fromstring('RGBA', (width, height), img.tostring())
#        # convert to ImageTk
#        self.imagetk=ImageTk.PhotoImage(pil_img)                       
#        self.object_map["display_frame"].canvas.create_image(0,0,image=self.imagetk, anchor=tk.NW)
