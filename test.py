import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.patches import Polygon

import sys
sys.path.append('../bounce_viz/src/')
from simple_polygon import Simple_Polygon
from maps import small_square

environment = Simple_Polygon("env", small_square[0], small_square[1:])

TWOPI = 2*np.pi

fig, ax = plt.subplots()

t = np.arange(0.0, TWOPI, 0.001)
initial_amp = .5
s = initial_amp*np.sin(t)
l, = plt.plot(t, s, lw=2)

axis = plt.axis([0,TWOPI,-1,1])

axamp = plt.axes([0.25, .03, 0.50, 0.02])
# Slider
samp = Slider(axamp, 'Amp', 0, 1, valinit=initial_amp)


def draw_poly(poly):
    patches = []

    outer = [p for (i,p) in poly.vertex_list_per_poly[0]]
    p = Polygon(outer, ec='k', lw=2, fc='none')
    patches.append(ax.add_patch(p))

    for hole in poly.vertex_list_per_poly[1:]:
        pass

    return patches

def draw_trajectory(bounce_rule, start, n):
    return

def update(val):
    global environment
    # amp is the current value of the slider
    amp = samp.val
    # update curve
    l.set_ydata(amp*np.sin(t))
    polys = draw_poly(environment)
    # redraw canvas while idle
    fig.canvas.draw_idle()

# call update function on slider value change
samp.on_changed(update)

plt.show()
