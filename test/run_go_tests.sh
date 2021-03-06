#!/bin/bash
#  ----------------------------------------------------------------
#

function print_msg {
    echo -e "${MSG_COLOR}*** $(date): run_go_tests.sh: $* ${NOCOLOR}"
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

function reset_yang_repository {
    if [[ ! -d $HOME/.ydk/127.0.0.1 ]]; then
      mkdir -p $HOME/.ydk
      mkdir -p $HOME/.ydk/127.0.0.1
    fi
    rm -f $HOME/.ydk/127.0.0.1/*

    # Correct issue with confd 7.3
    if [[ $confd_version > 7.2 ]]; then
      cp ${YDKGEN_HOME}/sdk/cpp/core/tests/models/ietf-interfaces.yang $HOME/.ydk/127.0.0.1/
    fi
}

# ------------------------------------------------------------------
# Golang specific functions
#------------------------------------------------------------------

function init_go_env {
    print_msg "Initializing Go environment"

    if [ -z $GOPATH ]; then
       export GOPATH="${HOME}/go"
    fi
    if [ -z $GOROOT ]; then
      export GOROOT="/usr/local/go"
    fi

    print_msg "GOPATH = ${GOPATH}"
    print_msg "GOROOT = ${GOROOT}"

    export PATH=$PATH:$GOPATH/bin
    export PATH=$PATH:$GOROOT/bin

    cd $YDKGEN_HOME

    export CXX=/usr/bin/c++
    export CC=/usr/bin/cc

    print_msg "CC: ${CC}"
    print_msg "CXX: ${CXX}"

    if [ ! -d $GOPATH/src/github.com/stretchr/testify ]; then
      print_msg "Installing 'testify' package"
      run_cmd go get github.com/stretchr/testify
      cd $GOPATH/src/github.com/stretchr/testify
      git checkout tags/v1.6.1
      cd -
    fi

    export CGO_ENABLED=1
    export CGO_LDFLAGS_ALLOW="-fprofile-arcs|-ftest-coverage|--coverage"
}

function install_go_core {
    print_msg "Installing Go core"
    cd $YDKGEN_HOME

    mkdir -p $GOPATH/src/github.com/CiscoDevNet/ydk-go/ydk
    cp -r sdk/go/core/ydk/* $GOPATH/src/github.com/CiscoDevNet/ydk-go/ydk/

    run_cmd ./generate.py --bundle profiles/test/ydktest-cpp.json --go -i
}

function install_go_bundle {
    print_msg "Generating/installing go bundle tests"
    cd $YDKGEN_HOME
    run_cmd ./generate.py --bundle profiles/test/ydktest-cpp.json --go -i
}

function run_go_bundle_tests {
    run_cmd $script_dir/init_test_env.sh
    confd_version=$($HOME/confd/bin/confd --version)

    reset_yang_repository

    run_go_samples
    run_go_sanity_tests
}

function run_go_sanity_tests {
    print_msg "Running go sanity tests"
    cd $YDKGEN_HOME/sdk/go/core/tests
    run_cmd go test
    cd - > /dev/null
}

function run_go_samples {
    print_msg "Running Go samples"

    cd $YDKGEN_HOME/sdk/go/core/samples
    run_cmd go run cgo_path/cgo_path.go
    run_cmd go run bgp_create/bgp_create.go -device ssh://admin:admin@localhost:12022
    run_cmd go run bgp_read/bgp_read.go -device ssh://admin:admin@localhost:12022
    run_cmd go run bgp_delete/bgp_delete.go -device ssh://admin:admin@localhost:12022 -v
    cd -
}

#-----------------------------------------------------------------------------
#  gNMI Tests
#-----------------------------------------------------------------------------

function init_gnmi_server {
    print_msg "Starting YDK gNMI server"
    mkdir -p $YDKGEN_HOME/test/gnmi_server/build && cd $YDKGEN_HOME/test/gnmi_server/build
    cmake .. && make clean && make
    ./gnmi_server &
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Could not start gNMI server"
        exit $status
    fi
    cd -
}

function stop_gnmi_server {
    print_msg "Stopping gNMI server"
    pkill -f gnmi_server
}

function install_go_gnmi {
    print_msg "Installing Go gNMI package"
    cd $YDKGEN_HOME

    run_cmd python ./generate.py --service profiles/services/gnmi-0.4.0.json --go -i
}

function run_go_gnmi_tests {
    init_gnmi_server

    print_msg "Running Go gNMI tests"

    cd $YDKGEN_HOME/sdk/go/gnmi/tests
    #run_cmd go test
    run_cmd go test -run GnmiServiceProviderTestSuite
    run_cmd go test -run TestGnmiServiceTestSuite
    run_cmd go test -run TestGnmiSessionTestSuite

    run_go_gnmi_samples

    stop_gnmi_server

    cd $YDKGEN_HOME
}

function run_go_gnmi_samples {
    print_msg "Running Go gNMI samples"

    cd $YDKGEN_HOME/sdk/go/gnmi/samples
    run_cmd go run service_subscribe_poll.go < $YDKGEN_HOME/test/gnmi_subscribe_poll_input.txt
    run_cmd go run session_subscribe_poll.go < $YDKGEN_HOME/test/gnmi_subscribe_poll_input.txt
}

########################## EXECUTION STARTS HERE #############################

# Terminal colors
RED='\033[0;31m'
GREEN='\033[1;32m'
NOCOLOR='\033[0m'
YELLOW='\033[1;33m'
MSG_COLOR=$YELLOW

os_type=$(uname)
if [[ ${os_type} == "Linux" ]] ; then
    os_info=$(cat /etc/*-release)
else
    os_info=$(sw_vers)
fi
print_msg "Running OS type: $os_type"
print_msg "OS info: $os_info"

script_dir=$(cd $(dirname ${BASH_SOURCE}) && pwd)
if [ -z ${YDKGEN_HOME} ] || [ ! -d ${YDKGEN_HOME} ]; then
    export YDKGEN_HOME=$(cd $script_dir/.. && pwd)
    print_msg "YDKGEN_HOME is set to ${YDKGEN_HOME}"
fi

if [[ $(uname) == "Linux" && ${os_info} == *"fedora"* ]]; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/grpc/libs/opt:$HOME/protobuf-3.5.0/src/.libs:/usr/local/lib:/usr/local/lib64:/usr/lib64
    print_msg "LD_LIBRARY_PATH is set to: $LD_LIBRARY_PATH"
    centos_version=$(echo `lsb_release -r` | awk '{ print $2 }' | cut -d '.' -f 1)
fi

curr_dir="$(pwd)"
script_dir=$(cd $(dirname ${BASH_SOURCE}) && pwd)

cd $YDKGEN_HOME

if [[ -z ${PYTHON_VENV} ]]; then
    export PYTHON_VENV=${HOME}/venv
    print_msg "Python virtual environment location is set to ${PYTHON_VENV}"
fi
source $PYTHON_VENV/bin/activate

init_go_env
install_go_core
install_go_bundle

run_go_bundle_tests

install_go_gnmi
run_go_gnmi_tests

$script_dir/clean_test_env.sh

cd $curr_dir
