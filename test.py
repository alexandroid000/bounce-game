import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.patches import Polygon

import sys
sys.path.append('../bounce_viz/src/')
from simple_polygon import Simple_Polygon
from maps import small_square

TWOPI = 2*np.pi
EPSILON = 0.0001

class Game(object):

    def __init__(self, environment):

        self.environment = environment
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

    def draw_trajectory(self, start, k):
        outer_map, holes_map = self.environment.compute_unit_interval_mapping()
        pts = env.complete_vertex_list
        n = env.size
        if start < 0.0 or start > 1.0:
            raise ValueError("Start position must be on polygon")
        else:
            #print(outer_map)
            startv = outer_map[0]
            i = 0
            while startv < start:
                i += 1
                startv = outer_map[i]
            print(pts[(i-1)%n])
            print((start-outer_map[(i-1)%n]))
            print(pts[i%n]-pts[(i-1)%n])
            start = pts[(i-1)%n]+(start-outer_map[(i-1)%n])*(pts[i]-pts[(i-1)%n])
            print(pts)
            print(start)

        return

    def update(self, val):
        # amp is the current value of the slider
        amp = self.samp.val
        # update curve
        self.l.set_ydata(amp*np.sin(self.t))
        polys = self.draw_poly(self.environment)
        # redraw canvas while idle
        self.fig.canvas.draw_idle()


    def run(self):
        # call update function on slider value change
        self.samp.on_changed(self.update)

        plt.show()

if __name__ == '__main__':


    env = Simple_Polygon("env", small_square[0], small_square[1:])

    g = Game(env)
    g.draw_trajectory(0.5, 5)
    #g.run()

