#!/bin/bash
#  ----------------------------------------------------------------
# Copyright 2016-2019 Cisco Systems
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
# ------------------------------------------------------------------
# This file has been modified by Yan Gorelik, YDK Solutions.
# All modifications in original under CiscoDevNet domain
# introduced since October 2019 are copyrighted.
# All rights reserved under Apache License, Version 2.0.
# ------------------------------------------------------------------
#
# Script for running ydk CI on docker via travis-ci.org
# and installing YDK from install_ydk.sh script
#
# dependencies_centos (Centos/RHEL 7 and 8)
# ------------------------------------------------------------------

function print_msg {
    echo -e "${MSG_COLOR}*** $(date) *** dependencies_centos.sh | $* ${NOCOLOR}"
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

function check_install_gcc {
  which gcc
  local status=$?
  if [[ $status == 0 ]]
  then
    gcc_version=$(echo $(gcc --version) | awk '{ print $3 }')
    print_msg "Current gcc/g++ version is $gcc_version"
  else
    print_msg "The gcc/g++ not installed"
    gcc_version="4.0.0"
  fi
  major=$(echo $gcc_version | cut -d '.' -f 1)
  if [[ $major -le 4 && $gcc_version < "4.8.1" ]]
  then
    print_msg "Upgrading gcc/g++ to version 7"
    $sudo_cmd yum install centos-release-scl -y > /dev/null
    $sudo_cmd yum install devtoolset-7-gcc* -y > /dev/null
    local status2=$?
    if [[ $status2 != 0 ]]; then
      MSG_COLOR=$RED
      print_msg "Failed to install gcc; exiting"
      exit 1
    else
      $sudo_cmd ln -sf /opt/rh/devtoolset-7/root/usr/bin/gcc /usr/bin/cc
      $sudo_cmd ln -sf /opt/rh/devtoolset-7/root/usr/bin/g++ /usr/bin/c++

      $sudo_cmd ln -sf /opt/rh/devtoolset-7/root/usr/bin/gcc /usr/bin/gcc
      $sudo_cmd ln -sf /opt/rh/devtoolset-7/root/usr/bin/g++ /usr/bin/g++

      $sudo_cmd ln -sf /opt/rh/devtoolset-7/root/usr/bin/gcov /usr/bin/gcov
      gcc_version=$(echo $(gcc --version) | awk '{ print $3 }')
      print_msg "Installed gcc/g++ version is $gcc_version"
    fi
  fi
}

function install_dependencies {
    print_msg "Installing dependencies"
    $sudo_cmd dnf install redhat-lsb-core -y
    centos_version=$(echo `lsb_release -r` | awk '{ print $2 }' | cut -d '.' -f 1)
    print_msg "Running Centos/RHEL version $centos_version"
    if [[ $centos_version == 8 ]]; then
        run_cmd $sudo_cmd yum update --nobest -y > /dev/null
    else
        run_cmd $sudo_cmd yum update -y > /dev/null
    fi
    run_cmd $sudo_cmd yum install epel-release -y > /dev/null
#    run_cmd $sudo_cmd yum install https://centos7.iuscommunity.org/ius-release.rpm -y > /dev/null
    run_cmd $sudo_cmd yum install which libxml2-devel libxslt-devel libssh-devel libtool gcc-c++ -y > /dev/null
    run_cmd $sudo_cmd yum install pcre-devel pcre-static -y > /dev/null
#    run_cmd $sudo_cmd yum install pcre-static.x86_64 glibc-static libstdc++-static -y > /dev/null
    run_cmd $sudo_cmd yum install cmake3 wget curl-devel unzip make java mlocate flex bison -y > /dev/null
    run_cmd $sudo_cmd yum install python3-devel -y > /dev/null
    $sudo_cmd yum install valgrind -y > /dev/null
    $sudo_cmd yum install rpm-build redhat-lsb redhat-lsb-core -y > /dev/null
#    sudo yum install python3-venv -y
    if [[ $centos_version == 8 ]]; then
      $sudo_cmd yum install dnf-plugins-core -y
      $sudo_cmd yum config-manager --set-enabled powertools
      $sudo_cmd yum glibc-static -y
    fi
    $sudo_cmd yum install doxygen -y
    $sudo_cmd yum install lcov -y
}

function check_install_go {
  go_exec=$(which go)
  if [[ -z ${go_exec} && -d /usr/local/go ]]; then
    go_exec=/usr/local/go/bin/go
  fi
  if [[ -x ${go_exec} ]]
  then
    go_version=$(echo `$go_exec version` | awk '{ print $3 }' | cut -d 'o' -f 2)
    print_msg "Current Go version is $go_version"
    minor=$(echo $go_version | cut -d '.' -f 2)
  else
    print_msg "The Go is not installed"
    minor=0
  fi
  if [ $minor -lt 9 ]; then
    print_msg "Installing Golang version 1.13.1"
    $curr_dir/3d_party/go/goinstall.sh --version 1.13.1 > /dev/null
    $sudo_cmd ln -sf $HOME/.go /usr/local/go
    $sudo_cmd ln -sf /usr/local/go/bin/go /usr/local/bin/go
  fi
}

function check_install_libssh {
  locate libssh_threads.so
  local status=$?
  if [ $status -ne 0 ]; then
    print_msg "Installing libssh-0.7.6"
    run_cmd wget https://git.libssh.org/projects/libssh.git/snapshot/libssh-0.7.6.tar.gz
    tar zxf libssh-0.7.6.tar.gz && rm -f libssh-0.7.6.tar.gz
    mkdir libssh-0.7.6/build && cd libssh-0.7.6/build
    run_cmd cmake3 ..
    run_cmd $sudo_cmd make install
    cd - > /dev/null
  else
    cd /usr/lib64
    if [[ ! -L libssh_threads.so && -L libssh_threads.so.4 ]]; then
      print_msg "Adding symbolic link /usr/lib64/libssh_threads.so"
      $sudo_cmd ln -s libssh_threads.so.4 libssh_threads.so
    fi
    cd - > /dev/null
  fi
}

function install_confd {
  if [[ ! -s $HOME/confd/bin/confd ]]; then
    if [[ $centos_version -gt 7 ]]; then
      print_msg "Installing confd basic 7.3"
      unzip $curr_dir/3d_party/linux/confd-basic-7.3.linux.x86_64.zip
      cd confd-basic-7.3.linux.x86_64
      run_cmd ./confd-basic-7.3.linux.x86_64.installer.bin $HOME/confd
      cd - > /dev/null
    else
      print_msg "Installing confd basic 6.2"
      run_cmd wget https://github.com/CiscoDevNet/ydk-gen/files/562538/confd-basic-6.2.linux.x86_64.zip &> /dev/null
      unzip confd-basic-6.2.linux.x86_64.zip
      run_cmd ./confd-basic-6.2.linux.x86_64.installer.bin $HOME/confd
    fi
    rm -rf confd-basic* ConfD*
  fi
}

function install_openssl {
  if [[ ! -s $HOME/confd/lib/libcrypto.so.1.0.0 ]]; then
    print_msg "Installing openssl 0.1.0u for confd"
    run_cmd wget https://www.openssl.org/source/openssl-1.0.1u.tar.gz &> /dev/null
    tar -xvzf openssl-1.0.1u.tar.gz > /dev/null
    rm -rf openssl-1.0.1u.tar.gz
    cd openssl-1.0.1u
    run_cmd ./config shared > /dev/null
    run_cmd make all > /dev/null
    cp libcrypto.so.1.0.0 $HOME/confd/lib
    cd - > /dev/null
    rm -rf openssl-1.0.1u
  fi
}

########################## EXECUTION STARTS HERE #############################
# Terminal colors
NOCOLOR="\033[0m"
YELLOW='\033[1;33m'
MSG_COLOR=$YELLOW

sudo_cmd=
if [ $(id -u -n) != "root" ]; then
  sudo_cmd="sudo"
fi

curr_dir=$(pwd)

install_dependencies
check_install_gcc
check_install_go

$sudo_cmd updatedb
check_install_libssh

# These components needed only for YDK unit testing
# Confd Netconf server and dependent OpenSSL library
#
install_confd
install_openssl

