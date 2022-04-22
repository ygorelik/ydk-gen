..
  # *************************************************************
  #  YDK-YANG Development Kit
  #  Copyright 2016-2019 Cisco Systems. All rights reserved
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

.. image::  https://travis-ci.com/CiscoDevNet/ydk-py.svg?branch=master
    :target: https://travis-ci.com/CiscoDevNet/ydk-py

.. image:: https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg
    :alt: Docker Automated build
    :target: https://hub.docker.com/r/ydkdev/ydk-py/

=============================
YANG Development Kit (Python)
=============================

.. contents:: Table of Contents

Overview
========

The YANG Development Kit (YDK) is a software development tool, which provides API for building applications based on YANG models.
The main goal of YDK is to reduce the learning curve of YANG data models by expressing the model semantics in an API and abstracting protocol/encoding details.
YDK is composed of a core package that defines services and providers, plus one or more module bundles that are based on YANG models.

Backward Compatibility
======================

The Python YDK-0.8.6 core package is compatible with all model bundles generated previously with ydk-gen releases starting from 0.7.3.
However the YDK-0.8.6 generates slightly different code and model API comparing to YDK-0.8.4.
The YDK-0.8.6 generated code is not compatible with YDK-0.7.2 and earlier bundle packages due to changes in modeling and handling of YList objects.

**NOTE.** Starting from release 0.8.5 the YDK does not support Python2 interpreter as it was deprecated.


Docker
======

To use the docker image, `install docker <https://docs.docker.com/install/>`_ on your system and run the below command.
See the `docker documentation <https://docs.docker.com/engine/reference/run/>`_ for more details::

  docker run -it ydksolutions/ydk-gen:0.8.6.3


..
  A `docker image <https://docs.docker.com/engine/reference/run/>`_ is automatically built with the latest ydk-py commit to the GitHub.
  The docker image is used to run ydk-py without installing anything natively on your machine.

  To use the docker image, `install docker <https://docs.docker.com/install/>`_ on your system and run the below command.
  See the `docker documentation <https://docs.docker.com/engine/reference/run/>`_ for more details::

    docker run -it ydksolutions/ydk-gen:0.8.6.3


System Requirements
===================

The YDK is currently supported on the following platforms including native installations, virtual machines, and docker images:

 - Linux Ubuntu Xenial (16.04 LTS), Bionic (18.04 LTS), and Focal (20.04 LTS)
 - Linux CentOS/RHEL versions 7 and 8.2
 - MacOS up to 11.6.2 (Big Sur)

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

**NOTE.** It is strongly recommended to use Python virtual environment on Centos/RHEL and Mac platforms.

Core Installation
=================

Installation Script
-------------------

For YDK installation it is recommended to use script `install_ydk.sh` from `ydk-gen` git repository.
The script detects platform OS, installs all the dependencies and builds complete set of YDK components for specified language.
The user must have sudo access to these locations.

The YDK extensively uses Python scripts for building its components and model API packages (bundles).
By default the YDK uses Python system installation.
In order to isolate YDK Python environment from system installation, the script can build Python3 virtual environment.
If built, the user must manually activate virtual environment when generating model bundles and/or running YDK based application.
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
    usage: install_ydk [ {--cpp|--py|--go|--all} ] [-c] [-s gnmi] [-h] [-n] [-v]
    Options and arguments:
      --cpp                 install YDK for C++ programming language
      --go                  install YDK for Go programming language
      --py|--python         install YDK for Python programming language (default)
      --all                 install YDK for all supported programming languages
      -v|--venv             create python virtual environment
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
location of libraries) then building from source method should be used.

Building from source
--------------------

Environment variables
~~~~~~~~~~~~~~~~~~~~~

In some OS configurations during YDK package installation the cmake fails to find C/C++ headers for previously installed YDK libraries.
In this case the headers file location must be specified explicitly (in below commands the default location is shown)::

    export C_INCLUDE_PATH=/usr/local/include
    export CPLUS_INCLUDE_PATH=/usr/local/include

When non-standard Python installation is used or there are multiple installations of Python on the platform,
the PATH and CMAKE_LIBRARY_PATH environment variables must be set accordingly in order for the installation scripts
to pick up correct Python binaries and shared libraries.

Installing third party dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If user platform is supported one, it is recommended to use `ydk-gen/install_ydk.sh` script.
The script will also install Python virtual environment in default or specified location, when '--venv' is specified::

    # Clone ydk-gen from GitHub
    git clone https://github.com/ygorelik/ydk-gen.git
    cd ydk-gen

    # Define optional environment variables and install dependencies
    export YDKGEN_HOME=`pwd`
    export PYTHON_VENV=$HOME/ydk_venv
    ./install_ydk.sh -v   # also builds Python virtual environment

For unsupported platforms it is recommended to follow logic of `ydk-gen/test/dependencies-*` scripts.

Installing core components
~~~~~~~~~~~~~~~~~~~~~~~~~~

Please follow this procedure to install YDK core components for Python apps development::

    # If created, activate Python virtual environment
    source $PYTHON_VENV/bin/activate

    # Generate and install YDK core library
    python3 generate.py -is --core --cpp

    # Generate and install Python core package
    python3 generate.py -i --py --core -v

Adding gNMI Service
-------------------

In order to enable YDK support for gNMI protocol, which is optional, the user need install third party software
and YDK gNMI service package.

gNMI service installation
~~~~~~~~~~~~~~~~~~~~~~~~~

Here is simple example, how gNMI service package for Python could be added::

    cd ydk-gen
    ./install_ydk.sh --py --service gnmi -v


gNMI runtime environment
~~~~~~~~~~~~~~~~~~~~~~~~

There is an open issue with gRPC on Centos/RHEL, which requires an extra step before running any YDK gNMI application.
See this issue on `GRPC GitHub <https://github.com/grpc/grpc/issues/10942#issuecomment-312565041>`_ for details.
As a workaround, the YDK based application runtime environment must include setting of `LD_LIBRARY_PATH` variable::

    PROTO=$HOME  # Default location defined during installation
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PROTO/grpc/libs/opt:$PROTO/protobuf-3.5.0/src/.libs:/usr/local/lib:/usr/local/lib64


Using Python virtual environment
================================

You may want to perform the installation under Python `virtual environment <https://pypi.python.org/pypi/virtualenv/>`_.
The virtual environment allows you to install multiple versions of YDK if needed.  In addition, it prevents any potential conflicts between package dependencies in your system.

To install virtual environment use parameter '-v' or '--venv' with the `Installation Script`_.

To activate virtual environment::

  source $PYTHON_VENV/bin/activate

To exit virtual environment::

  deactivate

Once Python virtual environment is activated, you can perform quick installation or installation from source described above.
Take into consideration that you must not attempt to install YDK as root user under virtual environment.

Quick Bundle Installation
=========================

You can install the latest model packages from the Python package index.  Note that, in some systems, you need to install the new package as root.
You get a fully operational YDK environment by installing the `cisco-ios-xr` and/or `cisco-ios-xe` bundle(s) (depending on whether you're developing for an IOS XR or IOS XE platform),
which automatically installs all other dependent packages (`openconfig` and `ietf` packages)::

  pip install ydk-models-cisco-ios-xr
  pip install ydk-models-cisco-ios-xe

Alternatively, you can perform a partial installation.  If you only want to install the `openconfig` bundle and its dependencies (`ydk` and `ietf` packages), execute::

  pip install ydk-models-openconfig

If you only want to install the `ietf` bundle and its dependencies (`ydk` package), execute::

  pip install ydk-models-ietf

Installing from Source
======================

If you prefer not to use the YDK packages from the Python package index,
you have to install manually the `ydk` core package first, and then the model bundles you plan to use.
It is recommended to use `ydk-gen/install_ydk.sh` script in order to install the core components::

  # Clone ydk-gen from GitHub
  git clone https://github.com/ygorelik/ydk-gen.git
  cd ydk-gen

  # Define optional environment variables and install dependencies
  export YDKGEN_HOME=`pwd`
  export PYTHON_VENV=$HOME/ydk_venv
  ./install_ydk.sh -v   # also builds Python virtual environment


Once you have installed the `ydk` core package, you can install one or more model bundles.  Note that some bundles have dependencies on other bundles.
Those dependencies are already captured in the bundle package.  Make sure you install the desired bundles in the order below.
To install the `ietf` bundle from `ydk-gen` execute::

  # Activate Python virtual environment and navigate to ydk-gen directory
  source $PYTHON_VENV/bin/activate
  cd ydk-gen
  # Generate and install the bundle
  python3 generate.py -i --bundle profiles/bundles/ietf_0_1_5_post2.json

To install the `openconfig` bundle, execute::

  # Navigate to ydk-gen directory and activate runtime environment, if applicable
  source $PYTHON_VENV/bin/activate
  cd ydk-gen
  # Generate and install the bundle
  python3 generate.py -i --bundle profiles/bundles/openconfig_0_1_8.json


To install the `cisco-ios-xr` bundle, execute::

  # Activate Python virtual environment and navigate to ydk-gen directory
  source $PYTHON_VENV/bin/activate
  cd ydk-gen
  # Generate and install the bundle
  python3 generate.py -i --bundle profiles/bundles/cisco-ios-xr-6_6_3_post1.json


Documentation and Support
=========================

Available resources:

- Read the `API documentation <http://ydk.cisco.com/py/docs>`_ (release 0.8.3) for details on how to use the API and specific models
- Check `GitHub Pages <https://ygorelik.github.io/ydk-gen>`_ for the latest YDK release documentation
- Find some app samples in the `samples directory <https://github.com/CiscoDevNet/ydk-py/tree/master/core/samples>`_
- Find hundreds of additional samples in the `YDK-PY samples repository <https://github.com/CiscoDevNet/ydk-py-samples>`_
- Join the `YDK community <https://communities.cisco.com/community/developer/ydk>`_ to connect with YDK users and developers

Release Notes
=============

The current YDK release version is 0.8.6.3.

YDK is licensed under the Apache 2.0 License.
