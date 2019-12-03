import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.patches import Polygon
from copy import copy

import sys
sys.path.append('../bounce_viz/src/')
from simple_polygon import Simple_Polygon
from maps import small_square

TWOPI = 2*np.pi
EPSILON = 0.001

class Game(object):

    def __init__(self, env):

        self.env = env
        self.fig, self.ax = plt.subplots()

        self.t = np.arange(0.0, TWOPI, 0.001)
        initial_amp = .5
        s = initial_amp*np.sin(self.t)
        self.l, = plt.plot(self.t, s, lw=2)

        axis = plt.axis([0,TWOPI,-1,1])

        axamp = plt.axes([0.25, .03, 0.50, 0.02])
        # Slider
        self.samp = Slider(axamp, 'Amp', 0, 1, valinit=initial_amp)


    def draw_poly(self, poly):
        patches = []

        outer = [p for (i,p) in poly.vertex_list_per_poly[0]]
        p = Polygon(outer, ec='k', lw=2, fc='none')
        patches.append(self.ax.add_patch(p))

        # TODO implement holes
        for hole in poly.vertex_list_per_poly[1:]:
            pass

        return patches

    def s_to_point(self, s):
        outer_map, holes_map = self.env.compute_unit_interval_mapping()
        pts = self.env.complete_vertex_list
        n = self.env.size
        if s < 0.0 or s > 1.0:
            raise ValueError("Start position must be on polygon")
        else:
            sv = 0.
            j = 0
            for i in range(n):
                sv = outer_map[i]
                j = copy(i)
                if sv > s:
                    break
                elif i == n-1:
                    j = n
                    break
                elif abs(s - sv) < EPSILON:
                    break

            s_on_edge = (s-outer_map[(j-1)])/(outer_map[j]-outer_map[(j-1)])
            s_pt = pts[j-1] + s_on_edge*(pts[j%n]-pts[j-1])
            return s_pt

    def draw_bounces(self, traj):
        return

    def update(self, val):
        # amp is the current value of the slider
        amp = self.samp.val
        # update curve
        self.l.set_ydata(amp*np.sin(self.t))
        polys = self.draw_poly(self.env)
        # redraw canvas while idle
        self.fig.canvas.draw_idle()


    def run(self):
        # call update function on slider value change
        self.samp.on_changed(self.update)

        plt.show()

if __name__ == '__main__':


    env = Simple_Polygon("env", small_square[0], small_square[1:])

    g = Game(env)
    print(g.s_to_point(0.2))
    print(g.s_to_point(0.5))
    print(g.s_to_point(0.99))
    #g.run()

