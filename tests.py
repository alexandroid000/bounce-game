#! /usr/bin/env python

import unittest
from random import randint, random
import numpy as np

# using bounce-viz repo for maps and data structures
import sys
sys.path.append('../bounce_viz/src/')
from simple_polygon import Simple_Polygon
from maps import small_square

from game import *


class TestExamples(unittest.TestCase):

    # add global stuff here
    def setUp(self):

        self.env = Simple_Polygon("env", small_square[0], small_square[1:])
        self.g = Game(self.env)
        return

    def test_bounce(self):

        t1 = self.g.s_to_point(0.2)
        t2 = self.g.s_to_point(0.5)
        t3 = self.g.s_to_point(0.999)

        p1 = np.array([0.8, 0.])
        p2 = np.array([1., 1.])
        p3 = np.array([0., 0.004])
        np.testing.assert_almost_equal(t1,p1, decimal=7, verbose=True)
        np.testing.assert_almost_equal(t2,p2, decimal=7, verbose=True)
        np.testing.assert_almost_equal(t3,p3, decimal=7, verbose=True)


        #self.assertSequenceEqual(decode_policy(encode_policy(test1)), test1)
