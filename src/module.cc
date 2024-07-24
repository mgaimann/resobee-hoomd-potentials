// Copyright (c) 2009-2024 The Regents of the University of Michigan.
// Part of HOOMD-blue, released under the BSD 3-Clause License.

// Include the defined classes that are to be exported to python
#include "EvaluatorLymburnRepulsion.h"

#include "hoomd/md/PotentialPair.h"
#include <pybind11/pybind11.h>
#ifdef ENABLE_HIP
#include "hoomd/md/PotentialPairGPU.h"
#endif

namespace hoomd
    {
namespace md
    {

PYBIND11_MODULE(_resobee_hoomd_potentials, m)
    {
    detail::export_PotentialPair<LymburnRepulsion>(m, "LymburnRepulsion");

#ifdef ENABLE_HIP
    detail::export_PotentialPairGPU<LymburnRepulsion>(m, "LymburnRepulsionGPU");
#endif
    }

    } // end namespace md
    } // end namespace hoomd
