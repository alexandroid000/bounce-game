#! /usr/bin/env python

import unittest
from backend import *
from utilities import *
from random import randint, random
import numpy as np


class TestExamples(unittest.TestCase):

    # add global stuff here
    def setUp(self):
        return

    def test_scatter(self):
        np.testing.assert_almost_equal(particle1.velocity,
                                       [-1., 1.],
                                       decimal=7, verbose=True)
        self.assertSequenceEqual(decode_policy(encode_policy(test1)), test1)
