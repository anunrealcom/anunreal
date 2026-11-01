# =============================================================================
#  Godot "manhua" superbuild (CMake shell around SCons)
# -----------------------------------------------------------------------------
#  Godot's own build system is SCons. We do NOT rewrite it. Instead this
#  CMake project is a thin shell that:
#    1. triggers `scons` to build the (trimmed) Godot editor binary, and
#    2. builds YOUR manhua/film-scene code as a normal CMake target, so you
#       get full CLion CMake editing/debugging for the parts you actually write.
#
#  Open this folder in CLion with the CMake profile (not Compilation Database).
#  Build = runs scons (incremental). Debug/Run = use the "Godot Editor" run
#  config (see .run/Godot Editor.run.xml), which launches bin/...exe.
# =============================================================================
cmake_minimum_required(VERSION 3.21)
project(godot_manhua_superbuild LANGUAGES NONE)

# ---- tool paths (mirror build_editor_dev.bat) -------------------------------
set(PYTHON "C:/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe")

# ---- manhua-focused SCons arguments -----------------------------------------
# Keep in sync with build_editor_dev.bat. These disable XR/C#/FBX/CSG/heavy
# physics/navigation/networking/compressed-textures/etc.
set(SCONS_ARGS
    platform=windows
    target=editor
    dev_build=yes
    accesskit=no
    d3d12=no
    module_mono_enabled=no
    module_fbx_enabled=no
    module_csg_enabled=no
    module_gridmap_enabled=no
    module_raycast_enabled=no
    module_openxr_enabled=no
    module_mobile_vr_enabled=no
    module_webxr_enabled=no
    module_xr_enabled=no
    module_camera_enabled=no
    module_jolt_physics_enabled=no
    module_navigation_2d_enabled=no
    module_navigation_3d_enabled=no
    module_multiplayer_enabled=no
    module_websocket_enabled=no
    module_enet_enabled=no
    module_webrtc_enabled=no
    module_upnp_enabled=no
    module_jsonrpc_enabled=no
    module_astcenc_enabled=no
    module_basis_universal_enabled=no
    module_betsy_enabled=no
    module_bcdec_enabled=no
    module_cvtt_enabled=no
    module_dds_enabled=no
    module_etcpak_enabled=no
    module_ktx_enabled=no
    module_msdfgen_enabled=no
    module_text_server_adv_enabled=no
    module_noise_enabled=no
    module_texture_streaming_enabled=no
    module_objectdb_profiler_enabled=no
    module_lightmapper_rd_enabled=no
)
string(JOIN " " SCONS_ARGS_STR ${SCONS_ARGS})

# ---- optionally regenerate compile_commands.json during configure -----------
# (so CLion's CMake mode can still index engine sources).
# This runs scons with compiledb=yes; the gen_only path returns quickly.
option(GODOT_GEN_COMPILE_DB "Run scons compiledb=yes during CMake configure" OFF)
if(GODOT_GEN_COMPILE_DB)
    message(STATUS "Generating compile_commands.json via scons ...")
    execute_process(
        COMMAND ${PYTHON} -m SCons ${SCONS_ARGS} compiledb=yes
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        RESULT_VARIABLE _db_res
    )
    if(NOT _db_res EQUAL 0)
        message(WARNING "scons compiledb step returned ${_db_res} (non-fatal)")
    endif()
endif()

# ---- build the Godot engine via SCons (ExternalProject) ---------------------
include(ExternalProject)
ExternalProject_Add(godot_engine
    SOURCE_DIR        ${CMAKE_SOURCE_DIR}
    CONFIGURE_COMMAND ""
    BUILD_COMMAND     ${PYTHON} -m SCons ${SCONS_ARGS_STR} -j$ENV{NUMBER_OF_PROCESSORS}
    BUILD_IN_SOURCE   1
    INSTALL_COMMAND   ""
    BUILD_ALWAYS      1   # always let scons decide what to rebuild (incremental)
    BUILD_BYPRODUCTS  ${CMAKE_SOURCE_DIR}/bin/godot.windows.editor.dev.x86_64.exe
)

# ---- YOUR manhua / film-scene code ------------------------------------------
# This is the part you edit with full CMake support in CLion.
# Start empty; add targets here as you develop (GDExtension modules, tools...).
# if(EXISTS "${CMAKE_SOURCE_DIR}/manhua/CMakeLists.txt")
#     add_subdirectory(manhua)
# endif()
# (subdirectory left commented until you scaffold manhua/ — see notes)
