project(generated_components)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -O3")
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../simulator/core)
link_directories(${CMAKE_CURRRENT_BINARY_DIR}/../../simulator/core)

add_library(generated_components 
	T.cpp
	FPNPS.cpp
	EDF.cpp
	FPPS.cpp
	L.cpp
	CS.cpp
	common.cpp
)
target_link_libraries(generated_components core)
