..
  #  YDK - YANG Development Kit
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

YDK Path API
============

.. go:package:: ydk/path
    :synopsis: YDK Path API

This package contains YDK Go Path API.

YDK Go provides a new interface in the form of Path API, which can be used to write apps using a generic API, using xpath-like path expression to create and access YANG data nodes. Internally, the nodes created using the YDK model API are converted to Path API data nodes for validation and encoding to respective protocol payloads.


.. toctree::
    :maxdepth: 2

    path.rst
    netconf_session.rst

