#   This file is part of the dbus-cxx library.
#
#   The dbus-cxx library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   version 3 as published by the Free Software Foundation.
#
#   The dbus-cxx library is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this software. If not see <http://www.gnu.org/licenses/>.

pkg_check_modules( expat REQUIRED IMPORTED_TARGET expat )

set( TEST_INCLUDES ${cppgenerate_INCLUDE_DIRS} )
set( TEST_LINK dbus-cxx dbus-cxx-uv PkgConfig::libuv PkgConfig::sigc PkgConfig::expat ${LIBRT} )

link_directories( ${CMAKE_BINARY_DIR} )

include_directories(
    ${CMAKE_BINARY_DIR}/dbus-cxx
    ${CMAKE_SOURCE_DIR}/dbus-cxx-uv )

add_executable( test-uv-dispatcher test-uv-dispatcher.cpp calleeclass.cpp )
target_link_libraries( test-uv-dispatcher ${TEST_LINK} )
target_include_directories( test-uv-dispatcher PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-uv-dispatcher PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-uv-dispatcher PROPERTY CXX_STANDARD 17 )

add_executable( uv-caller uv-caller.cpp )
target_link_libraries( uv-caller ${TEST_LINK} )
target_include_directories( uv-caller PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( uv-caller PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET uv-caller PROPERTY CXX_STANDARD 17 )

if( WIN32 )
  set( TEST_SCRIPT dbus-wrapper-uv-tests.bat )
else( WIN32 )
  set( TEST_SCRIPT dbus-wrapper-uv-tests.sh )
endif( WIN32 )

configure_file( ${TEST_SCRIPT} ${TEST_SCRIPT} COPYONLY )

add_test( NAME uv-dispatcher COMMAND ${TEST_SCRIPT} uv-dispatcher)

if( WIN32 )
  set( PATH_MODIFICATION
        "PATH=path_list_append:$<SHELL_PATH:${libuv_BINDIR}>"
	"PATH=path_list_append:$<SHELL_PATH:$<TARGET_FILE_DIR:dbus-cxx>>"
        "PATH=path_list_append:$<SHELL_PATH:$<TARGET_FILE_DIR:dbus-cxx-uv>>"
        "PATH=path_list_append:$<SHELL_PATH:$<TARGET_FILE_DIR:uv-caller>>" )
  set_tests_properties( uv-dispatcher PROPERTIES ENVIRONMENT_MODIFICATION "${PATH_MODIFICATION}" )
endif( WIN32 )
