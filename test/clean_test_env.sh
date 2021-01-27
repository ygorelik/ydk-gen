#!/bin/bash
#  ----------------------------------------------------------------
#

function print_msg {
    echo -e "\n${MSG_COLOR}*** $(date): clean_test_env.sh: $1${NOCOLOR}"
}

function run_cmd {
    $@
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Command '$@' FAILED with status=$status"
        exit $status
    fi
    return $status
}

function init_confd_rc {
    confd_rc=$(find $HOME/confd -name confdrc)
    if [[ -z $confd_rc ]]; then
        MSG_COLOR=$RED
        print_msg "Cannot find confdrc resource file in user file system. Exiting"
        exit 1
    fi
    print_msg "Found confd resource file: $confd_rc"
    run_cmd source $confd_rc
}

function stop_confd {
  init_confd_rc
  stop_confd_server $YDKGEN_HOME/sdk/cpp/core/tests/confd/ydktest
  stop_confd_server $YDKGEN_HOME/sdk/cpp/core/tests/confd/deviation
  stop_confd_server $YDKGEN_HOME/sdk/cpp/core/tests/confd/augmentation
}

function stop_confd_server {
    cd $1
    print_msg "Stopping confd from $(pwd)"
    run_cmd make stop > /dev/null
    sleep 3
    run_cmd make clean
    cd - > /dev/null
}

function stop_tcp_server {
    if [[ ! -z $TCP_SERVER_PID ]]; then
        print_msg "Stopping TCP server PID $TCP_SERVER_PID"
        kill $TCP_SERVER_PID
        unset TCP_SERVER_PID
    else
        print_msg "Stopping all TCP servers"
        pkill -f tcp_proxy_server
    fi
}

function stop_rest_server {
    if [[ ! -z $REST_SERVER_PID ]]; then
        print_msg "Stopping REST server PID $REST_SERVER_PID"
        kill $REST_SERVER_PID
        unset REST_SERVER_PID
    else
        print_msg "Stopping all REST servers"
        pkill -f moco-runner
    fi
}

function stop_gnmi_server {
        print_msg "Stopping gNMI server"
        pkill -f gnmi_server
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

if [ -z ${YDKGEN_HOME} ] || [ ! -d ${YDKGEN_HOME} ]; then
    YDKGEN_HOME=$(pwd)
    print_msg "YDKGEN_HOME is set to ${YDKGEN_HOME}"
fi

curr_dir="$(pwd)"
cd $YDKGEN_HOME

stop_gnmi_server
stop_tcp_server
stop_rest_server
stop_confd

if [ -d ${HOME}/.ydk ]; then
    print_msg "Deleting YDK cache in ${HOME}/.ydk"
    rm -rf ${HOME}/.ydk/127.0.0.1/*
    rm -rf ${HOME}/.ydk/localhost/*
fi

cd $curr_dir
