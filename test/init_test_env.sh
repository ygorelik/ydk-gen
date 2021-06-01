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
# Bash script to initialize and run dumb services for unit tests
#
# ------------------------------------------------------------------------

function print_msg {
    echo -e "\n${MSG_COLOR}*** $(date): init_test_env.sh: $*${NOCOLOR}"
}

function run_cmd {
    $*
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Command '$*' FAILED with status=$status"
        exit $status
    fi
    return $status
}

function init_confd {
    cd $1
    print_msg "Initializing confd in $(pwd)"
    confd_rc=$(find $HOME/confd -name confdrc)
    if [[ -z $confd_rc ]]; then
        MSG_COLOR=$RED
        print_msg "Cannot find 'confdrc' resource file in user file system. Exiting"
        exit 1
    fi
    print_msg "Found confd resource file: $confd_rc"
    run_cmd source $confd_rc
    run_cmd make stop > /dev/null
    run_cmd make clean > /dev/null
    run_cmd make all > /dev/null
    run_cmd make start
    sleep 2
    cd - > /dev/null
}

function init_confd_ydktest {
    init_confd $YDKGEN_HOME/sdk/cpp/core/tests/confd/ydktest
}

function init_rest_server {
    print_msg "Starting REST server"
    pkill -f moco-runner
    export REST_SERVER_PID=$(./test/start_rest_server.sh)
    print_msg "REST server started with PID $REST_SERVER_PID"
}

function init_tcp_server {
    print_msg "Starting TCP server"
    pkill -f tcp_proxy_server
    export TCP_SERVER_PID=$(./test/start_tcp_server.sh)
    print_msg "TCP server started with PID: $TCP_SERVER_PID"
}

########################## EXECUTION STARTS HERE #############################

# Terminal colors
RED='\033[0;31m'
GREEN='\033[1;32m'
NOCOLOR='\033[0m'
YELLOW='\033[1;33m'
MSG_COLOR=$YELLOW

os_type=$(uname)
print_msg "Running OS type: $os_type"

script_dir=$(cd $(dirname ${BASH_SOURCE}) > /dev/null && pwd)

if [ -z ${YDKGEN_HOME} ] || [ ! -d ${YDKGEN_HOME} ]; then
  YDKGEN_HOME=$(cd "$script_dir/../" > /dev/null && pwd)
  print_msg "YDKGEN_HOME is set to ${YDKGEN_HOME}"
fi

print_msg "Python location: $(which python)"

curr_dir="$(pwd)"
cd $YDKGEN_HOME

init_confd_ydktest
init_rest_server
init_tcp_server

cd $curr_dir
exit
