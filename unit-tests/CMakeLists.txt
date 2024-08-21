
set( TEST_INCLUDES ${cppgenerate_INCLUDE_DIRS} )
set( TEST_LINK dbus-cxx PkgConfig::sigc PkgConfig::expat ${LIBRT} )

link_directories( ${CMAKE_BINARY_DIR} )

include_directories( ${CMAKE_SOURCE_DIR}/dbus-cxx ${CMAKE_BINARY_DIR}/dbus-cxx )

if( WIN32 )
  add_compile_definitions( DBUS_DLL_IMPORT )
  include_directories( ${CMAKE_SOURCE_DIR}/compat )
endif( WIN32 )

function( set_common_test_properties test_name )
  if( WIN32 )
    set( PATH_MODIFICATION
      "PATH=path_list_append:$<SHELL_PATH:$<TARGET_FILE_DIR:dbus-cxx>>"
      "PATH=path_list_append:$<SHELL_PATH:$<TARGET_FILE_DIR:test-callmessage>>" )
    set_tests_properties( ${test_name} PROPERTIES ENVIRONMENT_MODIFICATION "${PATH_MODIFICATION}" )
  endif( WIN32 )
endfunction( set_common_test_properties )

foreach( script IN ITEMS
    dbus-wrapper
    dbus-wrapper-data-tests
    dbus-wrapper-introspection-tests
    dbus-wrapper-customaddress
    dbus-wrapper-fd-tests
    dbus-wrapper-recursive
    dbus-wrapper-recursive-signal
    dbus-wrapper-property-tests )
  if( WIN32 )
    set( ${script} ${script}.bat )
    configure_file( ${script}.bat ${script}.bat COPYONLY )
  else( WIN32 )
    set( ${script} ${script}.sh )
    configure_file( ${script}.sh ${script}.sh COPYONLY )
  endif( WIN32 )
endforeach() 

if( WIN32 )
  set( dbus-wrapper-affinity dbus-run-session )
else( WIN32 )
  set( dbus-wrapper-affinity )
endif( WIN32 )

if( ENABLE_ROBUSTNESS_TESTS )
    add_subdirectory( robustness-tests )
endif( ENABLE_ROBUSTNESS_TESTS )

add_executable( test-callmessage callmessagetests.cpp )
target_link_libraries( test-callmessage ${TEST_LINK} )
target_include_directories( test-callmessage PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-callmessage PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-callmessage PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS bool byte int16 uint16 int32 uint32 int64 uint64 double cstring string array_double multiple )
  add_test( NAME Callmessage-${type} COMMAND test-callmessage ${type})
  set_common_test_properties( Callmessage-${type} )
endforeach()

add_executable( test-messageiterator messageiteratortests.cpp )
target_link_libraries( test-messageiterator ${TEST_LINK} )
target_include_directories( test-messageiterator PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-messageiterator PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-messageiterator PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    bool byte int16 uint16 int32 uint32 int64 uint64 double cstring string signature
    array_int array_string array_array_string filedescriptor multiple struct
    variant variant_vector variant_map variant_struct
    map_string_variant map_string_variant_many map_string_string map_string_string_many correct_variant_signature
    array_array_bytes array_array_int
    complex_variants complex_variants2 complex_variants3 nested_map variant_deep )
  add_test( NAME messageiterator-${type} COMMAND test-messageiterator ${type} )
  set_common_test_properties( messageiterator-${type} )
endforeach()

foreach( type IN ITEMS
    bool byte int16 uint16 int32 uint32 int64 uint64 double cstring string
    signature array_int array_string filedescriptor multiple struct variant )
  add_test( NAME messageiterator-${type}-2 COMMAND test-messageiterator ${type}-2 )
  set_common_test_properties( messageiterator-${type}-2 )
endforeach()

add_executable( test-path pathclasstests.cpp )
target_link_libraries( test-path ${TEST_LINK} )
target_include_directories( test-path PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-path PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-path PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    valid invalid-characters invalid-trailing-slash invalid-empty-path invalid-double-slash invalid-missing-leading-slash
    decompose-valid decompose-root decompose-invalid decompose-empty
    append-valid append-valid-multiple append-valid-leading-slash append-valid-trailing-slash
    append-invalid-empty append-invalid-chars append-invalid-double-slash append-invalid-root )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME path-${type} COMMAND test-path ${type_} )
  set_common_test_properties( path-${type} )
endforeach()

add_executable( test-connection connectiontests.cpp )
target_link_libraries( test-connection ${TEST_LINK} )
target_include_directories( test-connection PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-connection PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-connection PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    create-signal-proxy get-signal-proxy-by-iface get-signal-proxy-by-iface-and-name
    create-void-signal create-int-signal remove-object-proxy )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME connection-${type} COMMAND ${dbus-wrapper} test-connection ${type_} )
  set_common_test_properties( connection-${type} )
endforeach()

#
# Object Tests
#
add_executable( object-tests objecttests.cpp )
target_link_libraries( object-tests ${TEST_LINK} )
target_include_directories( object-tests PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( object-tests PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET object-tests PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    proxy-create proxy-create-method1 export-method )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME object-${type} COMMAND ${dbus-wrapper} object-tests ${type_} )
  set_common_test_properties( object-${type} )
endforeach()

#
# Data Sending tests - make sure we can actually send data across the bus correctly
#
add_executable( data-tests datatests.cpp custom-type.cpp )
target_link_libraries( data-tests ${TEST_LINK} )
target_include_directories( data-tests PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( data-tests PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET data-tests PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    send-integers void-method void-custom send-intcustom ping machine-uuid tuple
    variant-array variant-map variant-tuple nonexistant-method
    send-multiplereturn send-multiplereturn2 send-complex error-return )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME data-${type} COMMAND ${dbus-wrapper-data-tests} ${type_} )
  set_common_test_properties( data-${type} )
endforeach()

#
# Signal tests - make sure we can tx and rx singals correctly
#
add_executable( signal-tests signaltests.cpp )
target_link_libraries( signal-tests ${TEST_LINK} )
target_include_directories( signal-tests PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( signal-tests PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET signal-tests PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    create tx-rx void-txrx path-match-only interface-match-only member-match-only multiple-handlers remove-handler )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME signal-${type} COMMAND ${dbus-wrapper} signal-tests ${type_} )
  set_common_test_properties( signal-${type} )
endforeach()

#
# Introspection Tests - make sure that we can introspect and get the correct data back
#
add_executable( introspection-tests introspection-test.cpp )
target_link_libraries( introspection-tests ${TEST_LINK} PkgConfig::expat )
target_include_directories( introspection-tests PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( introspection-tests PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET introspection-tests PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    basic-introspect valid-xml validate-interfaces add-method-under-foowhat
    first-argname-correct second-argname-correct signal-found multiple-return )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME introspection-${type} COMMAND ${dbus-wrapper-introspection-tests} ${type_} )
  set_common_test_properties( introspection-${type} )
endforeach()

#
# Custom DBus address test - make sure that we can connect to an arbitary bus, not just the default session bus
#
add_executable( customaddress-tests customaddress-test.cpp )
target_link_libraries( customaddress-tests ${TEST_LINK} )
target_include_directories( customaddress-tests PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( customaddress-tests PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET customaddress-tests PROPERTY CXX_STANDARD 17 )

add_test( NAME custom-address COMMAND ${dbus-wrapper-customaddress} customaddress-tests)
set_common_test_properties( custom-address )

#
# Signature tests - make sure that given a signature, we can validate it and iterate over it
#
add_executable( test-signature signaturetests.cpp )
target_link_libraries( test-signature ${TEST_LINK} )
target_include_directories( test-signature PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-signature PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-signature PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    create iterate-arrayint iterate-arrayint2 iterate-nested-array iterate-multiple-types iterate-dictionary
    iterate-struct iterate-nested-with-more-data iterate-dict-and-data iterate-struct-and-data
    unbalanced-struct single-bool create-from-struct-in-array single-type1 single-type2 )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME signature-${type} COMMAND test-signature ${type_} )
  set_common_test_properties( signature-${type} )
endforeach()

#
# Validation tests - make sure that our validation routines work correctly
#
add_executable( test-validation validationtests.cpp )
target_link_libraries( test-validation ${TEST_LINK} )
target_include_directories( test-validation PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-validation PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-validation PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    one_section_bus_name two_section_bus_name three_section_bus_name )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME validation-${type} COMMAND test-validation ${type_} )
  set_common_test_properties( validation-${type} )
endforeach()

#
# Thread affinity tests - make sure that when we define what thread we want to be
#  called from, it calls it from the correct thread
#
add_executable( test-affinity affinity-tests.cpp )
target_link_libraries( test-affinity ${TEST_LINK} )
target_include_directories( test-affinity PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-affinity PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-affinity PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    signal-dispatcher-thread signal-main-thread message-dispatcher-thread message-main-thread message-change-thread )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME affinity-${type} COMMAND ${dbus-wrapper-affinity} test-affinity ${type_} )
  set_common_test_properties( affinity-${type} )
endforeach()

#
# File Descriptor tests - make sure that we can send and receive file descriptors correctly
#
add_executable( test-filedescriptor filedescriptor-tests.cpp )
target_link_libraries( test-filedescriptor ${TEST_LINK} )
target_include_directories( test-filedescriptor PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-filedescriptor PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-filedescriptor PROPERTY CXX_STANDARD 17 )

if( NOT WIN32 )
  add_test( NAME filedescriptor-send COMMAND dbus-wrapper-fd-tests.sh send)
  add_test( NAME filedescriptor-receive COMMAND dbus-wrapper-fd-tests.sh get)
endif( NOT WIN32 )

#
# Recursive tests - make sure that calling another DBus method inside of a current DBus method doesn't lockup
#
add_executable( test-recursive recursive-test.cpp )
target_link_libraries( test-recursive ${TEST_LINK} )
target_include_directories( test-recursive PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-recursive PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-recursive PROPERTY CXX_STANDARD 17 )

add_test( NAME recursive-method-call COMMAND ${dbus-wrapper-recursive} test)
set_common_test_properties( recursive-method-call )

add_executable( test-recursive-signal recursive-signal-test.cpp )
target_link_libraries( test-recursive-signal ${TEST_LINK} )
target_include_directories( test-recursive-signal PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-recursive-signal PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-recursive-signal PROPERTY CXX_STANDARD 17 )

add_test( NAME recursive-from-signal COMMAND ${dbus-wrapper-recursive-signal} test)
set_common_test_properties( recursive-from-signal )

#
# Ensure that unset environment variables don't cause problems
#
add_executable( test-unset-envvars unset-envvars.cpp )
target_link_libraries( test-unset-envvars ${TEST_LINK} )
target_include_directories( test-unset-envvars PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-unset-envvars PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-unset-envvars PROPERTY CXX_STANDARD 17 )

add_test( NAME unset-session-bus COMMAND test-unset-envvars connect_session_bus )
add_test( NAME unset-starter-bus COMMAND test-unset-envvars connect_starter_bus )

#
# Property tests - test that we can get/set properties, as well as getting signals
#
add_executable( test-property property-test.cpp )
target_link_libraries( test-property ${TEST_LINK} )
target_include_directories( test-property PUBLIC ${CMAKE_SOURCE_DIR} )
target_include_directories( test-property PUBLIC ${CMAKE_CURRENT_BINARY_DIR} )
set_property( TARGET test-property PROPERTY CXX_STANDARD 17 )

foreach( type IN ITEMS
    get-all get-valid set-valid set-invalid set-readonly signal-emitted )
  string( REPLACE "-" "_" type_ "${type}" )
  add_test( NAME property-${type} COMMAND ${dbus-wrapper-property-tests} ${type_} )
  set_common_test_properties( property-${type} )
endforeach()
