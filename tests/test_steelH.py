import unittest

from src.steelH import steelH


def test_Cube():
    stH = steelH()
    ans = stH.createCube()
    assert ans=="lua"

