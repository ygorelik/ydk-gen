..
  # *************************************************************
  #  YDK - YANG Development Kit
  #  Copyright 2021 Yan Gorelik, YDK Solutions. All rights reserved
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

Restconf Session
================

.. go:package:: ydk/path
    :synopsis:  Path API via Restconf

.. go:struct:: RestconfSession

	The RestconfSession is an implementation of Session for the `Restconf protocol <https://tools.ietf.org/html/draft-ietf-netconf-restconf-18>`_.
	The sructure `RestconfSession` includes the following attributes:

	.. attribute:: Repo

		An instance of :go:struct:`Repository<ydk/types/Repository>`. This attribute
		must be set during initialization.

	.. attribute:: Address

		A Go ``string`` that represents an IP address of the device supporting a Restconf protocol. This attribute
		must be set during initialization.

	.. attribute:: Username

		A Go ``string`` that represents a username to log in to the device. This attribute
		must be set during initialization.

	.. attribute:: Password

		A Go ``string`` that represents a password to log in to the device. This attribute
		must be set during initialization.

	.. attribute:: Port

		A Go ``int`` that represents the web server port number, which is used to access the Restconf Server.
		Default value - 80.

	.. attribute:: Encoding

		A YDK type of :ref:`encoding-format-ydk` that represents encoding format of payload in the RPC. 
		When not specified the `JSON` formatting is assumed.

	.. attribute:: ConfigRoot

		A Go ``string`` that represents root of the URL path to configuration data.
		If not specified, it is set by default to "/data".

	.. attribute:: StateRoot

		A Go ``string`` that represents root of the URL path to state data.
		If not specified, it is set by default to "/data".

The sructure `RestconfSession` defines the following methods:

.. method:: Connect()

	Connects to Restconf Server using Repo/Address/Username/Password/Port.

.. method:: Disconnect()

	Disconnects from Restconf Server.

.. method:: GetState() *errors.State

	Returns error state for the RestconfSession.

.. method:: ExecuteRpc(rpc types.Rpc) DataNode

	Sends RPC to Restconf server and gets response.

	:param rpc: :go:struct:`Rpc<ydk/types/Rpc>` to be sent to Restconf server.
				The `rpc` values currently restricted to only YDK defined RPCs:
				"ydk:create", "ydk:read", "ydk:update", and "ydk:delete".
	:rtype: `DataNode` - top level datanode of a tree hierarchy.

.. method:: GetCapabilities()

	Gets the capabilities supported by Restconf server.

	:return: The list of capabilities.
	:rtype: ``[]string``.
