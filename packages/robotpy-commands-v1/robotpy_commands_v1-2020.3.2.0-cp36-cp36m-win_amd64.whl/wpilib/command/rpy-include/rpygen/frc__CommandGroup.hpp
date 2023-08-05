
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>

#include <frc\commands\CommandGroup.h>



#include <rpygen/frc__Command.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__CommandGroup = 
    Pyfrc__Command<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__CommandGroup : PyBasefrc__CommandGroup<CxxBase> {
    using PyBasefrc__CommandGroup<CxxBase>::PyBasefrc__CommandGroup;



#ifndef RPYGEN_DISABLE_Initialize_v
    void Initialize() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "initialize", Initialize,);    }
#endif

#ifndef RPYGEN_DISABLE_Execute_v
    void Execute() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "execute", Execute,);    }
#endif

#ifndef RPYGEN_DISABLE_IsFinished_v
    bool IsFinished() override {
PYBIND11_OVERLOAD_NAME(bool, CxxBase, "isFinished", IsFinished,);    }
#endif

#ifndef RPYGEN_DISABLE_End_v
    void End() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "end", End,);    }
#endif

#ifndef RPYGEN_DISABLE_Interrupted_v
    void Interrupted() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "interrupted", Interrupted,);    }
#endif

#ifndef RPYGEN_DISABLE__Initialize_v
    void _Initialize() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "_initialize", _Initialize,);    }
#endif

#ifndef RPYGEN_DISABLE__Execute_v
    void _Execute() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "_execute", _Execute,);    }
#endif

#ifndef RPYGEN_DISABLE__End_v
    void _End() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "_end", _End,);    }
#endif

#ifndef RPYGEN_DISABLE__Interrupted_v
    void _Interrupted() override {
PYBIND11_OVERLOAD_NAME(void, CxxBase, "_interrupted", _Interrupted,);    }
#endif



};

}; // namespace rpygen
