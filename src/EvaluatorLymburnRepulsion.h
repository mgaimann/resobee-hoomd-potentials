// Copyright (c) 2009-2024 The Regents of the University of Michigan.
// Part of HOOMD-blue, released under the BSD 3-Clause License.

#ifndef __EVALUATOR_LYMBURN_REPULSION_H__
#define __EVALUATOR_LYMBURN_REPULSION_H__

#ifndef __HIPCC__
#include <string>
#endif

#include "hoomd/HOOMDMath.h"

/*! \file EvaluatorLymburnRepulsion.h
    \brief Defines the pair evaluator class for a long-ranged repulsion force ~1/r (potential:
   ln(r)) with a cutoff
*/

// need to declare these class methods with __device__ qualifiers when building in nvcc
// DEVICE is __host__ __device__ when included in nvcc and blank when included into the host
// compiler
#ifdef __HIPCC__
#define DEVICE __device__
#define HOSTDEVICE __host__ __device__
#else
#define DEVICE
#define HOSTDEVICE
#endif

namespace hoomd
    {
namespace md
    {

class EvaluatorLymburnRepulsion
    {
    public:
    //! Define the parameter type used by this pair potential evaluator
    struct param_type
        {
        Scalar strength; //!< Strength of the repulsion

        DEVICE void load_shared(char*& ptr, unsigned int& available_bytes) { }

        HOSTDEVICE void allocate_shared(char*& ptr, unsigned int& available_bytes) const { }

#ifdef ENABLE_HIP
        //! Set CUDA memory hints
        void set_memory_hint() const
            {
            // default implementation does nothing
            }
#endif

#ifndef __HIPCC__
        param_type() : strength(0) { }

        param_type(pybind11::dict v, bool managed = false)
            {
            strength = v["strength"].cast<Scalar>();
            }

        pybind11::dict asDict()
            {
            pybind11::dict v;
            v["strength"] = strength;
            return v;
            }
#endif
        }
#if HOOMD_LONGREAL_SIZE == 32
        __attribute__((aligned(8)));
#else
        __attribute__((aligned(16)));
#endif

    //! Constructs the long-ranged Lymburn repulsion interaction
    /*! \param _rsq Squared distance between the particles
        \param _rcutsq Squared distance at which the potential goes to 0
        \param _params Per type pair parameters of this potential
    */
    DEVICE EvaluatorLymburnRepulsion(Scalar _rsq, Scalar _rcutsq, const param_type& _params)
        : rsq(_rsq), rcutsq(_rcutsq), strength(_params.strength)
        {
        }

    //! no charge required
    DEVICE static bool needsCharge()
        {
        return false;
        }
    //! Accept the optional charge value
    /*! \param qi Charge of particle i
        \param qj Charge of particle j
    */
    DEVICE void setCharge(Scalar qi, Scalar qj) { }

    //! Evaluate the force and energy
    /*! \param force_divr Output parameter to write the computed force divided by r.
        \param pair_eng Output parameter to write the computed pair energy
        \param energy_shift If true, the potential must be shifted so that
        V(r) is continuous at the cutoff
        \note There is no need to check if rsq < rcutsq in this method.
        Cutoff tests are performed in PotentialPair.
        \note the force is given by:
        \mathbf{F}_{r,i}=\sum_{j=1}^{N_r}
       \frac{\mathbf{x}_i-\mathbf{x}_j}{\left\|\mathbf{x}_i-\mathbf{x}_j\right\|^2}

        \return True if they are evaluated or false if they are not because
        we are beyond the cutoff
    */
    DEVICE bool evalForceAndEnergy(Scalar& force_divr, Scalar& pair_eng, bool energy_shift)
        {
        // compute the force divided by r in force_divr
        if (rsq < rcutsq)
            {
            Scalar rinvsq = 1.0 / rsq;
            force_divr = strength * rinvsq;

            pair_eng = 0.0; // not implemented
            return true;
            }
        else
            return false;
        }

    //! Example doesn't eval LRC integrals
    DEVICE Scalar evalPressureLRCIntegral()
        {
        return 0;
        }

    //! Example doesn't eval LRC integrals
    DEVICE Scalar evalEnergyLRCIntegral()
        {
        return 0;
        }

#ifndef __HIPCC__
    //! Get the name of this potential
    /*! \returns The potential name.
     */
    static std::string getName()
        {
        return std::string("lymburn_repulsion");
        }

    std::string getShapeSpec() const
        {
        throw std::runtime_error("Shape definition not supported for this pair potential.");
        }
#endif

    protected:
    Scalar rsq;      //!< Stored rsq from the constructor
    Scalar rcutsq;   //!< Stored rcutsq from the constructor
    Scalar strength; //!< Stored strength from the constructor
    };

    } // end namespace md
    } // end namespace hoomd

#endif // __EVALUATOR_LYMBURN_REPULSION_H__
