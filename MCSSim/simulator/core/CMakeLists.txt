project(core)
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O3")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -pg -no-pie -O3")

set(SOURCE_FILES location.cpp transition.cpp timer.cpp var.cpp automaton.cpp network.cpp channel.cpp)
add_library(core ${SOURCE_FILES})
