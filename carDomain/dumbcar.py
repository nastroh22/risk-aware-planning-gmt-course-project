import numpy as np
import  carDomain.utils as utils
import theano as th
import theano.tensor as tt
from carDomain.trajectory import Trajectory
import carDomain.feature as feature
import pyglet

class Car(object):
    def __init__(self):
        self.guy = pyglet.sprite.Sprite("imgs/car-blue.png")
        self.dx = .01
        self.dy = .01
    def move_x(self,dt):
        self.guy.x += self.dx * dt
    def move_y(self,dt):
        self.guy.y += self.dy * dt
