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
# Bash script to run basic YDK tests for Python
# ------------------------------------------------------------------------

function print_msg {
    echo -e "\n${MSG_COLOR}*** $(date): python_bundle_tests.sh: $* ${NOCOLOR}"
}

function run_test {
    test=$*
    print_msg "Running test $test"
    python3 $YDKGEN_HOME/sdk/python/core/tests/$test
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Command 'python $YDKGEN_HOME/sdk/python/core/tests/$test' FAILED with status=$status"
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
    confd_version=$($HOME/confd/bin/confd --version)
    if [[ $confd_version. > 7.2. ]]; then
      cp ${YDKGEN_HOME}/sdk/cpp/core/tests/models/ietf-interfaces.yang $HOME/.ydk/127.0.0.1/
    fi
}

########################## EXECUTION STARTS HERE #############################
#

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

reset_yang_repository

print_msg "Installing test bundles"
cd $YDKGEN_HOME
python3 generate.py --python --bundle profiles/test/ydktest-cpp.json -i
cd -

$script_dir/init_test_env.sh

run_test test_ydk_types.py
run_test test_sanity_codec.py
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
