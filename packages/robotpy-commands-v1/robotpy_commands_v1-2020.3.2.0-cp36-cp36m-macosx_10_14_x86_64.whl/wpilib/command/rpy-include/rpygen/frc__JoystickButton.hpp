
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>

#include <frc/buttons/JoystickButton.h>



#include <rpygen/frc__Button.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__JoystickButton = 
    Pyfrc__Button<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__JoystickButton : PyBasefrc__JoystickButton<CxxBase> {
    using PyBasefrc__JoystickButton<CxxBase>::PyBasefrc__JoystickButton;



#ifndef RPYGEN_DISABLE_Get_v
    bool Get() override {
PYBIND11_OVERLOAD_NAME(bool, CxxBase, "get", Get,);    }
#endif



};

}; // namespace rpygen
