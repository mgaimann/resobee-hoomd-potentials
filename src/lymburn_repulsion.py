# Copyright (c) 2009-2024 The Regents of the University of Michigan.
# Part of HOOMD-blue, released under the BSD 3-Clause License.

"""Long-range Lymburn repulsion ln(r) potential."""

# Import the C++ module.
from hoomd.data.parameterdicts import TypeParameterDict
from hoomd.data.typeparam import TypeParameter

# Import the hoomd Python package and other necessary components.
from hoomd.md import pair
from hoomd.resobee_hoomd_potentials import _resobee_hoomd_potentials


class LymburnRepulsion(pair.Pair):
    """Long-range Lymburn repulsion ln(r) potential."""

    # set static class data
    _ext_module = _resobee_hoomd_potentials
    _cpp_class_name = 'LymburnRepulsion'
    _accepted_modes = ('none', 'shift', 'xplor')

    def __init__(
        self, nlist, default_r_cut=None, default_r_on=0.0, strength=None, mode='none'
    ):
        super().__init__(nlist, default_r_cut, default_r_on, mode)
        params = TypeParameter(
            'params', 'particle_types', TypeParameterDict(strength=float, len_keys=1)
        )
        self._add_typeparam(params)
