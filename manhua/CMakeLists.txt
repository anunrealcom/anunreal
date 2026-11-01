# =============================================================================
#  manhua/  -- your film-scene (漫剧) code, built with normal CMake.
#  This is the only part you normally edit in CLion with full CMake features.
#
#  Recommended approach for extending Godot without forking its build:
#  develop a GDExtension (C++ shared library loaded by the Godot editor at
#  runtime). You need the Godot extension API headers (godot-cpp) which are
#  NOT in this repo; pull them separately, e.g. as a git submodule:
#
#     git submodule add https://github.com/godotengine/godot-cpp manhua/godot-cpp
#
#  Then uncomment the example target below once headers are present.
# =============================================================================
cmake_minimum_required(VERSION 3.21)
project(manhua LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Placeholder: add your sources here as you grow the project.
# file(GLOB_RECURSE MANHUA_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

# add_library(manhua SHARED ${MANHUA_SOURCES})
# target_include_directories(manhua PRIVATE
#     "${CMAKE_CURRENT_SOURCE_DIR}/godot-cpp/gdextension/auto_generated
#      ${CMAKE_CURRENT_SOURCE_DIR}/godot-cpp/include")
# target_link_libraries(manhua PRIVATE ${CMAKE_DL_LIBS})
