
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>

#include <frc\commands\WaitUntilCommand.h>



#include <rpygen/frc__Command.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__WaitUntilCommand = 
    Pyfrc__Command<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__WaitUntilCommand : PyBasefrc__WaitUntilCommand<CxxBase> {
    using PyBasefrc__WaitUntilCommand<CxxBase>::PyBasefrc__WaitUntilCommand;



#ifndef RPYGEN_DISABLE_IsFinished_v
    bool IsFinished() override {
PYBIND11_OVERLOAD_NAME(bool, CxxBase, "isFinished", IsFinished,);    }
#endif



};

}; // namespace rpygen
