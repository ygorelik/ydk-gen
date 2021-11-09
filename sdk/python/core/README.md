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

<!-- END doctoc generated TOC please keep comment here to allow auto update 

<a href="https://github.com/CiscoDevNet/ydk-py"><img src="https://cloud.githubusercontent.com/assets/17089095/14834057/2e1fe270-0bb7-11e6-9e94-73dd7d71e87d.png" height="240" width="240" ></a>
-->

# Overview

The YANG Development Kit (YDK) is a software development tool, which provides API for building applications based on YANG models.
The YDK allows generate YANG model API and provides services to apply generated API over various communication protocols.
Currently implemented protocols are: Netconf, Restconf, OpenDaylight and gNMI.
YDK provides CRUD and protocol specific services over above protocols.
YDK also provides codec services to translate API models to/from XML and JSON encoded strings.

# Installation

Create a source distribution for YDK:
```
    $ python setup.py sdist
```

Install YDK:
```
    $ pip install dist/ydk-*.tar.gz
```

