import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.patches import Polygon, Circle
from copy import copy

import sys
sys.path.append('../bounce_viz/src/')
from simple_polygon import Simple_Polygon
from helper.shoot_ray_helper import ClosestPtFromPt
from maps import small_square, poly1, bigpoly

TWOPI = 2*np.pi
EPSILON = 0.001

def rotate_vector(v, theta):
    vx, vy = v[0], v[1]
    return np.array( [np.cos(theta)*vx - np.sin(theta)*vy,
                     np.sin(theta)*vx + np.cos(theta)*vy])

class Game(object):

    def __init__(self, env):

        self.env = env
        self.fig, self.ax = plt.subplots()

        self.t = np.arange(0.0, TWOPI, 0.001)
        initial_amp = .5
        s = initial_amp*np.sin(self.t)
        #self.l, = plt.plot(self.t, s, lw=2)
        xs = [x for (x,y) in self.env.complete_vertex_list]
        ys = [y for (x,y) in self.env.complete_vertex_list]
        XMIN = np.amin(xs)-1
        XMAX = np.amax(xs)+1
        YMIN = np.amin(ys)-1
        YMAX = np.amax(ys)+1

        axis = plt.axis([XMIN,XMAX,YMIN,YMAX])

        axamp = plt.axes([0.25, .03, 0.50, 0.02])
        # Slider
        self.samp = Slider(axamp, 'Start', 0, 1, valinit=initial_amp)
        polys = self.draw_poly(self.env)
        scale = 0.01*(XMAX-XMIN)
        self.p = Circle([0.,0.], ec='r', fc='r', lw=2, radius=scale)
        self.ax.add_patch(self.p)


    def draw_poly(self, poly):

        outer = [p for (i,p) in poly.vertex_list_per_poly[0]]
        p = Polygon(outer, ec='k', lw=2, fc='none')
        self.ax.add_patch(p)

        # TODO implement holes
        for hole in poly.vertex_list_per_poly[1:]:
            pass


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
            return s_pt, j-1

    # compute theta relative to x axis for fixed bounce rule
    def fixed_brule(self, theta, edge_i):
        pt1 = self.env.complete_vertex_list[edge_i]
        pt2 = self.env.complete_vertex_list[(edge_i + 1) % self.env.size]
        edge_v = pt2 - pt1
        out_v = rotate_vector(edge_v, theta)
        global_theta = np.arctan2(out_v[1], out_v[0])
        return global_theta

    # theta defined relative to tangent. right pointing tangent theta = 0
    # normal theta = pi/2
    def do_bounce(self, pt, edge_i, theta):
        global_theta = self.fixed_brule(theta, edge_i)
        state = (pt[0], pt[1], global_theta)
        ret = ClosestPtFromPt(state, self.env, last_bounce_edge=-1)
        if ret:
            bounce_point, bounce_edge = ret
            return bounce_point, bounce_edge
        else:
            raise ValueError("bounce failed!")

    def make_trajectory(self, s, theta, n):
        start_pt, j = self.s_to_point(s)
        pts = [start_pt]

        for i in range(n):
            next_pt, next_edge = self.do_bounce(start_pt, j, theta)
            pts.append(next_pt)
            start_pt = next_pt
            j = next_edge

        return pts

    def draw_bounces(self, traj):
        self.p.center = traj[0][0], traj[0][1]
        bounces = zip(traj, traj[1:])

        for (pt1, pt2) in bounces:
            arrow = plt.arrow(pt1[0], pt1[1], pt2[0], pt2[1])

    def update(self, val):
        # amp is the current value of the slider
        s = self.samp.val
        start_pt, j = self.s_to_point(s)
        theta = 0.2
        n = 2
        #bounces = self.make_trajectory(s, theta, n)

        self.draw_bounces([start_pt])
        # redraw canvas while idle
        self.fig.canvas.draw_idle()


    def run(self):
        # call update function on slider value change
        self.samp.on_changed(self.update)

        plt.show()

if __name__ == '__main__':

    N = 2

    env = Simple_Polygon("env", bigpoly[0], bigpoly[1:])

    g = Game(env)
    g.run()

