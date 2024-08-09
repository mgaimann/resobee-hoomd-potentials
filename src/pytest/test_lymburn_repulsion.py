# Copyright (c) 2009-2024 The Regents of the University of Michigan.
# Part of HOOMD-blue, released under the BSD 3-Clause License.

"""Lymburn Repulsion Force unit tests."""

# Import the plugin module.
import itertools

# Import the hoomd Python package.
import hoomd
import numpy
import pytest
from hoomd.resobee_hoomd_potentials.lymburn_repulsion import LymburnRepulsion


def apply_pbcs_to_vector(vector: numpy.ndarray, box_size: float) -> numpy.ndarray:
    """Apply periodic boundary conditions (PBCs) to a vector.

    This function modifies a given vector by applying periodic boundary
    conditions, ensuring that the vector remains within the simulation
    box. If any component of the vector exceeds half the box size, it is
    adjusted to reflect the periodic boundaries.

    Parameters:
    ----------
    vector : numpy.ndarray
        The vector to which periodic boundary conditions are applied,
        represented as a 1D array with 3 elements.
    box_size : float
        The size of the simulation box along one dimension.

    Returns:
    -------
    numpy.ndarray
        The vector after applying periodic boundary conditions.
    """
    for i in range(3):
        if vector[i] > box_size * 0.5:
            vector[i] -= box_size
        elif vector[i] < -box_size * 0.5:
            vector[i] += box_size
    return vector


def get_1_over_r_force(
    pos_a: numpy.ndarray,
    pos_b: numpy.ndarray,
    r_cut: float,
    strength: float,
    box_size: float,
) -> numpy.ndarray:
    """Calculate the 1/r repulsive force between two particles.

    This function computes the force between two particles based on
    a 1/r repulsion model, applying periodic boundary conditions (PBCs).
    If the distance between the particles exceeds the cutoff distance
    `r_cut`, the force is set to zero.

    Parameters:
    ----------
    pos_a : numpy.ndarray
        Position of the first particle as a 1D array with 3 elements.
    pos_b : numpy.ndarray
        Position of the second particle as a 1D array with 3 elements.
    r_cut : float
        The cutoff distance beyond which the force is not calculated.
    strength : float
        The strength of the repulsion force.
    box_size : float
        The size of the box in which particles are contained, used for
        applying periodic boundary conditions.

    Returns:
    -------
    numpy.ndarray
        The force vector acting on the first particle due to the second
        particle, as a 1D array with 3 elements. Returns a zero vector
        if the distance between the particles exceeds `r_cut`.
    """
    r = pos_b - pos_a
    r = apply_pbcs_to_vector(r, box_size)
    r_abs = numpy.linalg.norm(r)
    if r_abs > r_cut:
        return numpy.zeros(3)
    return -r * strength / r_abs**2


# Python implementation of the pair force
def get_lymburn_repulsion_forces(
    positions: numpy.ndarray, r_cut: float, strength: float, box_size: float
) -> numpy.ndarray:
    """Calculate the Lymburn repulsion forces between pairs of particles.

    This function computes the forces based on the 1/r repulsion model
    for a set of particles confined in a box. The forces are computed
    pairwise and are subject to a cutoff distance `r_cut`.

    Parameters:
    ----------
    positions : numpy.ndarray
        Array of particle positions with shape (N, 3), where N is the
        number of particles.
    r_cut : float
        The cutoff distance beyond which the force is not calculated.
    strength : float
        The strength of the repulsion force.
    box_size : float
        The size of the box in which particles are contained.

    Returns:
    -------
    numpy.ndarray
        Array of computed forces with shape (N, 3), where N is the
        number of particles.
    """
    forces_manual = numpy.zeros((positions.shape[0], 3), dtype=numpy.float64)

    for i in range(positions.shape[0]):
        for j in range(i):
            pos_a = positions[i]
            pos_b = positions[j]
            this_force = get_1_over_r_force(pos_a, pos_b, r_cut, strength, box_size)
            forces_manual[i] += this_force
            forces_manual[j] -= this_force

    return forces_manual


distances = [0.1, 0.5, 1.0, 2.0, 5.0]
modes = ['none']
r_cuts = [1.0, 2.0]
strengths = [2.0, 0.01]
box_sizes = [10.0, 20.0]
testdata = list(itertools.product(distances, r_cuts, strengths, box_sizes, modes))


@pytest.mark.parametrize(
    ('distance', 'r_cut', 'strength', 'box_size', 'mode'), testdata
)
def test_force_and_energy_eval(
    simulation_factory,
    two_particle_snapshot_factory,
    distance,
    r_cut,
    strength,
    box_size,
    mode,
):
    """Test the force and energy evaluation of the Lymburn repulsion model.

    This function sets up a two-particle simulation using the HOOMD-blue
    framework and tests the computed forces against the Python implementation
    of the Lymburn repulsion model. It ensures that the forces and energies
    produced by the HOOMD simulation match those calculated in Python.

    Parameters:
    ----------
    simulation_factory : callable
        A factory fixture to create the simulation context.
    two_particle_snapshot_factory : callable
        A factory fixture to create a snapshot with two particles separated
        by a given distance.
    distance : float
        The distance between the two particles in the snapshot.
    r_cut : float
        The cutoff distance beyond which the force is not calculated.
    strength : float
        The strength of the repulsion force.
    box_size : float
        The size of the simulation box in which particles are contained.
    mode : str
        The mode of force evaluation in the HOOMD-blue LymburnRepulsion
        pair potential.

    Returns:
    -------
    None
    """
    # Build the simulation from the factory fixtures defined in
    # hoomd/conftest.py.
    sim = simulation_factory(two_particle_snapshot_factory(d=distance))

    # Setup integrator and force.
    integrator = hoomd.md.Integrator(dt=0.001)
    nve = hoomd.md.methods.ConstantVolume(hoomd.filter.All())

    cell = hoomd.md.nlist.Cell(buffer=0.4)
    lymburn_repulsion: hoomd.md.pair.Pair = LymburnRepulsion(cell, mode=mode)
    lymburn_repulsion.params[('A', 'A')] = dict(strength=strength)
    integrator.forces = [lymburn_repulsion]
    integrator.methods = [nve]

    sim.operations.integrator = integrator

    sim.run(0)
    snap = sim.state.get_snapshot()
    if snap.communicator.rank == 0:
        positions = snap.particles.position

        # Compute force and energy from Python
        f = get_lymburn_repulsion_forces(positions, r_cut, strength, box_size)

    # Test that the forces and energies match that predicted by the Python
    # implementation.
    forces = numpy.array(lymburn_repulsion.forces)
    if snap.communicator.rank == 0:
        numpy.testing.assert_array_almost_equal(forces, f, decimal=6)
