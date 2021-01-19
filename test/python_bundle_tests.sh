#!/bin/bash

function print_msg {
    echo -e "\n${MSG_COLOR}*** $(date): python_bundle_tests.sh: $1${NOCOLOR}"
}

function run_test {
    test=$@
    print_msg "Running test $test"
    python $YDKGEN_HOME/sdk/python/core/tests/$test
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Command 'python $YDKGEN_HOME/sdk/python/core/tests/$test' FAILED with status=$status"
        exit $status
    fi
    return $status
}

########################## EXECUTION STARTS HERE #############################
#

# Terminal colors
RED='\033[0;31m'
GREEN='\033[1;32m'
NOCOLOR='\033[0m'
YELLOW='\033[1;33m'
MSG_COLOR=$YELLOW

if [ -z ${YDKGEN_HOME} ] || [ ! -d ${YDKGEN_HOME} ]; then
    export YDKGEN_HOME=$(pwd)
    print_msg "YDKGEN_HOME is set to ${YDKGEN_HOME}"
fi

script_dir=$(cd $(dirname ${BASH_SOURCE}) && pwd)
$script_dir/init_test_env.sh

source ${HOME}/venv/bin/activate

run_test test_ydk_types.py
run_test test_netconf_operations.py
run_test test_opendaylight.py
run_test test_restconf_provider.py
run_test test_sanity_delete.py
run_test test_sanity_errors.py
run_test test_sanity_filter_read.py
run_test test_sanity_filters.py
run_test test_sanity_levels.py
run_test test_sanity_netconf.py
run_test test_sanity_path.py
run_test test_netconf_provider.py
run_test test_sanity_service_errors.py
run_test test_sanity_type_mismatch_errors.py
run_test test_sanity_types.py
run_test test_non_top_operations.py

$script_dir/clean_test_env.sh
