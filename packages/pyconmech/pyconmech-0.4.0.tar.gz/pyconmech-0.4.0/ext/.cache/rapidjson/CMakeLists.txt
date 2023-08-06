# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(rapidjson-download NONE)

include(ExternalProject)
ExternalProject_Add(rapidjson-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/Tencent/rapidjson.git;GIT_TAG;b16cec1a1aff158f5002250139528cf8a4b413d8
                    SOURCE_DIR          "C:/Users/yijiangh/Documents/pb_ws/conmech/cmake/../ext/rapidjson"
                    BINARY_DIR          "C:/Users/yijiangh/Documents/pb_ws/conmech/build/rapidjson-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
