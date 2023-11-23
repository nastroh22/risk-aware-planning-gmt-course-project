import pyglet as pyg
from pyglet import app
from pyglet import image
from pyglet.window import Window , key
import carDomain.visualize as visualize
import carDomain.feature as feature
import carDomain.car as car
import carDomain.lane as lane
import carDomain.trajectory as trajectory
import carDomain.utils as utils
import carDomain.world  as world

import pyglet.gl  as gl
import pyglet.graphics as graphics
import numpy as np
import controls

c = controls.State()

vis = visualize.Visualizer()
roadmap = world.intersection()
vis.use_world(roadmap)
vis.reset()

sprite = roadmap.cars[0]
window = vis.window

label = pyg.text.Label('',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

K = .5

@window.event
def on_key_press(symbol, modifiers):
    # Symbolic names:
    if symbol == key.W or symbol == key.UP:
        c.GO = True
    if symbol == key.D or symbol == key.RIGHT:
        c.RIGHT = True
    if symbol == key.A or symbol == key.LEFT:
        c.LEFT = True
    if symbol == key.S or symbol == key.DOWN:
        c.REVERSE = True
    if symbol == key.SPACE:
        c.REVERSE = True
    # print(roadmap.cars[0].x)


@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.W or symbol == key.UP:
        c.GO = False
    if symbol == key.D or symbol == key.RIGHT:
        c.RIGHT = False
    if symbol == key.A or symbol == key.LEFT:
        c.LEFT = False
    if symbol == key.S or symbol == key.DOWN:
        c.REVERSE = False
    if symbol == key.SPACE:
        c.BRAKE = False

    # # Number keys:
    # elif symbol == key._1:

    # # Number keypad keys:
    # elif symbol == key.NUM_1:

@window.event
def on_draw():

    # Player Movements:
    if c.GO:
        roadmap.cars[0].traj.x0.set_value( 
                        np.array([roadmap.cars[0].x[0] + .01*np.cos(roadmap.cars[0].x[2]) , 
                                  roadmap.cars[0].x[1] + .01*np.sin(roadmap.cars[0].x[2]), 
                                  roadmap.cars[0].x[2] , 
                                  roadmap.cars[0].x[3]  ]) )
        c.brakes = 0
    if c.BRAKE:
        roadmap.cars[0].traj.x0.set_value( 
                        np.array([roadmap.cars[0].x[0] + .05*np.cos(roadmap.cars[0].x[2])*K**(c.brakes+1) , 
                                  roadmap.cars[0].x[1] + .05*np.sin(roadmap.cars[0].x[2])*K**(c.brakes+1), 
                                  roadmap.cars[0].x[2] , 
                                  roadmap.cars[0].x[3]  ]) )
        c.brakes += 1
    if c.LEFT:
        roadmap.cars[0].traj.x0.set_value( 
                        np.array([roadmap.cars[0].x[0], 
                                    roadmap.cars[0].x[1] , 
                                    roadmap.cars[0].x[2] + .05 , 
                                    roadmap.cars[0].x[3] +1 ]) )
    if c.RIGHT:
        roadmap.cars[0].traj.x0.set_value( np.array([
                                    roadmap.cars[0].x[0] ,
                                    roadmap.cars[0].x[1] , 
                                    roadmap.cars[0].x[2] - .05, 
                                    roadmap.cars[0].x[3] ]) )
    if c.REVERSE:
        roadmap.cars[0].traj.x0.set_value( np.array([
                                    roadmap.cars[0].x[0]  - .01*np.cos(roadmap.cars[0].x[2]),
                                    roadmap.cars[0].x[1] - .01*np.sin(roadmap.cars[0].x[2]), 
                                    roadmap.cars[0].x[2] , 
                                    roadmap.cars[0].x[3] ]) )
        c.brakes += 1
    
    
    label.draw()


    vis.window.clear()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    # self.camera()
    gl.glEnable(vis.grass.target)
    gl.glEnable(gl.GL_BLEND)
    gl.glBindTexture(vis.grass.target, vis.grass.id)
    W = 10000.
    graphics.draw(4, gl.GL_QUADS,
        ('v2f', (-W, -W, W, -W, W, W, -W, W)),
        ('t2f', (0., 0., W*5., 0., W*5., W*5., 0., W*5.))
    )
    gl.glDisable(vis.grass.target)
    for lane in vis.lanes:
        vis.draw_lane_surface_og(lane)
    for lane in vis.lanes:
        vis.draw_lane_lines(lane)
    for exit in vis.exits:
        vis.draw_exit(exit)
    for obj in vis.objects:
        vis.draw_object(obj)
    for car in vis.cars:
        if car!=vis.main_car and car not in vis.visible_cars:
            vis.draw_car(vis.anim_x[car], car.color)
    if vis.heat is not None:
        vis.draw_heatmap()
    for car in vis.cars:
        if car==vis.main_car or car in vis.visible_cars:
            vis.draw_car(vis.anim_x[car], car.color)
    gl.glPopMatrix()
# print(vis.anim_x)
# print(vis.anim_x[vis.cars[0]])
vis.run_sim()

