<!---
# *************************************************************
#  YDK-YANG Development Kit
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
-->
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6e111527081b48e1b2252c3562e08a3b)](https://www.codacy.com/app/ydk/ydk-gen?utm_source=github.com&utm_medium=referral&utm_content=CiscoDevNet/ydk-gen&utm_campaign=badger)
[![License](https://cloud.githubusercontent.com/assets/17089095/19458582/dd626d2c-9481-11e6-8019-8227c5c66a06.png)](https://github.com/CiscoDevNet/ydk-gen/blob/master/LICENSE) [![Build Status](https://travis-ci.org/CiscoDevNet/ydk-gen.svg?branch=master)](https://travis-ci.org/CiscoDevNet/ydk-gen)
[![codecov](https://codecov.io/gh/CiscoDevNet/ydk-gen/branch/master/graph/badge.svg)](https://codecov.io/gh/CiscoDevNet/ydk-gen)
[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)](https://hub.docker.com/r/ydkdev/ydk-gen/)

![ydk-logo-128](https://cloud.githubusercontent.com/assets/16885441/24175899/2010f51e-0e56-11e7-8fb7-30a9f70fbb86.png)

YANG Development Kit
====================

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Overview](#overview)
- [Backward compatibility](#backward-compatibility)
- [Docker](#docker)
- [System requirements](#system-requirements)
- [Core Installation](#core-installation)
  - [Installation Script](#installation-script)
  - [Building from Source](#building-from-source)
  - [Adding gNMI Service](#adding-gnmi-service)
- [Generate YDK components](#generate-ydk-components)
  - [Generate deployment packages](#generate-deployment-packages)
  - [Build model bundle profile](#build-model-bundle-profile)
  - [Generate and install model bundle](#generate-and-install-model-bundle)
  - [Writing your first app](#writing-your-first-app)
  - [Documentation](#documentation)
- [Generating an "Adhoc" YDK-Py Bundle](#generating-an-adhoc-ydk-py-bundle)
- [Notes](#notes)
  - [Python Requirements](#python-requirements)
  - [C++ Requirements](#c-requirements)
  - [Directory structure](#directory-structure)
  - [Troubleshooting](#troubleshooting)
- [Running Unit Tests](#running-unit-tests)
  - [Python](#python)
  - [C++](#c)
  - [Go](#go)
- [Support](#support)
- [Release Notes](#release-notes)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Overview

**YDK** is a developer tool that allows generate YANG model API's in multiple languages and provides services
to apply generated API over multiple communication protocols.
Currently supported languages are: Python, Go and C++.
Currently implemented protocols are: Netconf, Restconf, OpenDaylight and gNMI.
YDK provides CRUD and protocol specific services over above protocols.
YDK also provides codec services to translate API models to/from XML and JSON encoded strings.

Other tools and libraries are used to deliver `YDK` functionality:
* YANG model analysis and code generation is implemented using APIs from the [pyang](https://github.com/mbj4668/pyang) library
* Documentation is generated using [Sphinx](http://www.sphinx-doc.org/en/stable/)
* Runtime YANG model analysis is done using [libyang](https://github.com/CESNET/libyang)
* C++ to python bindings are created using [pybind11](https://github.com/pybind/pybind11)
* C++ uses [catch](https://github.com/catchorg/Catch2) and [spdlog](https://github.com/gabime/spdlog) for tests and logging respectively

The output of ydk-gen is either a core package, that defines main services and providers,
or add-on service package like gNMI Service, or a module bundle, consisting of programming language APIs derived from YANG models.
Each module bundle is generated using a bundle profile and the ydk-gen tool.
Developers can either use pre-packaged generated bundles (e.g. [ydk-py](http://cs.co/ydk-py)),
or define their own bundle, consisting of a set of YANG models, using a bundle profile
(e.g. [`ietf_0_1_1.json`](profiles/bundles/ietf_0_1_1.json)).
This gives the developer an ability to customize scope of their bundle based on their requirements.


# Backward compatibility

Although YDK-0.9.0 API is mostly the same as in previous YDK releases, it generates different code and model API comparing to YDK-0.8.5.
The YDK-0.9.0 generated code is not compatible with YDK-0.8.5 and earlier bundle packages due to changes Entity and YLeaf class objects.

**NOTE.** Starting from release 0.8.5 the YDK does not support Python2 interpreter as it was deprecated.

# Docker

A [docker image](https://docs.docker.com/engine/reference/run/) is automatically built with the latest ydk-gen commit.
This docker can be used to run ydk-gen without installing anything natively on your machine.

To use the docker image, [install docker](https://docs.docker.com/install/) on your system and run the below command.
See the [docker documentation](https://docs.docker.com/engine/reference/run/) for more details.

```
docker run -it ydksolutions/ydk-gen
```

# System requirements

The YDK is currently supported on the following platforms:
 - Linux Ubuntu Xenial (16.04 LTS), Bionic (18.04 LTS), and Focal (20.04 LTS)
 - Linux CentOS/RHEL versions 7 and 8
 - MacOS up to 10.14.6 (Mojave)

On supported platforms the YDK can be installed using [installation script](#installation-script).
On other platforms the YDK should be installed manually [from source](#building-from-source).
For both the methods the user must install `git` package prior to  the installation procedure.

All YDK core components are built using C and C++ compilers, which are default for the supported platform.
Corresponding libraries and header files are installed in default locations,
which are `/usr/local/lib`, `/usr/local/bin` and `/usr/local/include`.
Therefore the user must have sudo access in order to install YDK core components to these locations.

# Core Installation

## Installation Script

For YDK installation it is recommended to use script `install_ydk.sh` from `ydk-gen` git repository.
The script detects platform OS, installs all the dependencies and builds complete set of YDK components for specified language.
The user must have sudo access to these locations.

The YDK extensively uses Python scripts for building its components and model API packages (bundles).
In order to isolate YDK Python environment from system installation, the script builds Python3 virtual environment.
The user must manually activate virtual environment when generating model bundles and/or running YDK based application.
By default the Python virtual environment is installed under `$HOME/venv` directory.
If user has different location, the PYTHON_VENV environment variable should be set to that location.

Here is simple example of core YDK installation for Python programming language:

```
git clone https://github.com/ygorelik/ydk-gen.git
cd ydk-gen
export YDKGEN_HOME=`pwd`  # optional
export PYTHON_VENV=$HOME/ydk_vne  # optional
./install_ydk.sh --core
```

The script also allows to install individual components like dependencies, core, and service packages
 for specified programming language or for all supported languages.
 Full set of script capabilities could be viewed like this:

```
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
```

If user environment is different from the default one (different Python installation or different
 location of libraries) then building from source method should be used.

## Building from Source

If user platform is supported one, it is recommended to use `ydk-gen` script `install_ydk.sh`, 
in order to install third party software dependencies.

```
# Clone ydk-gen from GitHub
git clone https://github.com/ygorelik/ydk-gen.git
cd ydk-gen

# Define optional environment variables and install dependencies
export YDKGEN_HOME=`pwd`  
export PYTHON_VENV=$HOME/ydk_venv
./install_ydk.sh   # also builds Python virtual environment

# Activate Python virtual environment
source $PYTHON_VENV/bin/activate

# Generate and install YDK core library
./generate.py -is --core --cpp

# For Python programming language add
./generate.py -i --core 

# For Go programming language add
./generate.py -i --core --go
```

## Adding gNMI Service

In order to enable YDK support for gNMI protocol, which is optional, the user need install third party software
 and YDK gNMI service package. 

### gNMI Service installation

Here is simple example how gNMI service package for Python could be added:

```
cd ydk-gen
./install_ydk.sh -l py --service gnmi
```

### Runtime environment

There is an open issue with gRPC on Centos/RHEL, which requires an extra step before running any YDK gNMI application.
See this issue on [GRPC GitHub](https://github.com/grpc/grpc/issues/10942#issuecomment-312565041) for details.
As a workaround, the YDK based application runtime environment must include setting of `LD_LIBRARY_PATH` variable:

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$YDKGEN_HOME/grpc/libs/opt:$YDKGEN_HOME/protobuf-3.5.0/src/.libs:/usr/local/lib64
```


# Generate YDK components

All the YDK components/packages can be generated by using Python script `generate.py`. To get all of its options run:

```
cd ydk-gen
./generate.py --help
usage: generate.py [-h] [-l] [--core] [--service SERVICE] [--bundle BUNDLE]
                   [--adhoc-bundle-name ADHOC_BUNDLE_NAME]
                   [--adhoc-bundle ADHOC_BUNDLE [ADHOC_BUNDLE ...]]
                   [--generate-meta] [--generate-doc] [--generate-tests]
                   [--output-directory OUTPUT_DIRECTORY] [--cached-output-dir]
                   [-p] [-c] [-g] [-v] [-o]

Generate YDK artifacts:

optional arguments:
  -h, --help            show this help message and exit
  -l, --libydk          Generate libydk core package
  --core                Generate and/or install core library
  --service SERVICE     Location of service profile JSON file
  --bundle BUNDLE       Location of bundle profile JSON file
  --adhoc-bundle-name ADHOC_BUNDLE_NAME
                        Name of the adhoc bundle
  --adhoc-bundle ADHOC_BUNDLE [ADHOC_BUNDLE ...]
                        Generate an SDK from a specified list of files
  --generate-meta       Generate meta-data for Python bundle
  --generate-doc        Generate documentation
  --generate-tests      Generate tests
  --output-directory OUTPUT_DIRECTORY
                        The output directory where the sdk will get created.
  --cached-output-dir   The output directory specified with --output-directory
                        includes a cache of previously generated gen-
                        api/<language> files under a directory called 'cache'.
                        To be used to generate docs for --core
  -p, --python          Generate Python SDK
  -c, --cpp             Generate C++ SDK
  -g, --go              Generate Go SDK
  -v, --verbose         Verbose mode
  -o, --one-class-per-module
                        Generate separate modules for each python class
                        corresponding to yang containers or lists.
```

The below steps specify how to use `generate.py` to generate YDK core, model bundle, and service packages. All these packages are available for Python, Go and C++ in corresponding github repositories: [ydk-py](https://github.com/CiscoDevNet/ydk-py),  [ydk-go](https://github.com/CiscoDevNet/ydk-go) and [ydk-cpp](https://github.com/CiscoDevNet/ydk-cpp).

The script [create_ydk_sdk_for_github.sh](create_ydk_sdk_for_github.sh) can be used to generate the `ydk-py`, `ydk-cpp` and `ydk-go` repositories after having generated all the bundles and core packages using `generate.py`.

## Generate deployment packages

First the core installation procedure must be executed. Refer to [Core Installation](#core-installation) section for details.

To create the `libydk` binary package run the below commands:

```
cd ydk-gen/gen-api/cpp/ydk/build
[sudo] make package
```

To create the `libydk_gnmi` binary package run the below commands:

```
cd ydk-gen/gen-api/cpp/ydk-service-gnmi/build
[sudo] make package
```

## Build model bundle profile

The first step in using ydk-gen is either using one of the already built [bundle profiles](https://github.com/CiscoDevNet/ydk-gen/tree/master/profiles/bundles) or constructing your own bundle profile, consisting of the YANG models you are interested to include into the bundle:

Construct a bundle profile file, such as [```ietf_0_1_1.json```](profiles/bundles/ietf_0_1_1.json) and specify its dependencies.

A sample bundle profile file is described below. The file is in a JSON format. The profile must define the `"name"`, `"version"` and `"description"` of the bundle, and then the `"core_version"`, which refers to [the version](https://github.com/CiscoDevNet/ydk-gen/releases) of the ydk core package that you want to use with this bundle.
The `"name"` of the bundle will form part of the installation path of the bundle.
All other attributes, like `"author"` and `"copyright"`, are optional and will not affect the bundle generation. 

```
{
    "name":"cisco-ios-xr",
    "version": "6.5.3",
    "core_version": "0.9.0",
    "author": "Cisco",
    "copyright": "Cisco",
    "description": "Cisco IOS-XR Native Models From Git",
```

The `"models"` section of the profile describes sources of YANG models. It could contain combination of elements:

- `"dir"` - list of **relative** directory paths containing YANG files
- `"file"` - list of **relative** YANG file paths
- `"git"` - git repository, where YANG files are located

The sample below shows the use of git sources only. Other examples can be found in `profiles` directory README.md.

Each `"git"` source must specify `"url"` - git repository URL, and `"commits"` list. The specified URL must allow the repository
to be cloned without user intervention. Each element in `"commits"` list can specify:

- `"commitid"` - optional specification of a commit ID in string format. If not specified the HEAD revision is assumed.
The further specified directories and files will be copied from the context of this commit.
- `"dir"` - optional list of **relative** directory paths within the git repository.
All `*.yang` files in specified directory **and any sub-directories** will be pulled into the generated bundle.
- `"file"` - optional list of **relative** `*.yang` file paths within the git repository.

Only directory examples are shown in this example.

```
    "models": {
        "git": [
            {
                "url": "https://github.com/YangModels/yang.git",
                "commits": [
                  {
                    "dir": [
                        "vendor/cisco/xr/653"
                    ]
                  }
                ]
            },
            {
                "url": "https://github.com/YangModels/yang.git",
                "commits": [
                  {
                    "commitid": "f6b4e2d59d4eedf31ae8b2fa3119468e4c38259c",
                    "dir": [
                        "experimental/openconfig/bgp",
                        "experimental/openconfig/policy"
                    ]
                  }
                ]
            }
        ]
    },
```

## Generate and install model bundle

Generate model bundle using a bundle profile and install it.

### For Python

Python virtual environment must be activated prior to these procedures

```
./generate.py --python --bundle profiles/bundles/<name-of-profile>.json
[sudo] pip install gen-api/python/<name-of-bundle>-bundle/dist/ydk*.tar.gz
```

or using installation options:

```
./generate.py --bundle profiles/bundles/<name-of-profile>.json -i
```

Check Python packages installed:

```
pip list | grep ydk
...

ydk (0.9.0.1)
ydk-models-<name-of-bundle> (0.5.1)
...
```

### For Go

```
export $GOPATH=/your-go-path-installation-directory
./generate.py --go --bundle profiles/bundles/<name-of-profile>.json -i
```

### For C++

```
./generate.py --cpp --bundle profiles/bundles/<name-of-profile>.json
cd gen-api/cpp/<name-of-bundle>-bundle/build
make
[sudo] make install
```

or using installation options:

```
./generate.py --cpp --bundle profiles/bundles/<name-of-profile>.json -i [-s]
```

## Writing your first app

Now, you can start creating apps based on the models in your bundle.
Assuming you have generated a python bundle, the models will be available for importing in your app under
`ydk.models.<name-of-your-bundle>`.
For examples, see [ydk-py-samples](https://github.com/CiscoDevNet/ydk-py-samples#a-hello-world-app) and
[C++ samples](sdk/cpp/samples).
Also refer to the [documentation for python](http://ydk.cisco.com/py/docs/developer_guide.html),
[Go](http://ydk.cisco.com/go/docs/developer_guide.html) and
[C++](http://ydk.cisco.com/cpp/docs/developer_guide.html).

## Documentation

In order to generate YDK core and bundles documentation, the `--generate-doc` option of `generate.py` script is used, while generating core package. Therefore the user should generate all the bundles without the `--generate-doc` option prior to the documentation generation.
For example, the below sequence of commands will generate the documentation for the three python bundles and the python core
(for C++, use `--cpp`; for Go, use `--go`).

**Note.** The documentation generation for bundles can take few hours due to their size.

```
./generate.py --python --bundle profiles/bundles/ietf_0_1_1.json
./generate.py --python --bundle profiles/bundles/openconfig_0_1_1.json
./generate.py --python --bundle profiles/bundles/cisco_ios_xr_6_1_1.json
./generate.py --python --core --generate-doc
```

If you have previously generated documentation using the `--cached-output-dir --output-directory <dir>` option,
 the add-on documentation generation time can be reduced. Adding cisco-ios-xr documentation as an example:

```
mkdir gen-api/cache
mv gen-api/python gen-api/cache

./generate.py --python --bundle profiles/bundles/cisco_ios_xr_6_6_3.json
./generate.py --python --core --generate-doc --output-directory gen-api --cached-output-dir
```

Pre-generated documentation is available on the web for [Python](http://ydk.cisco.com/py/docs/), [C++](http://ydk.cisco.com/cpp/docs/) and [Go](http://ydk.cisco.com/go/docs/).

# Generating an "Adhoc" YDK-Py Bundle

The ability to generate an adhoc bundle directly from the command line and without creating a bundle file can be done something like this:

```
./generate.py --adhoc-bundle-name test --adhoc-bundle \
    /opt/git-repos/clean-yang/vendor/cisco/xr/621/Cisco-IOS-XR-ipv4-bgp-oper*.yang \
    /opt/git-repos/clean-yang/vendor/cisco/xr/621/Cisco-IOS-XR-types.yang
    /opt/git-repos/clean-yang/vendor/cisco/xr/621/Cisco-IOS-XR-ipv4-bgp-datatypes.yang
```

When run in this way, we will generate a bundle that only contains the files specified with the `--adhoc-bundle` option, creating a `pip` package name by the `--adhoc-bundle-name`, with a version `0.1.0` and a dependency on the base IETF bundle. Note that **all** dependencies for the bundle must be listed, and the expectation is that this option will typically be used for generating point YDK-Py bundles for specific testing, the `--verbose` option is automatically enabled to quickly and easily let a user see if dependencies have been satisfied.

# Notes

## Python Requirements

Starting from release 0.8.5 YDK supports only Python3 version.  At least Python3.4 along with corresponding pip3 utility must be installed on your the system. It is also required for Python installation to include corresponding shared library. As example:

 - python3.5m - /usr/lib/x86_64-linux-gnu/libpython3.5m.so

Please follow [Core Installation](#core-installation) procedures to assure presence of shared Python libraries.

## C++ Requirements

In some OS configurations during YDK package installation the `cmake` fails to find C/C++ headers for installed YDK libraries.
In this case the header location must be specified explicitly:

```
export C_INCLUDE_PATH=/usr/local/include
export CPLUS_INCLUDE_PATH=/usr/local/include
```

## Directory structure

```
gen-api         - generated code and packages for core and bundles
                    - python (Python SDK)
                    - go (Go SDK)
                    - cpp (C++ SDK)

3d_party        - suplemental code for third party software
profiles        - profile files used during generation
sdk             - sdk core and stubs for python, go and cpp
test            - dependencies and unit test shell scripts
yang            - some yang models used for testing
ydkgen          - python code to extend generate.py script 

create_ydk_sdk_for_github.sh - convenience script to generate language specific repositories
generate_bundles.sh          - convinience script to generate core and bundle packages for deployment

generate.py     - script used to generate SDK for yang models
install_ydk.sh  - YDK core components installation script
requirements.txt- python dependencies used during installation
README          - installation and usage notes
```

## Troubleshooting

Sometimes, developers using ydk-gen may run across errors when generating a YDK bundle using generate.py with some yang models. If there are issues with the .json profile file being used, such errors will be easily evident. Other times, when the problem is not so evident, it is recommended to try running with the `[--verbose|-v]` flag, which may reveal syntax problems with the yang models being used. For example,

```
./generate.py --python --bundle profiles/bundles/ietf_0_1_1.json --verbose
```

Also, it may be a good idea to obtain a local copy of the yang models and compile them using `pyang` to ensure the validity of the models,
```
cd /path/to/yang/models
pyang *.yang
```

# Running Unit Tests

## Python

#### Install the core and bundle packages

After installing C++ core packages and activating Python virtual environment:

1. Install bundle package

    ```
    cd ydk-gen
    ./generate.py -i --core
    ./generate.py -i --bundle profiles/test/ydktest-cpp.json
    ```

2. Start confd

    ```
    source $HOME/confd/confdrc
    cd ydk-gen/sdk/cpp/core/tests/confd/ydktest
    make all
    make start
    ```

3. Run unit tests

    ```
    cd ydk-gen/sdk/python
    python test/test_sanity_types.py
    python test/test_sanity_levels.py
    python test/test_sanity_filters.py
    ```

## C++

1. Install the core and bundle packages

    ```
    cd ydk-gen
    ./generate.py -is --core --cpp
    ./generate.py -is --bundle profiles/test/ydktest-cpp.json --cpp
    ```

2. Run the core tests

    ```
    cd ydkgen/gen-api/cpp/ydk/build
    ./test/ydk_core_test
    ```

3. Start confd

    ```
    source $HOME/confd/confdrc
    cd ydk-gen/sdk/cpp/core/tests/confd/ydktest
    make all
    make start
    ```

4. Build and run bundle tests

    ```
    cd ydk-gen/sdk/cpp/tests
    mkdir build && cd build
    cmake .. && make
    ./ydk_bundle_test
    ```

## Go

Please refer [here](https://github.com/CiscoDevNet/ydk-gen/blob/master/sdk/go/core/README.md).

#### Support

Join the [YDK community](https://communities.cisco.com/community/developer/ydk) to connect with other users and with the makers of YDK.

#### Release Notes

The current YDK release version is 0.9.0. The version of the latest ydk-gen master branch is 0.9.0.
The ydk-gen is licensed under the Apache 2.0 License.
