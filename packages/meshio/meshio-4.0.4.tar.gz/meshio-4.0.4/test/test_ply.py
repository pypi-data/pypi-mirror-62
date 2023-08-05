import os

import numpy
import pytest

import helpers
import meshio


@pytest.mark.parametrize(
    "mesh",
    [
        # helpers.tri_mesh,
        # helpers.quad_mesh,
        # helpers.tri_quad_mesh,
        helpers.add_point_data(helpers.tri_mesh, 1, dtype=int),
        helpers.add_point_data(helpers.tri_mesh, 1, dtype=float),
        # helpers.add_cell_data(helpers.tri_mesh, [("a", (), numpy.float64)]),
        # helpers.add_cell_data(helpers.tri_mesh, [("a", (2,), numpy.float64)]),
        # helpers.add_cell_data(helpers.tri_mesh, [("a", (3,), numpy.float64)]),
    ],
)
@pytest.mark.parametrize("binary", [False, True])
def test_ply(mesh, binary):
    def writer(*args, **kwargs):
        return meshio.ply.write(*args, binary=binary, **kwargs)

    for k, c in enumerate(mesh.cells):
        mesh.cells[k] = meshio.CellBlock(c.type, c.data.astype(numpy.int32))

    helpers.write_read(writer, meshio.ply.read, mesh, 1.0e-12)


@pytest.mark.parametrize(
    "filename, ref_sum, ref_num_cells",
    [("bun_zipper_res4.ply", 3.414583969116211e01, 948)],
)
def test_reference_file(filename, ref_sum, ref_num_cells):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, "meshes", "ply", filename)
    mesh = meshio.read(filename)
    tol = 1.0e-2
    s = numpy.sum(mesh.points)
    assert abs(s - ref_sum) < tol * abs(ref_sum)
    assert len(mesh.get_cells_type("triangle")) == ref_num_cells
