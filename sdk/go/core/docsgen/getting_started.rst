..
  #  YDK - YANG Development Kit
  #  Copyright 2016 Cisco Systems. All rights reserved
  # *************************************************************
  # Licensed to the Apache Software Foundation (ASF) under one
  # or more contributor license agreements.  See the NOTICE file
  # distributed with this work for additional information
  # regarding copyright ownership.  The ASF licenses this file
  # to you under the Apache License, Version 2.0 (the
  # "License"); you may not use this file except in compliance
  # with the License.  You may obtain a copy of the License at
  #
  #   http:#www.apache.org/licenses/LICENSE-2.0
  #
  #  Unless required by applicable law or agreed to in writing,
  # software distributed under the License is distributed on an
  # "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  # KIND, either express or implied.  See the License for the
  # specific language governing permissions and limitations
  # under the License.
  # *************************************************************
  # This file has been modified by Yan Gorelik, YDK Solutions.
  # All modifications in original under CiscoDevNet domain
  # introduced since October 2019 are copyrighted.
  # All rights reserved under Apache License, Version 2.0.
  # *************************************************************

===============
Getting Started
===============
.. contents:: Table of Contents

Overview
========

The YANG Development Kit (YDK) is a software development tool, which provides API for building applications based on YANG models.
The main goal of YDK is to reduce the learning curve of YANG data models by expressing the model semantics in an API
and abstracting protocol/encoding details.  YDK is composed of a core package that defines services and providers,
plus one or more module bundles that are based on YANG models.

Backward Compatibility
======================

Although YDK-0.9.0 API is mostly the same as in previous YDK releases, it generates different code and model API comparing to YDK-0.8.5.
The YDK-0.9.0 generated code is not compatible with YDK-0.8.5 and earlier bundle packages due to changes in Entity and YLeaf classes.

**NOTE.** Starting from release 0.8.5 the YDK does not support Python2 interpreter as it was deprecated.


Docker
======

A `docker image <https://docs.docker.com/engine/reference/run/>`_ is automatically built with the latest ydk-gen installed.
This be used to run ydk-gen without installing anything natively on your platform.

To use the docker image, `install docker <https://docs.docker.com/install/>`_ on your system and run the below command.
See the `docker documentation <https://docs.docker.com/engine/reference/run/>`_ for more details::

  docker run -it ydksolutions/ydk:0.9.0.1


System Requirements
===================

The YDK is currently supported on the following platforms including native installations, virtual machines, and docker images:

 - Linux Ubuntu Xenial (16.04 LTS), Bionic (18.04 LTS), and Focal (20.04 LTS)
 - Linux CentOS/RHEL versions 7 and 8
 - MacOS up to 10.14.6 (Mojave)

On Windows 10 the Linux virtual machine can run using Windows Subsystem for Linux (WSL);
check `this <https://www.windowscentral.com/install-windows-subsystem-linux-windows-10>`_ for virtual machine installation procedure.
The YDK has been tested in such environment on Ubuntu Bionic (18.04 LTS) and Focal (20.04 LTS) images obtained
from Microsoft Store.

On supported platforms the YDK can be installed using `Installation Script`_.
On other platforms the YDK should be installed manually `Building from source`_.
For both the methods the user must install `git` package prior to the installation procedure.

All YDK core components are based on C and C++ code. These components compiled using default compilers for the supported platform.
Corresponding binaries, libraries, and header files are installed in default locations,
which are `/usr/local/bin`, `/usr/local/lib`, and `/usr/local/include`.
The user must have sudo access in order to install YDK core components to these locations.

**NOTE.** Due to GitHub issue `#1050 <https://github.com/CiscoDevNet/ydk-gen/issues/1050>`_ YDK is not supported with Python 3.9.x.

.. _howto-install:

Core Installation
=================

Installation Script
-------------------

For YDK installation it is recommended to use script `install_ydk.sh` from `ydk-gen` git repository.
The script detects platform OS, installs all the dependencies and builds complete set of YDK components for specified language.
The user must have sudo access to these locations.

The YDK extensively uses Python scripts for building its components and model API packages (bundles).
In order to isolate YDK Python environment from system installation, the script builds Python3 virtual environment.
The user must manually activate virtual environment when generating model bundles and/or running YDK based application.
By default the Python virtual environment is installed under `$HOME/venv` directory.
If user has different location, the PYTHON_VENV environment variable should be set to that location.

Here is simple example of core YDK installation for Python programming language:

.. code-block:: sh

    git clone https://github.com/ygorelik/ydk-gen.git
    cd ydk-gen
    export YDKGEN_HOME=`pwd`  # optional
    export PYTHON_VENV=$HOME/ydk_vne  # optional
    ./install_ydk.sh --core


The script also allows to install individual components like dependencies, core, and service packages
for specified programming language or for all supported languages.
Full set of script capabilities could be viewed like this::

    ./install_ydk.sh --help
    usage: install_ydk [-l [cpp, py, go]] [-s gnmi] [-h] [-n]
    Options and arguments:
      -l [cpp, py, go, all] installation language; if not specified Python is assumed
                            'all' corresponds to all available languages
      -c|--core             install YDK core package
      -s|--service gnmi     install gNMI service package
      -n|--no-deps          skip installation of dependencies
      -h|--help             print this help message and exit

    Environment variables:
    YDKGEN_HOME         specifies location of ydk-gen git repository;
                        if not set, $HOME/ydk-gen is assumed
    PYTHON_VENV         specifies location of python virtual environment;
                        if not set, /home/ygorelik/venv is assumed
    GOROOT              specifies installation directory of go software;
                        if not set, /usr/local/go is assumed
    GOPATH              specifies location of go source directory;
                        if not set, $HOME/go is assumed
    C_INCLUDE_PATH      location of C include files;
                        if not set, /usr/local/include is assumed
    CPLUS_INCLUDE_PATH  location of C++ include files;
                        if not set, /usr/local/include is assumed
    CMAKE_LIBRARY_PATH  Location of Python shared libraries;
                        if not set, default system library location is assumed


If user environment is different from the default one (different Python installation or different
location of libraries), then building from source method should be used.

Building from source
--------------------

Environment variables
~~~~~~~~~~~~~~~~~~~~~

In some OS configurations during YDK package installation the cmake fails to find C/C++ headers for previously installed YDK libraries.
In this case the header location must be specified explicitly (in below commands the default location is shown)::

  export C_INCLUDE_PATH=/usr/local/include
  export CPLUS_INCLUDE_PATH=/usr/local/include

When non-standard Python installation is used or there are multiple installations of Python on the platform,
the PATH and CMAKE_LIBRARY_PATH environment variables must be set accordingly in order for the installation scripts
to pick up correct Python binaries and shared libraries.

Installing third party dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If user platform is supported one, it is recommended to use `ydk-gen/install_ydk.sh` script.
The script will also install Python virtual environment in default or specified location::

    # Clone ydk-gen from GitHub
    git clone https://github.com/ygorelik/ydk-gen.git
    cd ydk-gen

    # Define optional environment variables and install dependencies
    export YDKGEN_HOME=`pwd`
    export PYTHON_VENV=$HOME/ydk_venv
    ./install_ydk.sh   # also builds Python virtual environment

For unsupported platforms it is recommended to follow logic of `ydk-gen/test/dependencies-*` scripts.

Installing core components
~~~~~~~~~~~~~~~~~~~~~~~~~~

Please follow this procedure to install YDK core components for Python apps development::

    # Activate Python virtual environment
    source $PYTHON_VENV/bin/activate

    # Generate and install YDK core library
    ./generate.py -is --core --cpp

    # Generate and install Python core package
    ./generate.py -i --core --py

Adding gNMI Service
-------------------

In order to enable YDK support for gNMI protocol, which is optional, the user need install third party software
and YDK gNMI service package.

gNMI Service installation
~~~~~~~~~~~~~~~~~~~~~~~~~

Here is simple example, how gNMI service package for Python could be added::

    cd ydk-gen
    ./install_ydk.sh -l py --service gnmi


gNMI runtime environment
~~~~~~~~~~~~~~~~~~~~~~~~

There is an open issue with gRPC on Centos/RHEL, which requires an extra step before running any YDK gNMI application.
See this issue on `GRPC GitHub <https://github.com/grpc/grpc/issues/10942#issuecomment-312565041>`_ for details.
As a workaround, the YDK based application runtime environment must include setting of `LD_LIBRARY_PATH` variable::

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/grpc/libs/opt:~/protobuf-3.5.0/src/.libs:/usr/local/lib:/usr/local/lib64


Documentation and Support
=========================

- Read the `API documentation <http://ydk.cisco.com/go/docs>`_ for details on how to use the API and specific models
- Samples can be found under the `samples directory <https://github.com/CiscoDevNet/ydk-go/tree/master/samples>`_
- Additional samples can be found in the `YDK-Go samples repository <https://github.com/CiscoDevNet/ydk-go-samples>`_ (coming soon)
- Join the `YDK community <https://communities.cisco.com/community/developer/ydk>`_ to connect with other users and with the makers of YDK
- Additional YDK information can be found at `ydk.io <http://ydk.io>`_

Release Notes
=============

The current YDK release version is 0.9.0.1.

YDK-Go is licensed under the Apache 2.0 License.
