# Copyright (c) 2009-2024 The Regents of the University of Michigan.
# Part of HOOMD-blue, released under the BSD 3-Clause License.

"""Long-range Lymburn repulsion ln(r) potential."""

# Import the C++ module.
from hoomd.resobee_hoomd_potentials import _lymburn_repulsion

# Impot the hoomd Python package and other necessary components.
from hoomd.md import pair
from hoomd.data.parameterdicts import TypeParameterDict
from hoomd.data.typeparam import TypeParameter


class LymburnRepulsion(pair.Pair):
    """Long-range Lymburn repulsion ln(r) potential."""

    # set static class data
    _ext_module = _lymburn_repulsion
    _cpp_class_name = "LymburnRepulsion"
    _accepted_modes = ("none", "shift", "xplor")

    def __init__(self, nlist, default_r_cut=None, default_r_on=0., strength=None, mode='none'):
        super().__init__(nlist, default_r_cut, default_r_on, mode)
        params = TypeParameter(
            'params', 'particle_types',
            TypeParameterDict(strength=strength, len_keys=2))
        self._add_typeparam(params)