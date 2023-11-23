import numpy as np
# import theano as th
import theano.tensor as tt
import carDomain.feature as feature

class Lane(object): pass

class StraightLane(Lane):
    def __init__(self, p, q, w, l):
        self.p = np.asarray(p)
        self.q = np.asarray(q)
        self.w = w
        self.length = l
        self.m = (self.q-self.p)/np.linalg.norm(self.q-self.p)
        self.n = np.asarray([-self.m[1], self.m[0]])
    def shifted(self, m):
        return StraightLane(self.p+self.n*self.w*m, self.q+self.n*self.w*m, self.w, self.length)
    def dist2(self, x):
        r = (x[0]-self.p[0])*self.n[0]+(x[1]-self.p[1])*self.n[1]
        return r*r
    def gaussian(self, width=0.5):
        @feature.feature
        def f(t, x, u):
            return tt.exp(-0.5*self.dist2(x)/(width**2*self.w*self.w/4.))
        return f
class Exit(Lane):
    def __init__(self, start, angle, length, width):
        self.anchor = start
        self.width = width
        self.angle = angle
        self.theta = angle   * (np.pi / 180)
        self.scale = length
        self.a = self.anchor
        self.c = [self.a[0], self.a[1] + self.width ]
        self.d, self.b = [0,0] , [0,0]
        self.d[0] = self.c[0] + np.sin(self.theta)*self.scale
        self.d[1] = self.c[1] + np.sin(self.theta)*self.scale
        self.b[0] = self.a[0] + np.sin(self.theta)*self.scale
        self.b[1] = self.a[1] + np.cos(self.theta)*self.scale


if __name__ == '__main__':
    lane = StraightLane([0., -1.], [0., 1.], 0.1)
    x = tt.vector()
    lane.feature()(0, x, 0)

    print(lane)
    print(type(lane))
