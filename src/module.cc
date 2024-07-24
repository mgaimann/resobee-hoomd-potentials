// Copyright (c) 2009-2024 The Regents of the University of Michigan.
// Part of HOOMD-blue, released under the BSD 3-Clause License.

#include "EvaluatorLymburnRepulsion.h"

#ifdef ENABLE_HIP
#include "LymburnRepulsionGPU.h"
#endif

#include <pybind11/pybind11.h>

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
