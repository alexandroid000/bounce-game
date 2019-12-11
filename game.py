import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.patches import Polygon, Circle, FancyArrowPatch
from copy import copy

import sys
sys.path.insert(0, "./bounce-viz/src/")
from simple_polygon import Simple_Polygon
from helper.shoot_ray_helper import ClosestPtFromPt
from maps import small_square, poly1, bigpoly

TWOPI = 2*np.pi
EPSILON = 0.001

def rotate_vector(v, theta):
    vx, vy = v[0], v[1]
    return np.array( [np.cos(theta)*vx - np.sin(theta)*vy,
                     np.sin(theta)*vx + np.cos(theta)*vy])

def fix_angle(theta):
    if theta < 0:
        return fix_angle(theta+TWOPI)
    elif theta > TWOPI:
        return fix_angle(theta-TWOPI)
    else:
        return theta

class Game(object):

    def __init__(self, env):

        self.env = env
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(left=0.3, bottom=0.25)

        initial_amp = 0.01
        xs = [x for (x,y) in self.env.complete_vertex_list]
        ys = [y for (x,y) in self.env.complete_vertex_list]
        XMIN = np.amin(xs)-1
        XMAX = np.amax(xs)+1
        YMIN = np.amin(ys)-1
        YMAX = np.amax(ys)+1

        axis = plt.axis([XMIN,XMAX,YMIN,YMAX])

        # Sliders
        s_slider_ax = plt.axes([0.25, .15, 0.65, 0.03])
        self.slide_s = Slider(s_slider_ax, 'Start', 0, 1, valinit=initial_amp)

        theta_slider_ax = plt.axes([0.25, .1, 0.65, 0.03])
        self.slide_theta = Slider(theta_slider_ax, 'Theta', 0.01, 3.14, valinit=initial_amp)

        # Buttons
        rax = plt.axes([0.05, 0.7, 0.15, 0.15], facecolor='lightgoldenrodyellow')
        self.radio = RadioButtons(rax, ('Fixed', 'Fixed Monotonic', 'Relative'))
        self.radio.on_clicked(self.brulefunc)

        polys = self.draw_poly(self.env)
        scale = 0.01*(XMAX-XMIN)
        self.p = Circle([0.,0.], ec='r', fc='r', lw=2, radius=scale)
        self.ax.add_patch(self.p)

        self.s = 0.
        self.theta = np.pi/2
        self.brule = self.fixed_brule
        self.n = 20


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

    def relative_brule(self, theta, edge_i, prev_global_theta):
        new_global_theta = fix_angle(prev_global_theta + theta)
        pt1 = self.env.complete_vertex_list[edge_i]
        pt2 = self.env.complete_vertex_list[(edge_i + 1) % self.env.size]
        edge_v = pt2 - pt1
        edge_theta = np.arctan2(edge_v[1], edge_v[0])
        if new_global_theta > edge_theta and new_global_theta < (edge_theta + np.pi):
            return new_global_theta
        else:
            return self.relative_brule(theta, edge_i, new_global_theta)


    # compute theta relative to x axis for fixed bounce rule
    def fixed_brule(self, theta, edge_i, prev_global_theta):
        pt1 = self.env.complete_vertex_list[edge_i]
        pt2 = self.env.complete_vertex_list[(edge_i + 1) % self.env.size]
        edge_v = pt2 - pt1
        out_v = rotate_vector(edge_v, theta)
        global_theta = np.arctan2(out_v[1], out_v[0])
        return global_theta

    # compute theta relative to x axis for fixed monotonic bounce rule
    def fixed_monotonic_brule(self, theta, edge_i, prev_global_theta):
        pt1 = self.env.complete_vertex_list[edge_i]
        pt2 = self.env.complete_vertex_list[(edge_i + 1) % self.env.size]

        edge_v = pt2 - pt1
        theta_edge = np.arctan2(edge_v[1], edge_v[0])
        prev_global_theta_edge_frame = fix_angle(prev_global_theta - theta_edge)
        if prev_global_theta_edge_frame <= 0 or prev_global_theta_edge_frame <= np.pi:
            raise ValueError("rotation failed")
        # previous bounce coming in from the right
        elif prev_global_theta_edge_frame < 3*np.pi/2:
            # if theta would reverse direction, flip theta
            if theta < np.pi/2:
                theta = np.pi - theta
        # previous bounce coming in from the left
        elif prev_global_theta_edge_frame >= 3*np.pi/2 and prev_global_theta_edge_frame < 2*np.pi:
            if theta > np.pi/2:
                theta = np.pi - theta

        out_v = rotate_vector(edge_v, theta)
        global_theta = np.arctan2(out_v[1], out_v[0])
        return global_theta

    # theta defined relative to tangent. right pointing tangent theta = 0
    # normal theta = pi/2
    def do_bounce(self, pt, edge_i, theta, prev_global_theta, brule):
        global_theta = brule(theta, edge_i, prev_global_theta)
        state = (pt[0], pt[1], global_theta)
        ret = ClosestPtFromPt(state, self.env, last_bounce_edge=edge_i)
        if ret:
            bounce_point, bounce_edge = ret
            return bounce_point, bounce_edge, global_theta
        else:
            raise ValueError("bounce failed!")

    def make_trajectory(self):
        start_pt, j = self.s_to_point(self.s)
        pts = [start_pt]
        global_theta = self.theta

        for i in range(self.n):
            next_pt, next_edge, next_global_theta = self.do_bounce(
                                                    start_pt,
                                                    j,
                                                    self.theta,
                                                    global_theta,
                                                    self.brule)
            pts.append(next_pt)
            start_pt = next_pt
            j = next_edge
            global_theta = next_global_theta

        return pts

    def draw_bounces(self, traj):
        self.p.center = traj[0][0], traj[0][1]
        bounces = zip(traj, traj[1:])

        for (pt1, pt2) in bounces:
            a = FancyArrowPatch(posA = pt1, posB = pt2, arrowstyle="-")
            self.ax.add_patch(a)

    def update(self, val):
        # amp is the current value of the slider
        self.s = self.slide_s.val
        self.theta = self.slide_theta.val
        start_pt, j = self.s_to_point(self.s)
        bounces = self.make_trajectory()

        [p.remove() for p in reversed(self.ax.patches[2:])]

        self.draw_bounces(bounces)
        # redraw canvas while idle
        self.fig.canvas.draw_idle()

    def brulefunc(self, label):
        bdict = { 'Fixed': self.fixed_brule
                , 'Fixed Monotonic': self.fixed_monotonic_brule
                , 'Relative': self.relative_brule}
        self.brule = bdict[label]
        print(self.brule.__name__)
        bounces = self.make_trajectory()

        [p.remove() for p in reversed(self.ax.patches[2:])]
        self.draw_bounces(bounces)
        # redraw canvas while idle
        self.fig.canvas.draw_idle()

    def run(self):
        # call update function on slider value change
        self.slide_s.on_changed(self.update)
        self.slide_theta.on_changed(self.update)

        plt.show()

if __name__ == '__main__':


    env = Simple_Polygon("env", poly1[0], poly1[1:])

    g = Game(env)
    g.run()

