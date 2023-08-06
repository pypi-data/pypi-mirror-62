# Install script for directory: /home/axel/src/openPMD/openPMD-api

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/openpmd-api-develop-kcvzyxkqbmehfearcud63oyndo5yuj2c")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so"
         RPATH "/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/openpmd-api-develop-kcvzyxkqbmehfearcud63oyndo5yuj2c/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/openpmd-api-develop-kcvzyxkqbmehfearcud63oyndo5yuj2c/lib64:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/adios2-2.5.0-krrdvxaatbxcuhqeutdo2seaoe5ajvvb/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/bzip2-1.0.8-y3jwkzygasvmix7wsxsp7ughqon54dl5/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/c-blosc-1.17.0-f4jbzijnhau35fm4mrn56na57l63jrpc/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/lz4-1.9.2-vqbilgdxfniyiv7cswfrknzl7dshtx52/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/snappy-1.1.7-5x42xljcqpiwvzeypj6klniln2uo3kwe/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zlib-1.2.11-ozk7pekyb4npkjc2pa55hvbfmcxzuema/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zstd-1.4.3-6zkigze5kbwwo7khy7thxaar642udjkx/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libfabric-1.9.0-gydwo2ddeb65bxodpq6c5pakcxv5tzhi/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libffi-3.2.1-fm4z2ulfmjmxlfqwmotpf646pvzut7qq/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libpng-1.6.37-zpkeum5rxceppa5omibbobz6wtb7s4pq/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libzmq-4.3.2-zzkxgcbtg25di5kaqikh3q5env5t3mib/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libsodium-1.0.17-ksiujegl76j45tlhft5actddffcrz4y6/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/mpich-3.3.2-4vz4pkhd2hcc3dotaikfwaqzesljpzoy/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libpciaccess-0.13.5-gmb2nwcyb5j7gyw4ph4xb6aqjc562xdf/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libxml2-2.9.9-zqxdbvfwwbfyuv7oylwcsirydmipkypb/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libiconv-1.16-awoeb3awni3jad2oxtkl7w5lx73hkjij/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/xz-5.2.4-u3w5ejhk6xsjy5vpqav65jq4hj2zwyw5/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/sz-2.0.2.0-v63asfwuidph2yqr54vwitq6z7oror5a/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zfp-0.5.5-ynskv2ml6honh7uowtslmhvtxk6qltwc/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/hdf5-1.10.6-b3smtj2cyacwd5kcjs6ijwsqlmrrw66r/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/mpark-variant-1.4.0-7cfm6dqfyhruvbbv5estxssor6l37m5c/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/nlohmann-json-3.7.2-3g6qrjgspo45ryznfhj4ry2p6sf4xrmt/lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/axel/src/openPMD/openPMD-api/spack-build/lib/libopenPMD.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so"
         OLD_RPATH "/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/hdf5-1.10.6-b3smtj2cyacwd5kcjs6ijwsqlmrrw66r/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zlib-1.2.11-ozk7pekyb4npkjc2pa55hvbfmcxzuema/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/adios2-2.5.0-krrdvxaatbxcuhqeutdo2seaoe5ajvvb/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/mpich-3.3.2-4vz4pkhd2hcc3dotaikfwaqzesljpzoy/lib::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
         NEW_RPATH "/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/openpmd-api-develop-kcvzyxkqbmehfearcud63oyndo5yuj2c/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/openpmd-api-develop-kcvzyxkqbmehfearcud63oyndo5yuj2c/lib64:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/adios2-2.5.0-krrdvxaatbxcuhqeutdo2seaoe5ajvvb/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/bzip2-1.0.8-y3jwkzygasvmix7wsxsp7ughqon54dl5/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/c-blosc-1.17.0-f4jbzijnhau35fm4mrn56na57l63jrpc/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/lz4-1.9.2-vqbilgdxfniyiv7cswfrknzl7dshtx52/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/snappy-1.1.7-5x42xljcqpiwvzeypj6klniln2uo3kwe/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zlib-1.2.11-ozk7pekyb4npkjc2pa55hvbfmcxzuema/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zstd-1.4.3-6zkigze5kbwwo7khy7thxaar642udjkx/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libfabric-1.9.0-gydwo2ddeb65bxodpq6c5pakcxv5tzhi/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libffi-3.2.1-fm4z2ulfmjmxlfqwmotpf646pvzut7qq/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libpng-1.6.37-zpkeum5rxceppa5omibbobz6wtb7s4pq/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libzmq-4.3.2-zzkxgcbtg25di5kaqikh3q5env5t3mib/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libsodium-1.0.17-ksiujegl76j45tlhft5actddffcrz4y6/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/mpich-3.3.2-4vz4pkhd2hcc3dotaikfwaqzesljpzoy/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libpciaccess-0.13.5-gmb2nwcyb5j7gyw4ph4xb6aqjc562xdf/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libxml2-2.9.9-zqxdbvfwwbfyuv7oylwcsirydmipkypb/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/libiconv-1.16-awoeb3awni3jad2oxtkl7w5lx73hkjij/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/xz-5.2.4-u3w5ejhk6xsjy5vpqav65jq4hj2zwyw5/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/sz-2.0.2.0-v63asfwuidph2yqr54vwitq6z7oror5a/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/zfp-0.5.5-ynskv2ml6honh7uowtslmhvtxk6qltwc/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/hdf5-1.10.6-b3smtj2cyacwd5kcjs6ijwsqlmrrw66r/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/mpark-variant-1.4.0-7cfm6dqfyhruvbbv5estxssor6l37m5c/lib:/home/axel/src/spack/opt/spack/linux-ubuntu18.04-skylake/gcc-8.3.0/nlohmann-json-3.7.2-3g6qrjgspo45ryznfhj4ry2p6sf4xrmt/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenPMD.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/axel/src/openPMD/openPMD-api/include/openPMD" FILES_MATCHING REGEX "/[^/]*\\.hpp$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/openPMD" TYPE FILE FILES "/home/axel/src/openPMD/openPMD-api/spack-build/include/openPMD/config.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD/openPMDTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD/openPMDTargets.cmake"
         "/home/axel/src/openPMD/openPMD-api/spack-build/CMakeFiles/Export/lib/cmake/openPMD/openPMDTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD/openPMDTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD/openPMDTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD" TYPE FILE FILES "/home/axel/src/openPMD/openPMD-api/spack-build/CMakeFiles/Export/lib/cmake/openPMD/openPMDTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD" TYPE FILE FILES "/home/axel/src/openPMD/openPMD-api/spack-build/CMakeFiles/Export/lib/cmake/openPMD/openPMDTargets-relwithdebinfo.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD" TYPE FILE FILES
    "/home/axel/src/openPMD/openPMD-api/spack-build/openPMDConfig.cmake"
    "/home/axel/src/openPMD/openPMD-api/spack-build/openPMDConfigVersion.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/openPMD/Modules" TYPE FILE FILES "/home/axel/src/openPMD/openPMD-api/share/openPMD/cmake/FindADIOS.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/axel/src/openPMD/openPMD-api/spack-build/openPMD.pc")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/axel/src/openPMD/openPMD-api/spack-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
