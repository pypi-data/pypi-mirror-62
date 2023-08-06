# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(eigen-download NONE)

include(ExternalProject)
ExternalProject_Add(eigen-download
                    GIT_CONFIG advice.detachedHead=false;URL;http://bitbucket.org/eigen/eigen/get/3.3.4.tar.bz2;URL_MD5;a7aab9f758249b86c93221ad417fbe18
                    SOURCE_DIR          "/Users/yijiangh/conmech/cmake/../ext/eigen"
                    BINARY_DIR          "/Users/yijiangh/conmech/build/temp.macosx-10.14-x86_64-3.7/eigen-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
