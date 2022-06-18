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

RestconfSession
===============

.. module:: ydk.path
    :synopsis: RestconfSession


.. py:class:: RestconfSession(\
            repo, address, username, password, port=80, \
            encoding=EncodingFormat.JSON, \
            config_url_root="/data", state_url_root="/data")

        :param repo: (:py:class:`Repository`) Defines location of YANG model repository.
        :param address: (``str``) IP address or DNC name of the device supporting Netconf interface.
        :param username: (``str``) Username to log in to the device.
        :param password: (``str``) Password to log in to the device.
        :param port: (``int``) Type of encoding to be used for the payload. Default is 80.
        :param encoding: (:py:class:`EncodingFormat<ydk.types.EncodingFormat>`) Encoding Format, default is :py:attr:`JSON<ydk.types.EncodingFormat.JSON>`.
        :param config_url_root: (``str``) To provider backwards compatibility with older drafts of Restconf RFC, this can be "/config" or "/data" (which is the default).
        :param state_url_root: (``str``) To provider backwards compatibility with older drafts of Restconf RFC, this can be "/operational" or "/data" (which is the default)

    .. py:method:: get_root_schema()

        Returns the :py:class:`RootSchemaNode<RootSchemaNode>` tree supported by this instance of the :py:class:`RestconfSession<RestconfSession>`.

        :returns: Pointer to the :py:class:`RootSchemaNode<RootSchemaNode>` or ``None``, if one was not created.

    .. py:method:: invoke(rpc)

        Invokes or executes the given rpc and returns a :py:class:`DataNode<DataNode>` pointer if the :py:class:`Rpc<Rpc>` has an output modelled in YANG.

        :param rpc: (:py:class:`Rpc<Rpc>`)
        :returns: Pointer to the :py:class:`DataNode<DataNode>` representing the output.

    .. py:method:: get_capabilities()

        Returns a list of capabilities for the Restconf server.

        :returns: A list of ``str`` representing the Restconf server capabilities.
