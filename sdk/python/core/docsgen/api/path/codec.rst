..
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

Codec
=====

.. module:: ydk.path
    :synopsis: Path API Codec

.. py:class:: Codec

    YDK Path Codec provides encode and decode translations between string payload and :py:class:`DataNode<ydk.path.DataNode>`.

    .. py:method:: encode(data_node, encoding, pretty=True):

        Encodes data in `data_node` to string payload.

        :param data_node: (:py:class:`DataNode<ydk.path.DataNode>`) for single data node to encode.

              For multiple data nodes encapsulate :py:class:`DataNode<ydk.path.DataNode>` instances into Python ``list``.
        :param encoding: (:py:class:`EncodingFormat<ydk.types.EncodingFormat>`) Encoding format.
        :param pretty: (``bool``) Pretty format.
        :return: (``str``) encoded payload.
        :raises: ``RuntimeError`` with :py:exc:`YCodecError<ydk.errors.YCodecError>` prefix, if an error has occurred.

    .. py:method:: decode(root_schema_node, payload, encoding):

        Decodes payload string into :py:class:`DataNode<ydk.path.DataNode>` instance.

        :param root_schema_node: (:py:class:`RootSchemaNode<ydk.path.RootSchemaNode>`) An instance of `root_schema_node`.
        :param payload: (``str``) Payload to decode.
        :param encoding: (:py:class:`EncodingFormat<ydk.types.EncodingFormat>`) Encoding format.
        :return: (:py:class:`DataNode<ydk.path.DataNode>`) instance of a `data-node`.
        :raises: ``RuntimeError`` with :py:exc:`YCodecError<ydk.errors.YCodecError>` prefix, if an error has occurred.
