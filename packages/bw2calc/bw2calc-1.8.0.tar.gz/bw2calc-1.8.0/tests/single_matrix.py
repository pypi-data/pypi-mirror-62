# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from bw2calc.single_matrix import SingleMatrixLCA
import numpy as np
import pytest
import os


fixture = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fixtures",
    "single-matrix",
    "sm-fixture.tar.bz2"
)


def test_single_matrix():
    s = SingleMatrixLCA({"f": 1}, "sm-fixture.tar.bz2")
    s.calculate()
    assert s.scores['foo']
