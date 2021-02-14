#!/bin/bash
#  -----------------------------------------------------------------------
# Copyright 2020 Yan Gorelik, YDK Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
#
# Bash script to delete all YDK built and installed components
#
# ------------------------------------------------------------------------

function print_msg {
    echo -e "\n${MSG_COLOR}*** $(date): clean_builds.sh: $*${NOCOLOR}"
}

# Terminal colors
RED='\033[0;31m'
GREEN='\033[1;32m'
NOCOLOR='\033[0m'
YELLOW='\033[1;33m'
MSG_COLOR=$YELLOW

script_dir=$(cd $(dirname ${BASH_SOURCE}) > /dev/null && pwd)

if [ -z ${YDKGEN_HOME} ] || [ ! -d ${YDKGEN_HOME} ]; then
  YDKGEN_HOME=$(cd "$script_dir/../" > /dev/null && pwd)
  print_msg "YDKGEN_HOME is set to ${YDKGEN_HOME}"
fi

$script_dir/clean_test_env.sh

print_msg "Deleting all './build/*' content"
rm -rf $YDKGEN_HOME/sdk/cpp/tests/build
rm -rf $YDKGEN_HOME/sdk/cpp/core/build
rm -rf $YDKGEN_HOME/sdk/cpp/gnmi/tests/build
rm -rf $YDKGEN_HOME/sdk/cpp/gnmi/samples/build
rm -rf $YDKGEN_HOME/sdk/cpp/gnmi/build
rm -rf $YDKGEN_HOME/gen-api/cpp/ydk/build
rm -rf $YDKGEN_HOME/gen-api/cpp/ydktest-bundle/build
rm -rf $YDKGEN_HOME/test/gnmi_server/build

rm -f coverage.txt coverage.info

rm -rf $YDKGEN_HOME/gen-api/* $YDKGEN_HOME/gen-api/.cache

rm -rf $YDKGEN_HOME/sdk/python/core/dist

print_msg "Deleting go packages..."
if [ -z $GOPATH ]; then
    GOPATH="${HOME}/go"
fi
rm -rf $GOPATH/src/github.com/CiscoDevNet/ydk-go

print_msg "Deleting python packages..."
if [[ -z ${PYTHON_VENV} ]]; then
    export PYTHON_VENV=${HOME}/venv
    print_msg "Python virtual environment location is set to ${PYTHON_VENV}"
fi
source $PYTHON_VENV/bin/activate
pip uninstall -y ydk
pip uninstall -y ydk-models-ydktest
pip uninstall -y ydk-models-augmentation
pip uninstall -y ydk-models-deviation
pip uninstall -y ydk-service-gnmi

print_msg "Deleting C++ packages..."
sudo rm -rf /usr/local/lib/libydk* /usr/local/lib/libyang
sudo rm -rf /usr/local/include/ydk /usr/local/include/libyang /usr/local/include/libnetconf
