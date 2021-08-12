Netconf Session
===============

.. go:package:: ydk/path
    :synopsis:  Path API via Netconf

.. go:struct:: NetconfSession

	NetconfSession is an implementation of Session for the `NETCONF protocol <https://tools.ietf.org/html/rfc6241>`_.
	The sructure `NetconfSession` includes the following attributes:

	.. attribute:: Repo

		An instance of :go:struct:`Repository<ydk/types/Repository>`. This attribute represents the repository of YANG models.
		When not specified, the model repository path is set to `$USER/.ydk`.

	.. attribute:: Address

		A Go ``string`` that represents an IP address of the device supporting a Netconf protocol. This attribute
		must be set during initialization.

	.. attribute:: Username

		A Go ``string`` that represents a username to log in to the device. This attribute
		must be set during initialization.

	.. attribute:: Password

		A Go ``string`` that represents a password to log in to the device. This attribute
		must be set during initialization, when `ServerCert` is not set (non SSL connections).

	.. attribute:: Port

		An ``int`` that represents the device port number used to access the Netconf interface. Default value - 830.

	.. attribute:: Protocol

		A Go ``string`` that represents protocol used to connect to the device. The allowed values are `SSH` and `TCP`.
		When not specified, it is set to default value - `SSH`.

	.. attribute:: OnDemand

		A Go ``bool`` that defines how YANG modules are loaded from device to repository. Default value is `true`, meaning
		the YANG modules are loaded to repository on-demand.

	.. attribute:: CommonCache

		A Go ``bool`` that defines how repositories are used for different devices. Default value is `false`, which means
		different directories will be used for different connections. This attribute has meaning only when `Repo` is not defined.

	.. attribute:: Timeout

		A Go ``int`` that repesents allowed Netconf server response delay in seconds. Valid range is [1, 255]. If not set
		during initialization the value -1 is set by default, meaning the response delay is not limited.

	.. attribute:: ServerCert

		A Go ``string`` that represents full path to a file, which stores the Netconf server public key (server SSL certificate).
		This attribute must be set for SSL connection.

	.. attribute:: PrivateKey

		A Go ``string`` that represents full path to a file, which stores application platform private key.
		This attribute is optional and has meaning only when `ServerCert` is specified.

.. method:: (session *NetconfSession) Connect()

	Implementation of ServiceProvider interface. Connects to Netconf Server using Repo/Address/Username/Password/Port.

.. method:: (session *NetconfSession) Disconnect()

	Implementation of ServiceProvider interface. Disconnects from Netconf Server.

.. method:: (session *NetconfSession) GetState() *errors.State

	Implementation of ServiceProvider interface. Returns error state for the NetconfServiceProvider.

.. method:: (session *NetconfSession) ExecuteRpc(rpc types.Rpc) DataNode

	Sends RPC to Netconf server and gets response.

	:param rpc: :go:struct:`Rpc<ydk/types/Rpc>` to be sent to Netconf server.
	:rtype: `DataNode` - top level datanode of a tree hierarchy.

.. method:: (session *NetconfSession) GetCapabilities()

	Gets the capabilities supported by Netconf server.

	:return: The list of capabilities.
	:rtype: ``[]string``.
