cmake_minimum_required(VERSION 3.17)
project(CompliePrincipleExp)

set(CMAKE_CXX_STANDARD 14)

include_directories(byyl_exp1)

add_executable(CompliePrincipleExp
        byyl_exp1/main.cpp
        byyl_exp1/main.h)
