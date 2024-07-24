# Copyright (c) 2009-2024 The Regents of the University of Michigan.
# Part of HOOMD-blue, released under the BSD 3-Clause License.

"""Test the version module."""

import hoomd.resobee_hoomd_potentials


def test_version():
    """Test the version attribute."""
    assert hoomd.resobee_hoomd_potentials.version.version == '0.1.0'
