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
# dependencies_ubuntu (Ubuntu 16.04, 18.04, 20.04)
# ------------------------------------------------------------------

function print_msg {
    echo -e "${MSG_COLOR}*** $(date) *** dependencies_ubuntu.sh | $* ${NOCOLOR}"
}

function run_cmd {
    local cmd=$@
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

function install_dependencies {
    print_msg "Installing dependencies"

    sudo apt-get update -y -qq
    sudo apt-get install sudo -y -qq
    $sudo_cmd apt-get install -y -qq lsb-release
    codename=$(lsb_release -c | awk '{ print $2 }')
    ubuntu_release=$(lsb_release -r | awk '{ print $2 }' | cut -d '.' -f 1)
    if [[ $codename == "focal" || $codename == "jammy" ]] && [[ ! -h /etc/localtime ]]; then
      # Fixing timezone setting issue in focal
      export DEBIAN_FRONTEND=noninteractive
      $sudo_cmd apt-get install -y -qq tzdata
      ln -fs /usr/share/zoneinfo/US/Pacific /etc/localtime
      dpkg-reconfigure --frontend noninteractive tzdata
      unset DEBIAN_FRONTEND
    fi
    run_cmd $sudo_cmd apt-get install -y -qq --no-install-recommends apt-utils
    run_cmd $sudo_cmd apt-get install -y -qq build-essential
    run_cmd $sudo_cmd apt-get install -y -qq libtool-bin
    local status=$?
    if [[ ${status} != 0 ]]; then
        run_cmd $sudo_cmd apt-get install -y -qq libtool
    fi
    if [[ $codename == "focal" || $codename == "jammy" ]]; then
        $sudo_cmd apt-get install -y -qq mlocate git
        if [[ ! -h /usr/local/lib/libnettle.so.6 ]]; then
          cd /usr/local/lib/
          $sudo_cmd ln -s $curr_dir/3d_party/linux/ubuntu/lib/libnettle.so.6.4
          $sudo_cmd ln -s libnettle.so.6.4 libnettle.so.6
          cd - > /dev/null
        fi
    else
        run_cmd $sudo_cmd apt-get install -y -qq locate git
        run_cmd $sudo_cmd apt-get install -y -qq curl libcurl4-openssl-dev
    fi
    run_cmd $sudo_cmd apt-get install -y -qq bison doxygen flex unzip wget cmake gdebi-core lcov
    run_cmd $sudo_cmd apt-get install -y -qq libcmocka0 libpcre3-dev libpcre++-dev
    run_cmd $sudo_cmd apt-get install -y -qq libssh-dev libxml2-dev libxslt1-dev
    run_cmd $sudo_cmd apt-get install -y -qq python3-dev python3-lxml python3-pip python3-venv
    run_cmd $sudo_cmd apt-get install -y -qq pkg-config software-properties-common zlib1g-dev openjdk-8-jre
    run_cmd $sudo_cmd apt-get install -y -qq valgrind
    if [[ $codename == "focal" || $codename == "jammy" ]]; then
        run_cmd $sudo_cmd apt-get install -y -qq python3-pybind11
    fi
}

function check_install_gcc_link {
  cd /usr/bin
  if [ -x $1 ]; then
    $sudo_cmd ln -fs $1 $2
  else
    print_msg "Compiler /usr/bin/$1 is not installed!"
    return 1
  fi
  cd - > /dev/null
  return 0
}

function check_install_gcc {
  which gcc > /dev/null
  local status_gcc=$?
  which g++ > /dev/null
  local status_gxx=$?
  if [[ $status_gcc == 0  && $status_gxx == 0 ]]
  then
    gcc_version=$(echo $(gcc --version) | awk '{ print $3 }' | cut -d '-' -f 1)
    print_msg "Current gcc/g++ version is $gcc_version"
    local major=$(echo $gcc_version | cut -d '.' -f 1)
    if [[ $codename == "focal" && $major -gt 7 ]]; then
      print_msg "Installing gcc/g++ version 7"
#       $sudo_cmd add-apt-repository ppa:ubuntu-toolchain-r/test -y
#       $sudo_cmd apt-get update -y > /dev/null
      $sudo_cmd apt-get install gcc-7 g++-7 -y > /dev/null
      gcc_version=$(echo $(gcc --version) | awk '{ print $3 }' | cut -d '-' -f 1)
      print_msg "Installed gcc/g++ version is $gcc_version"
      major=$(echo $gcc_version | cut -d '.' -f 1)
    fi
    print_msg "Checking and installing symbolic links for the gcc/g++ compilers"
    run_cmd check_install_gcc_link gcc-$major cc
    run_cmd check_install_gcc_link g++-$major c++
  else
    print_msg "The gcc/g++ not installed"
    exit 1
  fi
}

function check_install_curl {
  if which curl > /dev/null; then
    print_msg "Installed curl version: $(curl --version | sed 1q | awk '{print$2}')"
  else
    print_msg "Installing curl from source"
    git clone https://github.com/curl/curl.git -b curl-7_61_1
    cd curl
    ./buildconf
    ./configure --enable-versioned-symbols --with-openssl > /dev/null
    make > /dev/null
    $sudo_cmd make install
    cd - > /dev/null
    $sudo_cmd rm -f /usr/lib/x86_64-linux-gnu/libcurl.so
    $sudo_cmd ln -sf /usr/local/lib/libcurl.so.4 /usr/lib/x86_64-linux-gnu/libcurl.so
    rm -rf curl
    print_msg "Installed curl version: $(curl --version | sed 1q | awk '{print$2}')"
  fi
}

function check_install_libssh {
  if [[ $codename == "focal" ]] && [[ ! -h /usr/local/lib/libssh_threads.so ]]; then
    print_msg "Copying libssh and libssh_threads to /usr/local/lib"
    sudo cp $curr_dir/3d_party/linux/ubuntu/lib/libssh.so.4.5.0 /usr/local/lib/
    sudo cp $curr_dir/3d_party/linux/ubuntu/lib/libssh_threads.so.4.5.0 /usr/local/lib/
    cd /usr/local/lib/
    sudo ln -s libssh.so.4.5.0 libssh.so.4
    sudo ln -s libssh.so.4 libssh.so
    sudo ln -s libssh_threads.so.4.5.0 libssh_threads.so.4
    sudo ln -s libssh_threads.so.4 libssh_threads.so
    cd - > /dev/null
  fi
  if [[ $codename == "jammy" ]]; then
    run_cmd $sudo_cmd apt-get install -y -qq libcurl4-openssl-dev
    if [[ ! -e "/usr/lib/x86_64-linux-gnu/libssh_threads.so.4" ]]; then
      run_cmd $sudo_cmd ln -s /usr/lib/x86_64-linux-gnu/libssh.so.4 /usr/lib/x86_64-linux-gnu/libssh_threads.so.4
    fi
    if [[ ! -e "/usr/lib/x86_64-linux-gnu/libssh_threads.so" ]]; then
      run_cmd $sudo_cmd ln -s /usr/lib/x86_64-linux-gnu/libssh.so.4 /usr/lib/x86_64-linux-gnu/libssh_threads.so
    fi
  fi
}

function check_install_go {
  if [[ $codename == "jammy" ]]; then
    if which go > /dev/null; then
      print_msg "Current Go version is: $(go version | grep --only-matching --perl-regexp '(?<= go)[\d\.]+')"
    else
      run_cmd $sudo_cmd apt-get install -y -qq golang-go
    fi
  else
    go_exec=$(which go)
    if [[ -z ${go_exec} && -d /usr/local/go ]]; then
      go_exec=/usr/local/go/bin/go
    fi
    if [[ -x ${go_exec} ]]
    then
      go_version=$(echo `${go_exec} version` | awk '{ print $3 }' | cut -d 'o' -f 2)
      print_msg "Current Go version is $go_version"
      minor=$(echo $go_version | cut -d '.' -f 2)
    else
      print_msg "The Go is not installed"
      minor=0
    fi
    if [ $minor -lt 9 ]; then
      print_msg "Installing Golang version 1.13.1 in /usr/local/go"
      run_cmd wget https://storage.googleapis.com/golang/go1.13.1.linux-amd64.tar.gz
      $sudo_cmd tar -zxf  go1.13.1.linux-amd64.tar.gz -C /usr/local/
      rm -f go1.13.1.linux-amd64.tar.gz
      cd /usr/local/bin
      $sudo_cmd ln -sf /usr/local/go/bin/go
      cd - > /dev/null
    fi
  fi
}

function check_install_confd {
  if [[ ! -s $HOME/confd/bin/confd ]]; then
    if [[ $ubuntu_release -lt 20 ]]; then
      print_msg "Installing confd-basic-6.2"
      run_cmd wget https://github.com/CiscoDevNet/ydk-gen/files/562538/confd-basic-6.2.linux.x86_64.zip &> /dev/null
      unzip confd-basic-6.2.linux.x86_64.zip
      run_cmd ./confd-basic-6.2.linux.x86_64.installer.bin $HOME/confd
    else
      print_msg "Installing confd-basic-7.3"
      unzip $curr_dir/3d_party/linux/confd-basic-7.3.linux.x86_64.zip
      cd confd-basic-7.3.linux.x86_64
      run_cmd ./confd-basic-7.3.linux.x86_64.installer.bin $HOME/confd
      cd - > /dev/null
      ln -s $curr_dir/3d_party/linux/ubuntu/lib/libcrypto.so.1.0.0 $HOME/confd/lib/libcrypto.so.1.0.0
      ln -s $curr_dir/3d_party/linux/ubuntu/lib/libncurses.so.5.9 $HOME/confd/lib/libncurses.so.5
      ln -s $curr_dir/3d_party/linux/ubuntu/lib/libtinfo.so.5.9 $HOME/confd/lib/libtinfo.so.5
    fi
    rm -rf confd-basic-* ConfD*
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

if [[ $ubuntu_release -gt 19 ]]; then
  check_install_curl
fi
check_install_confd

if grep -qi microsoft /proc/version; then
  # ubuntu in wsl do not include "windows" mounted drives
  $sudo_cmd updatedb --prunepaths='/mnt/c /mnt/wsl /mnt/wslg'
else 
  # native ubuntu
  $sudo_cmd updatedb
fi
check_install_libssh
