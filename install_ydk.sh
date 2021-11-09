#!/bin/bash
#  -----------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------
#
# Bash script to install ydk
#
# For usage run: ./install_ydk -h
# ------------------------------------------------------------------------------

function print_msg {
    echo -e "${MSG_COLOR}*** $(date) *** install_ydk.sh | $* ${NOCOLOR}"
}

function run_cmd {
    local cmd=$*
    print_msg "Running: $cmd"
    $*
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Exiting '$*' with status=$status"
        exit $status
    fi
    return $status
}

function usage {
    MSG_COLOR=$NOCOLOR
    echo "usage: install_ydk [ {--cpp|--py|--go|--all} ] [-c] [-s gnmi] [-h] [-n] [-v] [-p path]"
    echo "Options and arguments:"
    echo "  --cpp                 install YDK for C++ programming language"
    echo "  --go                  install YDK for Go programming language"
    echo "  --py|--python         install YDK for Python programming language (default)"
    echo "  --all                 install YDK for all available programming languages"
    echo "  -v|--venv             create python virtual environment"
    echo "  -c|--core             install YDK core packages"
    echo "  -s|--service gnmi     install gNMI service package"
    echo "  -n|--no-deps          skip installation of dependencies"
    echo "  -p|--python-dir path  set Python3 installation root directory;"
    echo "                        if not specified, system installation assumed"
    echo "  -h|--help             print this help message and exit"
    echo " "
    echo "Environment variables:"
    echo "YDKGEN_HOME         specifies location of ydk-gen git repository;"
    echo "                    if not set, $HOME/ydk-gen is assumed"
    echo "PYTHON_VENV         specifies location of python virtual environment;"
    echo "                    if not set, $HOME/venv is assumed"
    echo "GOROOT              specifies installation directory of go software;"
    echo "                    if not set, /usr/local/go is assumed"
    echo "GOPATH              specifies location of golang directory;"
    echo "                    if not set, $HOME/go is assumed"
    echo "C_INCLUDE_PATH      location of C include files;"
    echo "                    if not set, /usr/local/include is assumed"
    echo "CPLUS_INCLUDE_PATH  location of C++ include files;"
    echo "                    if not set, /usr/local/include is assumed"
    echo "CMAKE_LIBRARY_PATH  Location of Python shared libraries;"
    echo "                    if not set, default system library location is assumed"
}

function activate_python_venv() {
  if [[ -z ${PYTHON_VENV} ]]; then
    PYTHON_VENV=${HOME}/venv
    print_msg "Python virtual environment location is set to ${PYTHON_VENV}"
  fi
  if [[ ! -d ${PYTHON_VENV} ]]; then
    print_msg "Creating Python3 virtual environment in ${PYTHON_VENV}"
    run_cmd $PYTHON_BIN -m venv ${PYTHON_VENV}
  fi
  run_cmd source ${PYTHON_VENV}/bin/activate
}

function check_python_installation {
  if [ ${install_venv} == "yes" ]; then
    activate_python_venv
  fi
  print_msg "Checking python3 version and installation"
  $PYTHON_BIN --version
  status=$?
  if [ $status -ne 0 ]; then
    MSG_COLOR=$RED
    print_msg "Could not locate $PYTHON_BIN interpretor"
    exit $status
  fi

  print_msg "Checking $PIP_BIN version and installation"
  $PIP_BIN --version
  status=$?
  if [ $status -ne 0 ]; then
    MSG_COLOR=$RED
    print_msg "Could not locate $PIP_BIN"
    exit $status
  fi

  if [[ $ydk_lang == "py" || $ydk_lang == "all" ]]; then
    print_msg "Checking installation of python shared libraries"
    ver=$($PYTHON_BIN -c "import sys;print('{}.{}'.format(sys.version_info.major,sys.version_info.minor))")
    if [[ $ver. > "3.8." ]]; then
      print_msg "YDK for python currently is not supported with Python version $ver"
      print_msg "Please downgrade your Python installation to 3.8 or 3.7"
      exit 1
    fi
    os_type=$(uname)
    if [[ ${os_type} == "Linux" ]]; then
      if [[ $ver. > "3.7." ]]; then
        ext="$ver.so"
      else
        ext="$ver"m.so
      fi
    elif [[ ${os_type} == "Darwin" ]]; then
      ext="$ver.dylib"
    fi
    lines=($(locate libpython$ext))
    if [[ ${#lines[@]} -gt 0 ]] && [[ -x ${lines[0]} || -L ${lines[0]} ]]; then
      if [[ -z $CMAKE_LIBRARY_PATH ]]; then
        export CMAKE_LIBRARY_PATH=$(dirname ${lines[0]})
        print_msg "Setting CMAKE_LIBRARY_PATH to $CMAKE_LIBRARY_PATH"
      fi
    else
      print_msg "Could not locate python shared library libpython$ext"
      print_msg "Try to update locate database, then repeat YDK installation"
      exit 1
    fi
  fi
}

function init_py_env {
  check_python_installation
  print_msg "Initializing Python requirements"
  $PIP_BIN install wheel==0.34.2
  status=$?
  if [ $status -ne 0 ]; then
    print_msg "Enabling sudo for Python components installation"
    sudo_cmd="sudo"
    sudo_flag="s"
  fi
  $sudo_cmd $PIP_BIN install -r requirements.txt
  $sudo_cmd $PIP_BIN install $YDKGEN_HOME/3d_party/python/pyang-2.5.0.m1.tar.gz
}

function init_go_env {
  if [[ ${ydk_lang} == "go" || ${ydk_lang} == "all" ]]; then
    print_msg "Initializing Go environment"

    if [[ $(uname) == "Darwin" ]]; then
        if [[ $GOPATH. == "." ]]; then
            export GOPATH=$HOME/go
        fi
        print_msg "GOROOT: $GOROOT"
        print_msg "GOPATH: $GOPATH"
    else
        if [[ $GOROOT. == "." ]]; then
            export GOROOT=/usr/local/go
            print_msg "Setting GOROOT to $GOROOT"
        else
            print_msg "GOROOT: $GOROOT"
        fi
        export PATH=$GOROOT/bin:$PATH

        if [[ $GOPATH. == "." ]]; then
            export GOPATH=$HOME/go
            mkdir -p $GOPATH
            print_msg "Setting GOPATH to $GOPATH"
        else
            print_msg "GOPATH: $GOPATH"
        fi
    fi
    go_version=$(echo `go version` | awk '{ print $3 }' | cut -d 'o' -f 2)
    print_msg "Current Go version is $go_version"

    if [ ! -d $GOPATH/src/github.com/stretchr/testify ]; then
        go get github.com/stretchr/testify
        cd $GOPATH/src/github.com/stretchr/testify
        git checkout tags/v1.6.1
        cd -
    fi

    export CGO_ENABLED=1
    export CGO_LDFLAGS_ALLOW="-fprofile-arcs|-ftest-coverage|--coverage"
  fi
}

function install_cpp_core {
    print_msg "Installing C++ core library"
    cd $YDKGEN_HOME
    local cpp_sudo_flag
    if [ $USER != "root" ]; then cpp_sudo_flag="s"; fi
    run_cmd $PYTHON_BIN generate.py --core --cpp -i$cpp_sudo_flag
}

function install_cpp_gnmi {
    print_msg "Building C++ core gnmi library"
    cd $YDKGEN_HOME
    local cpp_sudo_flag
    if [ $USER != "root" ]; then cpp_sudo_flag="s"; fi
    run_cmd $PYTHON_BIN generate.py --service profiles/services/gnmi-0.4.0.json --cpp -i$cpp_sudo_flag
}

function install_go_core {
    print_msg "Installing Go core packages"
    cd $YDKGEN_HOME
    run_cmd $PYTHON_BIN generate.py -i --core --go
}

function install_go_gnmi {
    print_msg "Installing Go gNMI package"
    cd $YDKGEN_HOME
    run_cmd $PYTHON_BIN generate.py -i --service profiles/services/gnmi-0.4.0.json --go
}

function install_py_core {
    print_msg "Building and installing Python core package"
    cd $YDKGEN_HOME
    run_cmd $PYTHON_BIN generate.py -i$sudo_flag --core

    print_msg "Verifying Python YDK core package installation"
    $PYTHON_BIN -c "from ydk.path import NetconfSession"
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Verification failed for the Python core package 'ydk_.so'"
        exit $status
    fi
}

function install_py_gnmi {
    print_msg "Installing gNMI package for Python"
    cd $YDKGEN_HOME
    run_cmd $PYTHON_BIN generate.py -i$sudo_flag --service profiles/services/gnmi-0.4.0.json

    print_msg "Verifying Python gNMI package installation"
    $PYTHON_BIN -c "from ydk.gnmi.path import gNMISession"
    local status=$?
    if [ $status -ne 0 ]; then
        MSG_COLOR=$RED
        print_msg "Verification failed for the Python gNMI package 'ydk_gnmi_.so'"
        exit $status
    fi
}

function instal_dependencies {
    if [ ${os_type} == "Linux" ]; then
      if [[ ${os_info} == *"Ubuntu"* ]]; then
        run_cmd ${YDKGEN_HOME}/test/dependencies_ubuntu.sh
      else
        run_cmd ${YDKGEN_HOME}/test/dependencies_centos.sh
      fi
      if [ ${service_pkg} == "gnmi" ]; then
        run_cmd ${YDKGEN_HOME}/test/dependencies_linux_gnmi.sh
      fi
    else    # Darwin
      run_cmd ${YDKGEN_HOME}/test/dependencies_osx.sh
      if [ ${service_pkg} == "gnmi" ]; then
        run_cmd ${YDKGEN_HOME}/test/dependencies_osx_gnmi.sh
      fi
    fi
}

function install_ydk_cpp {
    if [[ ${core_package} == "yes" ]]; then
        install_cpp_core
    fi
    if [[ ${service_pkg} == "gnmi" ]]; then
        install_cpp_gnmi
    fi
}

function install_ydk_py {
    if [[ ${ydk_lang} == "py" || ${ydk_lang} == "all" ]]; then
        if [[ ${core_package} == "yes" ]]; then
            install_py_core
        fi
        if [[ ${service_pkg} == "gnmi" ]]; then
            install_py_gnmi
        fi
    fi
}

function install_ydk_go {
    if [[ ${ydk_lang} == "go" || ${ydk_lang} == "all" ]]; then
        if [[ ${core_package} == "yes" ]]; then
            install_go_core
        fi
        if [[ ${service_pkg} == "gnmi" ]]; then
            install_go_gnmi
        fi
    fi
}

function write_env_file {
  cd ${YDKGEN_HOME}
  rm -f .env
  echo "# ------------------------------------------------------------------
# This file has been auto-generated during YDK-$ydk_version installation.
# PLEASE, DO NOT CHANGE THIS FILE MANUALLY!
# ------------------------------------------------------------------
# Run this command once when entering YDK-GEN environment in bash:
#     source .env
# ------------------------------------------------------------------

YDKGEN_HOME=${YDKGEN_HOME}
export YDKGEN_HOME

export C_INCLUDE_PATH=$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH
" > .env
  if [ $install_venv == "yes" ]; then
    echo "export PYTHON_VENV=$PYTHON_VENV" >> .env
    echo "source $PYTHON_VENV/bin/activate" >> .env
  elif [[ -n $python_location ]]; then
    echo "PATH=$python_location/bin:$PATH
export PATH
alias python=$PYTHON_BIN
alias pip=$PIP_BIN
" >> .env
  fi
  if [[ -n $sudo_cmd ]]; then
    echo "export SUDO_CMD=$sudo_cmd" >> .env
  fi
  if [[ $ydk_lang == "go" || $ydk_lang == "all" ]]; then
    if [[ ${os_type} == "Linux" ]]; then
      echo "if [ -z \$GOROOT ]; then
    export GOROOT=$GOROOT
    PATH=$GOROOT/bin:$PATH
    export PATH
fi"
>> .env
    fi
    echo "
if [ -z \$GOPATH ]; then
    export GOPATH=$HOME/go
fi
" >> .env
  fi
  if [ $service_pkg == "gnmi" ]; then
    echo "export LD_LIBRARY_PATH=\$HOME/grpc/libs/opt:\$HOME/protobuf-3.5.0/src/.libs:\$LD_LIBRARY_PATH
" >> .env
  fi
  if [[ -n $CMAKE_LIBRARY_PATH ]]; then
    echo "export CMAKE_LIBRARY_PATH=$CMAKE_LIBRARY_PATH
" >> .env
  fi
#  cat .env
  cd - >& /dev/null
}

########################## EXECUTION STARTS HERE #############################

# Terminal colors
NOCOLOR="\033[0m"
RED="\033[0;31m"
YELLOW='\033[1;33m'
MSG_COLOR=${YELLOW}

######################################
# Parse script options

ydk_lang="py"
service_pkg="no"
core_package="no"
dependencies="yes"
install_venv="no"
sudo_flag=
sudo_cmd=
PYTHON_BIN=python3
PIP_BIN=pip3

# As long as there is at least one more argument, keep looping
while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
        # This is a flag type option. Will catch either -f or --foo
        -l|--lang)
            shift # past the key to the value
            ydk_lang="$1"
            if [[ ${ydk_lang} != "cpp" && ${ydk_lang} != "py" && ${ydk_lang} != "go" && ${ydk_lang} != "all"  ]]; then
                echo "Unknown language ${ydk_lang}"
                usage
                exit 1
            fi
            ;;
        --cpp)
            ydk_lang="cpp"
            ;;
        --go)
            ydk_lang="go"
            ;;
        --py|--python)
            ydk_lang="py"
            ;;
        --all)
            ydk_lang="all"
            ;;
        -n|--no-deps)
            dependencies="no"
            ;;
        -h|--help)
            usage
            exit 1
            ;;
        -c|--core)
            core_package="yes"
            ;;
        -s|--service)
            shift # past the key and to the value
            service_pkg="$1"
            if  [[ ${service_pkg} != "gnmi" ]]; then
                echo "Unknown service package specified; gnmi assumed"
                service_pkg="gnmi"
            fi
            ;;
        -v|--venv)
            install_venv="yes"
            ;;
        -p|--python-dir)
            python_location="$2"
            if [[ -n $python_location && ${python_location:0:1} != "-" ]]; then
                shift
                if [[ ! -d $python_location || ! -x $python_location/bin/python3 ]]; then
                    echo "Wrong Python installation directory specified!"
                    echo "System installation will be used"
                    unset python_location
                elif [ $install_venv == "no" ]; then
                    PYTHON_BIN=$python_location/bin/python3
                    PIP_BIN=$python_location/bin/pip3
                fi
            fi
            ;;
        *)
            echo "Unknown option '$key'"
            usage
            exit 1
            ;;
    esac
    # Shift after checking all the cases to get the next option
    shift
done

curr_dir=$(pwd)
script_dir=$(cd $(dirname ${BASH_SOURCE}) && pwd)
if [[ -z ${YDKGEN_HOME} || ! -d ${YDKGEN_HOME} ]]; then
    YDKGEN_HOME=$script_dir
    print_msg "YDKGEN_HOME is set to $script_dir"
fi
cd ${YDKGEN_HOME}

ydk_version=$(grep core sdk/version.json | awk '{print($2)'} | tr -d '"' | tr -d ',')
echo "YDK-$ydk_version installation options:"
if [ ${install_venv} == "no" ]; then
  if [[ -n $python_location ]]; then
    echo " - use custom Python installation in ${python_location}"
  else
    echo " - use system Python installation"
  fi
else
  echo " - create Python virtual environment = ${install_venv}"
fi
echo " - programming language = ${ydk_lang}"
echo " - install dependencies = ${dependencies}"
echo " - install core package = ${core_package}"
echo " - install service package = ${service_pkg}"
if [[ ${core_package} == "no" && ${service_pkg} == "no" && ${dependencies} == "no" ]]; then
    echo "There are no components to install"
    exit 0
fi

######################################
# Set up installation environment

os_type=$(uname)
if [[ ${os_type} == "Linux" ]]; then
    os_info=$(cat /etc/*-release)
elif [[ ${os_type} == "Darwin" ]]; then
    os_info=$(sw_vers)
else
    MSG_COLOR=${RED}
    print_msg "Unsupported OS type '${os_type}' detected"
    exit 1
fi
print_msg "Running OS type: $os_type"
print_msg "OS info: $os_info"
if [[ ${os_type} == "Linux" ]]; then
  if [[ ${os_info} == *"Ubuntu"* ]]; then
    if [[ ${os_info} != *"xenial"* && ${os_info} != *"bionic"* && ${os_info} != *"focal"* ]]; then
        print_msg "WARNING! Unsupported Ubuntu distribution found. Will try the best efforts."
    fi
  elif [[ ${os_info} == *"fedora"* ]]; then
    rhel_version=$(echo `lsb_release -r` | awk '{ print $2 }' | cut -d '.' -f 1)
    if [[ $rhel_version != 7 && $rhel_version != 8 ]]; then
        print_msg "WARNING! Unsupported Centos/RHEL version. Will try the best efforts."
    fi
  else
    MSG_COLOR=${RED}
    print_msg "Unsupported Linux distribution detected"
    exit 1
  fi
fi

if [[ -z ${C_INCLUDE_PATH} ]]; then
    export C_INCLUDE_PATH=/usr/local/include
fi
if [[ -z ${CPLUS_INCLUDE_PATH} ]]; then
    export CPLUS_INCLUDE_PATH=/usr/local/include
fi

if [[ $(uname) == "Linux" && ${os_info} == *"fedora"* ]]; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64:/usr/lib64
    if [ ${service_pkg} == "gnmi" ]; then
        export LD_LIBRARY_PATH=$HOME/grpc/libs/opt:$HOME/protobuf-3.5.0/src/.libs:$LD_LIBRARY_PATH
    fi
    print_msg "LD_LIBRARY_PATH is set to: $LD_LIBRARY_PATH"
fi

if [ ${dependencies} == "yes" ]; then
    instal_dependencies
fi
if [ -f ~/.profile.python ]; then
  print_msg "Reading python profile ~/.profile.python"
  source ~/.profile.python
fi

CMAKE_BIN=cmake
command -v cmake3 > /dev/null
status=$?
if [[ ${status} == 0 ]]; then
    CMAKE_BIN=cmake3
fi

######################################
# Start installation

init_py_env
init_go_env

write_env_file

install_ydk_cpp

install_ydk_py

install_ydk_go

if [ ${install_venv} == "yes" ]; then
  deactivate
fi

cd ${curr_dir}
