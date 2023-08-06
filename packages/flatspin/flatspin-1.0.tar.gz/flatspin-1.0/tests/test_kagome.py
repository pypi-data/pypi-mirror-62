import numpy as np
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal
from itertools import groupby

from flatspin import KagomeSpinIce

def test_init(opencl):
    a = 1/3
    si = KagomeSpinIce(size=(3,3), lattice_spacing=a, **opencl)

    assert si.size == (3,3)
    assert si.spin_count == 6 + 4 + 7 + 4 + 7 + 4 + 6
    assert si.num_neighbors == 4

def test_labels():
    # even
    si = KagomeSpinIce(size=(2,2))
    assert_array_equal(si.labels,
            [(0,0), (0,1), (0,2), (0,3),
             (1,0), (1,1), (1,2),
             (2,0), (2,1), (2,2), (2,3), (2,4),
             (3,0), (3,1), (3,2),
             (4,1), (4,2), (4,3), (4,4)])

    # odd
    si = KagomeSpinIce(size=(3,3))
    assert_array_equal(si.labels,
            [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5),
             (1,0), (1,1), (1,2), (1,3),
             (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6),
             (3,0), (3,1), (3,2), (3,3),
             (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6),
             (5,0), (5,1), (5,2), (5,3),
             (6,0), (6,1), (6,2), (6,3), (6,4), (6,5)])


def test_indexof():
    si = KagomeSpinIce(size=(4,3))

    inds = list(map(si.indexof, si.labels))
    assert_array_equal(inds, si.indices())

def test_geometry():
    si = KagomeSpinIce(size=(3,3), lattice_spacing=1/3)
    L = si.L

    # alternating 45 and 135 degrees
    a30 = np.deg2rad(30)
    a90 = np.deg2rad(90)

    assert_allclose(si.angle[L[0::4,0::2]], -a30)
    assert_allclose(si.angle[L[0::4,1::2]], a30)

    assert_allclose(si.angle[L[1::4]], a90)

    assert_allclose(si.angle[L[2::4,0::2]], a30)
    assert_allclose(si.angle[L[2::4,1::2]], -a30)

    # horizontal spacing between "horizontal" magnets is a
    a = si.lattice_spacing
    # vertical spacing between all magnets is a * sqrt(3) / 2
    av = a * np.sqrt(3)/2

    assert_allclose(si.pos[L[0], 0], a/2 + a*np.arange(6))
    assert_array_equal(si.pos[L[0], 1], 0)

    assert_allclose(si.pos[L[1], 0], 2*a*np.arange(4))
    assert_array_equal(si.pos[L[1], 1], av)

    assert_allclose(si.pos[L[2], 0], a/2 + a*np.arange(7))
    assert_array_equal(si.pos[L[2], 1], 2*av)

    assert_allclose(si.pos[L[3], 0], a+2*a*np.arange(4))
    assert_array_equal(si.pos[L[3], 1], 3*av)

    assert_allclose(si.pos[L[4], 0], a/2 + a*np.arange(7))
    assert_array_equal(si.pos[L[4], 1], 4*av)

    assert_allclose(si.pos[L[5], 0], 2*a*np.arange(4))
    assert_array_equal(si.pos[L[5], 1], 5*av)

    assert_allclose(si.pos[L[6], 0], a/2 + a*np.arange(6))
    assert_array_equal(si.pos[L[6], 1], 6*av)


def test_num_neighbors():
    size = (10,10)

    # nearest neighborhood (default)
    si = KagomeSpinIce(size=size)
    assert si.num_neighbors == 4

    # global neighborhood
    si = KagomeSpinIce(size=size, neighbor_distance=np.inf)
    assert si.num_neighbors == si.spin_count - 1


def test_neighbors():
    size = (2,2)
    si = KagomeSpinIce(size=size)
    L = si.L

    # First "horizontal" row
    i = L[0,0]
    ns = list(si.neighbors(i))
    assert ns == [L[0,1], L[1,0]]

    i = L[0,1]
    ns = list(si.neighbors(i))
    assert ns == [L[0,0], L[0,2], L[1,1]]

    i = L[0,3]
    ns = list(si.neighbors(i))
    assert ns == [L[0,2], L[1,2]]

    # First vertical row
    i = L[1,0]
    ns = list(si.neighbors(i))
    assert ns == [L[0,0], L[2,0]]

    i = L[1,1]
    ns = list(si.neighbors(i))
    assert ns == [L[0,1], L[0,2], L[2,1], L[2,2]]

    i = L[1,2]
    ns = list(si.neighbors(i))
    assert ns == [L[0,3], L[2,3], L[2,4]]

    # Middle "horizontal" row
    i = L[2,0]
    ns = list(si.neighbors(i))
    assert ns == [L[1,0], L[2,1], L[3,0]]

    i = L[2,2]
    ns = list(si.neighbors(i))
    assert ns == [L[1,1], L[2,1], L[2,3], L[3,1]]

    i = L[2,4]
    ns = list(si.neighbors(i))
    assert ns == [L[1,2], L[2,3], L[3,2]]

    # Second vertical row
    i = L[3,0]
    ns = list(si.neighbors(i))
    assert ns == [L[2,0], L[2,1], L[4,1]]

    i = L[3,1]
    ns = list(si.neighbors(i))
    assert ns == [L[2,2], L[2,3], L[4,2], L[4,3]]

    i = L[3,2]
    ns = list(si.neighbors(i))
    assert ns == [L[2,4], L[4,4]]

    # Top "horizontal" row
    i = L[4,1]
    ns = list(si.neighbors(i))
    assert ns == [L[3,0], L[4,2]]

    i = L[4,3]
    ns = list(si.neighbors(i))
    assert ns == [L[3,1], L[4,2], L[4,4]]

    i = L[4,4]
    ns = list(si.neighbors(i))
    assert ns == [L[3,2], L[4,3]]

def test_spin_dipolar_field(opencl):
    # default lattice spacing = 1 such that NN islands have coupling strength 1.5
    size = (3,3)
    si = KagomeSpinIce(size=size, **opencl)
    L = si.L

    j_NN = np.array([7/4, np.sqrt(3)/4])
    j_NNN = np.array([-10/(24*np.sqrt(3)), 1/12])

    assert si.spin_dipolar_field(L[0,0], L[0,1]) == approx(j_NN)
    assert si.spin_dipolar_field(L[0,0], L[1,0]) == approx([-1, 1] * j_NN)
    assert si.spin_dipolar_field(L[0,0], L[1,1]) == approx([-1, 1] * j_NNN)
    assert si.spin_dipolar_field(L[0,0], L[2,0]) == approx(j_NNN)

    assert si.spin_dipolar_field(L[1,0], L[0,0]) == approx(-j_NN)
    assert si.spin_dipolar_field(L[1,0], L[0,1]) == approx([1, -1] * j_NNN)

    assert si.spin_dipolar_field(L[1,1], L[0,1]) == approx([1, -1] * j_NN)
    assert si.spin_dipolar_field(L[1,1], L[0,2]) == approx(-j_NN)
    assert si.spin_dipolar_field(L[1,1], L[2,1]) == approx(-j_NN)
    assert si.spin_dipolar_field(L[1,1], L[2,2]) == approx([1, -1] * j_NN)
    assert si.spin_dipolar_field(L[1,1], L[0,0]) == approx(-j_NNN)
    assert si.spin_dipolar_field(L[1,1], L[0,3]) == approx([1, -1] * j_NNN)
    assert si.spin_dipolar_field(L[1,1], L[2,0]) == approx([1, -1] * j_NNN)
    assert si.spin_dipolar_field(L[1,1], L[2,3]) == approx(-j_NNN)

def test_dipolar_field(opencl):
    size = (3,3)
    si = KagomeSpinIce(size=size, neighbor_distance=1, **opencl)
    L = si.L

    j_NN = np.array([7/4, np.sqrt(3)/4])
    j_NNN = np.array([-10/(24*np.sqrt(3)), 1/12])

    assert si.dipolar_field(L[1,1]) == approx([0, -4] * j_NN)
    si.flip(L[2,1])
    assert si.dipolar_field(L[1,1]) == approx([2, -2] * j_NN)
    si.flip(L[0,2])
    assert si.dipolar_field(L[1,1]) == approx([4, 0] * j_NN)

def test_external_field(opencl):
    size = (3,3)
    si = KagomeSpinIce(size=size, neighbor_distance=1, **opencl)
    L = si.L
    a30 = np.deg2rad(30)
    cos30 = np.cos(a30)
    sin30 = np.sin(a30)
    cos60 = np.cos(np.deg2rad(60))
    sin60 = np.sin(np.deg2rad(60))

    assert si.external_field(L[0,0]) == approx([0, 0])
    assert si.external_field(L[1,0]) == approx([0, 0])

    # Horizontal
    si.set_h_ext((1,0))
    assert si.external_field(L[0,0]) == approx([cos30, sin30])
    assert si.external_field(L[0,1]) == approx([cos30, -sin30])
    assert si.external_field(L[1,0]) == approx([0, -1])

    # Vertical
    si.set_h_ext((0,1))
    assert si.external_field(L[0,0]) == approx([-sin30, cos30])
    assert si.external_field(L[0,1]) == approx([sin30, cos30])
    assert si.external_field(L[1,0]) == approx([1, 0])

    # 30 degrees
    si.set_h_ext((cos30, sin30))
    assert si.external_field(L[0,0]) == approx([cos60, sin60])
    assert si.external_field(L[0,1]) == approx([1, 0])
    assert si.external_field(L[1,0]) == approx([sin30, -cos30])

    # -30 degrees
    si.set_h_ext((np.cos(-a30), np.sin(-a30)))
    assert si.external_field(L[0,0]) == approx([1, 0])
    assert si.external_field(L[0,1]) == approx([cos60, -sin60])
    assert si.external_field(L[1,0]) == approx([-sin30, -cos30])

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_flippable(opencl, switching):
    si = KagomeSpinIce(size=(4,4), hc=2, switching=switching, **opencl)

    if switching == "budrikis":
        assert len(si.flippable()) == 0
    elif switching == "sw":
        assert len(si.flippable()) == 2

    si.flip(si.L[0,1])
    E = si.switching_energy()
    flippable = [i for i in si.indices() if E[i] > 0]
    assert len(flippable) > 0
    assert_array_equal(si.flippable(), flippable)

    si.polarize()
    si.set_h_ext([-20, -20])
    assert len(si.flippable()) == si.spin_count

def test_find_vertices():
    si = KagomeSpinIce(size=(3,3))
    L = si.L
    vi, vj, indices = si.find_vertices()

    assert_array_equal(vi, [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5])
    assert_array_equal(vj, [3, 7, 3, 7, 11, 1, 5, 9, 1, 5, 9, 3, 7, 11, 3, 7])

    assert tuple(indices[0]) == (L[0,1], L[0,2], L[1,1])
    assert tuple(indices[1]) == (L[0,3], L[0,4], L[1,2])

    assert tuple(indices[2]) == (L[1,1], L[2,1], L[2,2])
    assert tuple(indices[3]) == (L[1,2], L[2,3], L[2,4])
    assert tuple(indices[4]) == (L[1,3], L[2,5], L[2,6])

    assert tuple(indices[5]) == (L[2,0], L[2,1], L[3,0])
    assert tuple(indices[6]) == (L[2,2], L[2,3], L[3,1])
    assert tuple(indices[7]) == (L[2,4], L[2,5], L[3,2])

    assert tuple(indices[8])  == (L[3,0], L[4,0], L[4,1])
    assert tuple(indices[9])  == (L[3,1], L[4,2], L[4,3])
    assert tuple(indices[10]) == (L[3,2], L[4,4], L[4,5])

    assert tuple(indices[11]) == (L[4,1], L[4,2], L[5,1])
    assert tuple(indices[12]) == (L[4,3], L[4,4], L[5,2])
    assert tuple(indices[13]) == (L[4,5], L[4,6], L[5,3])

    assert tuple(indices[14]) == (L[5,1], L[6,1], L[6,2])
    assert tuple(indices[15]) == (L[5,2], L[6,3], L[6,4])

def test_vertex_type():
    si = KagomeSpinIce(size=(2,2))
    L = si.L
    # polarized: all vertices type 1

    # make vertex (2,0) type 2 (3 out)
    si.flip(L[2,0])

    # make vertex (2,1) type 2 (3 in)
    si.flip(L[2,3])
    si.flip(L[3,1])

    vertex = si.vertices()

    assert si.vertex_type(vertex[0]) == 1
    assert si.vertex_type(vertex[1]) == 1
    assert si.vertex_type(vertex[2]) == 1
    assert si.vertex_type(vertex[3]) == 2
    assert si.vertex_type(vertex[4]) == 2
    assert si.vertex_type(vertex[5]) == 1

def test_spin_grid(opencl):
    ls = 1/3
    si = KagomeSpinIce(size=(2,2), lattice_spacing=ls, **opencl)

    a30 = np.deg2rad(30)
    a90 = np.deg2rad(90)
    v30n = [np.cos(-a30), np.sin(-a30)]
    v30p = [np.cos(a30), np.sin(a30)]
    v90 = [0, 1]
    v0 = [0, 0]

    # grid_spacing == lattice_spacing
    grid = si.spin_grid()
    assert grid.shape == (5, 11, 2)
    expect = [[v0, v30n, v0, v30p, v0, v30n, v0, v30p, v0, v0, v0],
              [v90, v0, v0, v0, v90, v0, v0, v0, v90, v0, v0],
              [v0, v30p, v0, v30n, v0, v30p, v0, v30n, v0, v30p, v0],
              [v0, v0, v90, v0, v0, v0, v90, v0, v0, v0, v90],
              [v0, v0, v0, v30p, v0, v30n, v0, v30p, v0, v30n, v0]]
    assert_allclose(grid, np.array(expect))
