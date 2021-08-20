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

NetconfSession
==============


.. cpp:class:: ydk::path::NetconfSession : public path::Session

    Implementation of :cpp:class:`Session<Session>` for the `Netconf <https://tools.ietf.org/html/rfc6241>`_ protocol.

    .. cpp:function:: NetconfSession(\
        const std::string& address, \
        const std::string& username, \
        const std::string& password, \
        int port = 830, \
        const std::string& protocol = "ssh", \
        bool on_demand = true, \
        bool common_cache = false, \
        int timeout = -1)

        Constructs an instance of the `NetconfSession` to connect to a server which **has** to support model download.

        :param address: IP address of the device supporting a Netconf interface.
        :param username: Username to log in to the device.
        :param password: Password to log in to the device.
        :param port: Device port used to access the Netconf interface. Default value is 830.
        :param on_demand: Enable on demand downloading by default.
        :param common_cache: Use different directories for different connections by default.
        :param timeout: The timeout in microseconds, -1 for infinite timeout, 0 for non-blocking.

    .. cpp:function:: NetconfSession(\
        const path::Repository& repo, \
        const std::string& address, \
        const std::string& username, \
        const std::string& password, \
        int port = 830, \
        const std::string& protocol = "ssh", \
        bool on_demand = true, \
        int timeout = -1)

        Constructs an instance of the `NetconfSession` using the provided :cpp:class:`Repository<Repository>`.

        :param repo: Reference to an instance of :cpp:class:`Repository<Repository>`.
        :param address: IP address of the device supporting a Netconf interface.
        :param username: Username to log in to the device.
        :param password: Password to log in to the device.
        :param port: Device port used to access the Netconf interface. Default value is 830.
        :param protocol: supported string values are "ssh" and "tcp".
        :param on_demand: Enable on demand downloading by default.
        :param timeout: The timeout in microseconds, -1 for infinite timeout, 0 for non-blocking.

    .. cpp:function:: NetconfSession(\
        const std::string& address, \
        const std::string& username, \
        const std::string& private_key_path, \
        const std::string& public_key_path, \
        int port = 830, \
        bool on_demand = true, \
        bool common_cache = false, \
        int timeout = -1)

        Constructs an instance of the `NetconfSession` to connect to a server which **has** to support model download.

        :param address: IP address of the device supporting a Netconf interface.
        :param username: Username to log in to the device.
        :param private_key_path: Path to private key file.
        :param public_key_path: Path to public key file.
        :param port: Device port used to access the Netconf interface. Default value is 830.
        :param on_demand: Enable on demand downloading by default.
        :param common_cache: Use different directories for different connections by default.
        :param timeout: The timeout in microseconds, -1 for infinite timeout, 0 for non-blocking.

    .. cpp:function:: NetconfSession(\
        const path::Repository& repo, \
        const std::string& address, \
        const std::string& username, \
        const std::string& private_key_path, \
        const std::string& public_key_path, \
        int port = 830, \
        bool on_demand = true, \
        int timeout = -1)

        Constructs an instance of the `NetconfSession` using the provided :cpp:class:`Repository<Repository>`.

        :param repo: Reference to an instance of :cpp:class:`Repository<Repository>`.
        :param address: IP address of the device supporting a Netconf interface.
        :param username: Username to log in to the device.
        :param private_key_path: Path to private key file.
        :param public_key_path: Path to public key file.
        :param port: Device port used to access the Netconf interface. Default value is 830.
        :param on_demand: Enable on demand downloading by default.
        :param timeout: The timeout in microseconds, -1 for infinite timeout, 0 for non-blocking.

    .. cpp:function:: path::RootSchemaNode& get_root_schema() const

        Returns the :cpp:class:`RootSchemaNode<path::RootSchemaNode>` tree supported by this instance of the `NetconfSession`.

        :return: Pointer to the :cpp:class:`RootSchemaNode<path::RootSchemaNode>` or `nullptr` if one could not be created.

    .. cpp:function:: std::shared_ptr<path::DataNode> invoke(path::Rpc& rpc) const

        Invokes or executes the given RPC and returns a :cpp:class:`DataNode<DataNode>` pointer if the Rpc has an output modelled in YANG.

        :param rpc: Reference to the :cpp:class:`Rpc<Rpc>` node.
        :return: Shared pointer to the :cpp:class:`DataNode<DataNode>` representing the output.

    .. cpp:function:: std::shared_ptr<path::DataNode> invoke(path::DataNode& datanode) const

        Invokes or executes the given DataNode containing a YANG 1.1 action and returns a :cpp:class:`DataNode<DataNode>` pointer,
        if the action has an output modeled in YANG.

        :param datanode: Reference to the :cpp:class:`DataNode<DataNode>` node.
        :return: Pointer to the :cpp:class:`DataNode<DataNode>` representing the output.

    .. cpp:function:: std::string execute_netconf_operation(path::Rpc& rpc) const

        Sends the specified RPC to device (similar to `invoke` function) and returns device response in XML encoded string.

        :param rpc: Reference to the :cpp:class:`Rpc<Rpc>` node.
        :return: std::string, which represents the RPC output.

    .. cpp:function:: std::vector<std::string> get_capabilities() const

        Gets string representation of the Netconf server's capabilities.

        :return: A vector of ``std::string`` representing the Netconf server capabilities.
