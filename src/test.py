# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
 
import pygame
import mapnik

width = 800
height = 800

import threading
import Queue
import time
import random
class Supplier_Thread(threading.Thread):
    
    def __init__(self, queue):
        threading.Thread.__init__(self)
        queue = queue
        

    def run(self):
        while True:                                                            
            #puts gps string to output queue            
            queue.put((random.randint(-80,80),random.randint(-80,80)))            
            #signals to output queue job is done
            queue.task_done()

queue = Queue.Queue()
map = mapnik.Map(width, height)    
symbolizer = mapnik.PolygonSymbolizer(mapnik.Color("darkgreen"))
rule = mapnik.Rule()
rule.symbols.append(symbolizer)
style = mapnik.Style()
style.rules.append(rule)
layer = mapnik.Layer("mapLayer")
layer.datasource = mapnik.Shapefile(file="/usr/share/magics/110m/110m_land.shp")
layer.styles.append("mapStyle")        
map.background = mapnik.Color("steelblue")
map.append_style("mapStyle", style)        
map.layers.append(layer)
map.zoom_all()


# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
 
pygame.init()
  
# Set the height and width of the screen
size=[width,height]
screen=pygame.display.set_mode(size)
 
pygame.display.set_caption("Point plotter")
 
#Loop until the user clicks the close button.
done=False
 
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
 
supplier = Supplier_Thread(queue)
supplier.setDaemon(True)
supplier.start()

# -------- Main Program Loop -----------
while done==False:    
    if not queue.empty(): 
        # get point from queue
        point = queue.get()            #point is a tuple
                
        # make point
        ds = mapnik.MemoryDatasource()
        f = mapnik.Feature(mapnik.Context(), 1)
        f.add_geometries_from_wkt("POINT (%f %f)" % (point[0], point[1]))
        ds.add_feature(f)
        #pds.add_point(point[0], point[1],'Name','d')            
        
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

        layer2 = mapnik.Layer('GPS Coord')
        layer2.datasource = ds
        layer2.styles.append('Style')
        map.append_style('Style',s)
        
        map.layers.append(layer2)
    
    # get image from mapnik and render to canvas
    img = mapnik.Image(width, height)
    mapnik.render(map, img)
    img = pygame.image.fromstring(img.tostring(), (width, height), "RGBA")
    imgrect = img.get_rect()
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(black)
 
    # Limit to 20 frames per second
    clock.tick(20)
 
    screen.blit(img, imgrect)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
