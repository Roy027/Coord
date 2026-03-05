import pytest
import numpy as np
from coord_ml.geometry import round_decimals_down, coordinates_to_planes, planes_to_dot_products

def test_round_decimals_down():
    assert round_decimals_down(1.2345, 2) == 1.23
    assert round_decimals_down(1.2345, 0) == 1.0
    assert round_decimals_down(0.99, 1) == 0.9
    with pytest.raises(TypeError):
        round_decimals_down(1.23, "2")

def test_coordinates_to_planes_tetrahedral():
    # Simple tetrahedral-like coordinates
    # Center at (0,0,0)
    center = ("O", (0, 0, 0))
    p1 = ("H1", (1, 1, 1))
    p2 = ("H2", (-1, -1, 1))
    p3 = ("H3", (1, -1, -1))
    p4 = ("H4", (-1, 1, -1))
    
    xyz = [center, p1, p2, p3, p4]
    
    planes = coordinates_to_planes(xyz)
    # For CN4, we expect comb(4, 2) = 6 planes if center is at 0
    # Actually, the logic in original script was:
    # for j in range(1,num): for k in range(j+1,num):
    # This picks pairs of neighbors to form a plane with the center.
    assert len(planes) == 6

def test_planes_to_dot_products():
    # Two orthogonal planes
    plane1 = np.array([1, 0, 0])
    plane2 = np.array([0, 1, 0])
    dots = planes_to_dot_products([plane1, plane2])
    assert len(dots) == 1
    assert dots[0] == 0.0

    # Two identical planes
    dots_same = planes_to_dot_products([plane1, plane1])
    assert dots_same[0] == 1.0
