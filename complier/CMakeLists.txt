project(tmach_compiler)

set(ROOT ..)
set(SRC_DIR ./src)

set(SOURCE ${SRC_DIR}/tmach_compiler.cpp ${SRC_DIR}/tcompiler.cpp)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${ROOT}/bin)

add_executable(tmc ${SOURCE})
