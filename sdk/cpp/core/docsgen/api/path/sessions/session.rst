..
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

Session
=======

.. cpp:class:: ydk::path::Session

    Abstract base class to model sessions.

    .. cpp:function:: virtual RootSchemaNode& get_root_schema() const

        Returns the :cpp:class:`RootSchemaNode<RootSchemaNode>` tree supported by this instance of the `Session`.

        :return: Reference to the :cpp:class:`RootSchemaNode<RootSchemaNode>` or `nullptr` if one could not be created.

    .. cpp:function:: virtual std::shared_ptr<path::DataNode> invoke(path::Rpc& rpc) const

        Invokes or executes the given rpc and returns a :cpp:class:`DataNode<DataNode>` pointer if the Rpc has an output modeled in YANG.

        :param rpc: Reference to the :cpp:class:`Rpc<Rpc>` node.
        :return: Pointer to the :cpp:class:`DataNode<DataNode>` representing the output.

    .. cpp:function:: virtual std::vector<std::string> get_capabilities() const

        Gets string representation of server's capabilities.

        :return: A vector of ``std::string`` representing the server capabilities.
