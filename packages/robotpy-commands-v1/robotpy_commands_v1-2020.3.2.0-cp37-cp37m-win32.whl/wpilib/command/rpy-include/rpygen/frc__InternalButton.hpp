
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>

#include <frc\buttons\InternalButton.h>



#include <rpygen/frc__Button.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__InternalButton = 
    Pyfrc__Button<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__InternalButton : PyBasefrc__InternalButton<CxxBase> {
    using PyBasefrc__InternalButton<CxxBase>::PyBasefrc__InternalButton;



#ifndef RPYGEN_DISABLE_Get_v
    bool Get() override {
PYBIND11_OVERLOAD_NAME(bool, CxxBase, "get", Get,);    }
#endif



};

}; // namespace rpygen
