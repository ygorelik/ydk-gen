#!/bin/bash
#  ----------------------------------------------------------------

function print_msg {
    echo -e "\n${MSG_COLOR}*** $(date): clean_builds.sh: $1${NOCOLOR}"
}

# Terminal colors
RED='\033[0;31m'
GREEN='\033[1;32m'
NOCOLOR='\033[0m'
YELLOW='\033[1;33m'
MSG_COLOR=$YELLOW

if [ -z ${YDKGEN_HOME} ] || [ ! -d ${YDKGEN_HOME} ]; then
    YDKGEN_HOME=$(pwd)
    print_msg "YDKGEN_HOME is set to ${YDKGEN_HOME}"
fi

script_dir=$(cd $(dirname ${BASH_SOURCE}) && pwd)

$script_dir/clean_test_env.sh

print_msg "Deleting all './build/*' content"
rm -rf $YDKGEN_HOME/sdk/cpp/tests/build/*
rm -rf $YDKGEN_HOME/sdk/cpp/core/build/*
rm -rf $YDKGEN_HOME/sdk/cpp/gnmi/tests/build/*
rm -rf $YDKGEN_HOME/sdk/cpp/gnmi/samples/build/*
rm -rf $YDKGEN_HOME/sdk/cpp/gnmi/build/*
rm -rf $YDKGEN_HOME/gen-api/cpp/ydk/build/*
rm -rf $YDKGEN_HOME/gen-api/cpp/ydktest-bundle/build/*
rm -rf $YDKGEN_HOME/scripts/community/cpp/build/*
rm -rf $YDKGEN_HOME/scripts/community/Debug/cpp/build/*
rm -rf $YDKGEN_HOME/test/gnmi_server/build/*

rm -f coverage.txt coverage.info

rm -rf $YDKGEN_HOME/gen-api/* $YDKGEN_HOME/gen-api/.cache

rm -rf $YDKGEN_HOME/sdk/python/core/dist
