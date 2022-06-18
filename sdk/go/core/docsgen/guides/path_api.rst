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

.. _howto-path:

.. _path-api-guide:

How do I use the Path API?
==========================

.. contents:: Table of Contents

The :ref:`Path API<path-api-guide>` (part of the `YDK core <https://gitlab.com/yangorelik/ydk-gen/tree/master/sdk/go/core>`_)
is a generic API which can be used to create and access YANG data nodes without having to use the model bundle APIs.
Applications can be written using xpath-like expressions as illustrated below.


Path Syntax
-----------

Full XPath notation is supported for find operations on :go:struct:`DataNode<DataNode>`\(s\).
This XPath conforms to the YANG specification \(`RFC 6020 section 6.4 <https://tools.ietf.org/html/rfc6020#section-6.4>`_\).
Some useful examples:

- Get `list` element with `key1` of value `1` and `key2` of value `2` \(this can return more `list` instances if there are more keys than `key1` and `key2`\)

.. code-block:: bash

    /module-name:container/list[key1='1'][key2='2']

- Get `leaf-list` instance with the value `val`

.. code-block:: bash

    /module-name:container/leaf-list[.='val']

- Get `aug-leaf`, which was added to `module-name` from an augment module `augment-module`

.. code-block:: bash

    /module-name:container/container2/augment-module:aug-cont/aug-leaf

A very small subset of this full XPath is recognized by :go:func:`DataNodeCreate<DataNodeCreate>`. Basically, only a relative or absolute path can be specified to identify a new data node. However, lists must be identified by all their keys and created with all of them, so for those cases predicates are allowed. Predicates must be ordered the way the keys are ordered and all the keys must be specified. Every predicate includes a single key with its value. Optionally, leaves and leaf-lists can have predicates specifying their value in the path itself. All these paths are valid XPath expressions. Example: (Relative to Root Data or :go:struct:`RootSchemaNode`)

.. code-block:: bash

    ietf-yang-library:modules-state/module[name='ietf-yang-library'][revision='']/conformance[.='implement']

Almost the same XPath is accepted by :go:struct:`SchemaNode<SchemaNode>` methods. The difference is that it is not used on data, but schema, which means there are no key values and only one node matches one path. In effect, lists do not have to have any predicates. If they do, they do not need to have all the keys specified and if values are included, they are ignored. Nevertheless, any such expression is still a valid XPath, but can return more nodes if executed on a data tree. Examples (all returning the same node):

.. code-block:: bash

    ietf-yang-library:modules-state/module/submodules
    ietf-yang-library:modules-state/module[name]/submodules
    ietf-yang-library:modules-state/module[name][revision]/submodules
    ietf-yang-library:modules-state/module[name='ietf-yang-library'][revision]/submodules


.. note::

    In all cases the node's prefix is specified as the name of the appropriate YANG schema.
    Any node can be prefixed by the module name. However, if the prefix is omitted, the module name is inherited
    from the previous (parent) node. It means, that the first node in the path is always supposed to have a prefix.

Example of Path API with Netconf Session
----------------------------------------

This Path API example uses :go:struct:`NetconfSession<ydk/path/NetconfSession>` to connect and communicate with Netconf server.
It is also using openconfig-bgp.yang model to build BGP configuration on a router.

.. code-block:: c
   :linenos:

    package main

    import (
        "fmt"
        "github.com/CiscoDevNet/ydk-go/ydk"
        "github.com/CiscoDevNet/ydk-go/ydk/path"
        "github.com/CiscoDevNet/ydk-go/ydk/types"
        encoding "github.com/CiscoDevNet/ydk-go/ydk/types/encoding_format"
    )

    type PathApiTest struct {
        Session    path.NetconfSession
        RootSchema types.RootSchemaNode
    }

    func (suite *PathApiTest) Setup() {
        suite.Session = path.NetconfSession{
        Address:  "127.0.0.1",
        Username: "admin",
        Password: "admin",
        Port:     12022}
        suite.Session.Connect()
        suite.RootSchema = suite.Session.GetRootSchemaNode()
    }

    func (suite *PathApiTest) TearDown() {
        suite.Session.Disconnect()
    }

    func (suite *PathApiTest) TestBgpConfig() {
        // Delete BGP config
        bgp := path.CreateRootDataNode( suite.RootSchema, "openconfig-bgp:bgp")
        deleteRpc := path.CreateRpc( suite.RootSchema, "ydk:delete")
        path.CreateDataNode( deleteRpc.Input, "entity", path.CodecEncode( bgp, encoding.XML, true))
        suite.Session.ExecuteRpc(deleteRpc)

        // Greate BGP config
        bgp = path.CreateRootDataNode( suite.RootSchema, "openconfig-bgp:bgp")
        path.CreateDataNode( bgp, "global/config/as", 65172)
        path.CreateDataNode( bgp, "global/config/router-id", "1.2.3.4")
        neighbor := path.CreateDataNode( bgp, "neighbors/neighbor[neighbor-address='172.16.255.2']", "")
        path.CreateDataNode( neighbor, "config/neighbor-address", "172.16.255.2")
        path.CreateDataNode( neighbor, "config/peer-as","65172")

        createRpc := path.CreateRpc( suite.RootSchema, "ydk:create")
        path.CreateDataNode( createRpc.Input, "entity", path.CodecEncode( bgp, encoding.XML, true))
        suite.Session.ExecuteRpc(createRpc)

        // Read BGP config
        bgp = path.CreateRootDataNode( suite.RootSchema, "openconfig-bgp:bgp")
        readRpc := path.CreateRpc( suite.RootSchema, "ydk:read")
        path.CreateDataNode( readRpc.Input, "filter", path.CodecEncode( bgp, encoding.XML, true))
        path.CreateDataNode( readRpc.Input, "only-config", "")
        result := suite.Session.ExecuteRpc(readRpc)

        config := path.CodecEncode( result, encoding.XML, true)
        ydk.YLogInfo("Got BGP config:\n" + config)

        // Delete BGP config
        suite.Session.ExecuteRpc(deleteRpc)
    }

    func main() {
        ydk.EnableLogging(ydk.Info)
        suite := PathApiTest{}
        suite.Setup()
        suite.TestBgpConfig()
        suite.TearDown()
    }
