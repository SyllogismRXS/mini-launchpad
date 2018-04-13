cmake_minimum_required (VERSION 3.5)

project (MiniLaunchpad)

set(PROJECT_VERSION_MAJOR "0")
set(PROJECT_VERSION_MINOR "1")
set(PROJECT_VERSION_PATCH "0")
set(PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")
set(PROJECT_VERSION_DATE "2018.03.21")

include(CMakePackageConfigHelpers)

###############################################################################
# Generate the cmake configuration files for the build tree
###############################################################################
set(SHARE_INSTALL_DIR ${CMAKE_SOURCE_DIR}/share)

configure_package_config_file(MiniLaunchpadConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/MiniLaunchpadConfig.cmake
  INSTALL_DESTINATION ${CMAKE_SOURCE_DIR}/build
  PATH_VARS SHARE_INSTALL_DIR)

write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/MiniLaunchpadConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion )

###############################################################################
# Generate the cmake configuration files for the system install tree
###############################################################################
if(NOT CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX /usr/local)
endif()

set(SHARE_INSTALL_DIR ${CMAKE_INSTALL_PREFIX}/share)

configure_package_config_file(MiniLaunchpadConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_FILES_DIRECTORY}/MiniLaunchpadConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/cmake/${PROJECT_NAME}
  PATH_VARS SHARE_INSTALL_DIR)

write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_FILES_DIRECTORY}/MiniLaunchpadConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion )

###############################################################################
# Define install targets
###############################################################################
install (DIRECTORY share/cmake
  DESTINATION share
  )

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/MiniLaunchpadConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/MiniLaunchpadConfigVersion.cmake
  DESTINATION lib/cmake/MiniLaunchpad
  )

###############################################################################
# Export the package for use from the build-tree
# (this registers the build-tree with a global CMake-registry ~/.cmake)
###############################################################################
export(PACKAGE ${PROJECT_NAME})
