cmake_minimum_required(VERSION 2.8.3)
project(vo_comparision)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  roscpp
  sensor_msgs
  message_filters
  cv_bridge
)

## System dependencies are found with CMake's conventions
find_package(OpenCV REQUIRED)


###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(CATKIN_DEPENDS
    rospy
    roscpp
    sensor_msgs
    message_filters
    cv_bridge
)

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories( ${catkin_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})

add_executable(image_enhance  src/pirvs_enhance_images.cpp)
target_link_libraries(image_enhance ${catkin_LIBRARIES})
target_link_libraries(image_enhance ${OpenCV_LIBS} ${BULLET_LIBRARIES})
add_dependencies(image_enhance ${PROJECT_NAME}_generate_messages_cpp)
