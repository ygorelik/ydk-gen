# YDK C++ Samples

## Building Sample Apps

### 1. Build YDK C++ Core

Install C++ core library and needed dependencies by following [Core installation](https://github.com/CiscoDevNet/ydk-gen#core-installation).

### 2. Build Model Bundles

For sample applications you need build and install the _openconfig_ and _cisco_ios_xr_ bundles.
You can use existing profiles to build complete model API or use
[addhock](https://github.com/CiscoDevNet/ydk-gen#generating-an-adhoc-ydk-py-bundle) method to generate bundles with
limited number of YANG modules that are required to run sample applications. Here are examples that can be used
after initializing Python virtual environment:

**Openconfig bundle**
```
export REPO="/Users/ygorelik/yang-models/yang/vendor/cisco/xr/751"
cd ~/ydk-gen
python generate.py -is --cpp --adhoc-bundle-name openconfig --adhoc-bundle \
$REPO/openconfig-bgp.yang \
$REPO/openconfig-bgp-types.yang \
$REPO/openconfig-extensions.yang \
$REPO/openconfig-bgp-common.yang \
$REPO/openconfig-bgp-common-multiprotocol.yang \
$REPO/openconfig-bgp-common-structure.yang \
$REPO/openconfig-bgp-peer-group.yang \
$REPO/openconfig-bgp-neighbor.yang \
$REPO/openconfig-bgp-global.yang \
$REPO/openconfig-types.yang \
$REPO/openconfig-inet-types.yang \
$REPO/openconfig-routing-policy.yang \
$REPO/openconfig-yang-types.yang \
$REPO/openconfig-interfaces.yang \
$REPO/openconfig-policy-types.yang
```

**Cisco_ios_xr bundle**
```
export REPO="/Users/ygorelik/yang-models/yang/vendor/cisco/xr/751"
cd ~/ydk-gen
python generate.py -is --cpp --adhoc-bundle-name cisco_ios_xr --adhoc-bundle \
$REPO/Cisco-IOS-XR-ipv4-bgp-cfg.yang \
$REPO/Cisco-IOS-XR-types.yang \
$REPO/Cisco-IOS-XR-ipv4-bgp-datatypes.yang \
$REPO/cisco-semver.yang \
$REPO/Cisco-IOS-XR-infra-rsi-cfg.yang \
$REPO/Cisco-IOS-XR-snmp-agent-cfg.yang \
$REPO/Cisco-IOS-XR-ifmgr-cfg.yang \
$REPO/Cisco-IOS-XR-clns-isis-datatypes.yang \
$REPO/Cisco-IOS-XR-clns-isis-cfg.yang
```

### 3. Build the Sample Apps

From ydk-gen directory execute these commands:
```
cd sdk/cpp/samples
mkdir -p build && cd build
cmake ..
make
```

That will build the following apps:
```
(venv3.7) YGORELIK-M-C3GG:build ygorelik$ ls -l bgp_*
-rwxr-xr-x  1 ygorelik  staff  16552816 Jan  5 16:23 bgp_create
-rwxr-xr-x  1 ygorelik  staff  16403152 Jan  5 16:23 bgp_delete
-rwxr-xr-x  1 ygorelik  staff  16425752 Jan  5 16:23 bgp_read
-rwxr-xr-x  1 ygorelik  staff  17038472 Jan  5 16:24 bgp_routing_policy_create
-rwxr-xr-x  1 ygorelik  staff  16404152 Jan  5 16:23 bgp_update
-rwxr-xr-x  1 ygorelik  staff  19793312 Jan  5 16:24 bgp_xr_create
-rwxr-xr-x  1 ygorelik  staff  19544792 Jan  5 16:24 bgp_xr_delete
-rwxr-xr-x  1 ygorelik  staff  19549288 Jan  5 16:24 bgp_xr_read
-rwxr-xr-x  1 ygorelik  staff  17403440 Jan  5 16:49 isis_xr_create
-rwxr-xr-x  1 ygorelik  staff  17152904 Jan  5 16:27 isis_xr_delete
-rwxr-xr-x  1 ygorelik  staff  17172552 Jan  5 16:27 isis_xr_read
```

## Running Sample Apps

To run sample apps you need to have live or simulated router with enabled Netconf server. For test purposes it is
recommended to use _confd_ app, which was installed during core installation. The _confd_ can be initialized,
start and stop using test scripts:
```
cd ~ydk-gen
./test/init_test_env.sh   # this will initializa and start confd router simulator
./test/clean_test_env.sh  # this will stop the confd and clean test environment
```

Run any of the apps without parameters to see the usage info:
```
build ygorelik$ ./bgp_delete

Usage:
	./bgp_delete [http|ssh]://user:password@host[:port] [-v]
		If host is IPv6, enclose it in square brackets. E.g. [1234:1234:1234:1234::1234]
		If port is not specified, 830 will be used with ssh (netconf) or 80 with http (restconf)
```

All the apps have one required parameter, which specifies credentials for the router. The optional parameter `-v`
will turn on verbose mode, in which you will be able to see all sent and received RPCs.

Below are shown examples of output (partial) when running some of the samples on _confd_ router simulator.

**Create BGP configuration**
```
build ygorelik$ ./bgp_create ssh://admin:admin@127.0.0.1:12022 -v
...
[2023-01-04 10:19:59.693] [ydk] [info] Path where models are to be downloaded: /Users/ygorelik/.ydk/127.0.0.1
[2023-01-04 10:19:59.705] [ydk] [info] Connected to 127.0.0.1 on port 12022 using ssh with timeout of -1
[2023-01-04 10:19:59.706] [ydk] [info] Executing CRUD create operation on [openconfig-bgp:bgp]
[2023-01-04 10:19:59.706] [ydk] [info] Executing 'edit-config' RPC on [openconfig-bgp:bgp]
[2023-01-04 10:19:59.735] [ydk] [info] ============= Sending RPC to device =============
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <candidate/>
  </target>
  <config><bgp xmlns="http://openconfig.net/yang/bgp" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
  <global>
    <afi-safis>
      <afi-safi>
        <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:L3VPN_IPV4_UNICAST</afi-safi-name>
        <config>
          <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:L3VPN_IPV4_UNICAST</afi-safi-name>
          <enabled>false</enabled>
        </config>
      </afi-safi>
    </afi-safis>
    <config>
      <as>65172</as>
      <router-id>1.2.3.4</router-id>
    </config>
  </global>
  <neighbors>
    <neighbor>
      <neighbor-address>6.7.8.9</neighbor-address>
      <config>
        <peer-group>IBGP</peer-group>
        <neighbor-address>6.7.8.9</neighbor-address>
        <peer-as>65001</peer-as>
        <local-as>65001</local-as>
      </config>
    </neighbor>
  </neighbors>
  <peer-groups>
    <peer-group>
      <peer-group-name>IBGP</peer-group-name>
      <config>
        <peer-group-name>IBGP</peer-group-name>
        <peer-as>65001</peer-as>
        <local-as>65001</local-as>
        <description>test description</description>
      </config>
    </peer-group>
  </peer-groups>
</bgp>
</config>
</edit-config>
</rpc>
[2023-01-04 10:19:59.744] [ydk] [info] ============= Received RPC from device =============
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="2">
  <ok/>
</rpc-reply>

[2023-01-04 10:19:59.745] [ydk] [info] Executing 'commit' RPC
[2023-01-04 10:19:59.745] [ydk] [info] ============= Sending RPC to device =============
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>
</rpc>
[2023-01-04 10:19:59.768] [ydk] [info] ============= Received RPC from device =============
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="3">
  <ok/>
</rpc-reply>

[2023-01-04 10:19:59.768] [ydk] [info] Operation succeeded
Create yfilter success

[2023-01-04 10:19:59.769] [ydk] [info] Disconnected from device
```

**Read BGP configuration**
```
build ygorelik$ ./bgp_read ssh://admin:admin@127.0.0.1:12022 -v
...
[2023-01-04 10:21:13.682] [ydk] [info] Path where models are to be downloaded: /Users/ygorelik/.ydk/127.0.0.1
[2023-01-04 10:21:13.692] [ydk] [info] Connected to 127.0.0.1 on port 12022 using ssh with timeout of -1
[2023-01-04 10:21:13.692] [ydk] [info] Executing CRUD read_config operation on [openconfig-bgp:bgp]
[2023-01-04 10:21:13.692] [ydk] [info] Executing 'get' RPC on [openconfig-bgp:bgp] from running
[2023-01-04 10:21:13.715] [ydk] [info] ============= Sending RPC to device =============
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter><bgp xmlns="http://openconfig.net/yang/bgp"/></filter>
</get-config>
</rpc>
[2023-01-04 10:21:13.720] [ydk] [info] ============= Received RPC from device =============
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="2">
  <data>
    <bgp xmlns="http://openconfig.net/yang/bgp">
      <global>
        <config>
          <as>65172</as>
          <router-id>1.2.3.4</router-id>
        </config>
        <afi-safis>
          <afi-safi>
            <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:L3VPN_IPV4_UNICAST</afi-safi-name>
            <config>
              <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:L3VPN_IPV4_UNICAST</afi-safi-name>
              <enabled>false</enabled>
            </config>
          </afi-safi>
        </afi-safis>
      </global>
      <neighbors>
        <neighbor>
          <neighbor-address>6.7.8.9</neighbor-address>
          <config>
            <peer-group>IBGP</peer-group>
            <neighbor-address>6.7.8.9</neighbor-address>
            <peer-as>65001</peer-as>
            <local-as>65001</local-as>
          </config>
        </neighbor>
      </neighbors>
      <peer-groups>
        <peer-group>
          <peer-group-name>IBGP</peer-group-name>
          <config>
            <peer-group-name>IBGP</peer-group-name>
            <peer-as>65001</peer-as>
            <local-as>65001</local-as>
            <description>test description</description>
          </config>
        </peer-group>
      </peer-groups>
    </bgp>
  </data>
</rpc-reply>

==================================================
BGP configuration: 

AS: 65172
Router ID: 1.2.3.4

Neighbor address: 6.7.8.9
Neighbor local AS: 65001
Neighbor peer group: IBGP
Neighbor peer type: 

AFI-SAFI name: openconfig-bgp-types:L3VPN_IPV4_UNICAST
AFI-SAFI config name: openconfig-bgp-types:L3VPN_IPV4_UNICAST
AFI-SAFI enabled: false

Peer group name: IBGP
Peer group type: 

==================================================

[2023-01-04 10:21:13.721] [ydk] [info] Disconnected from device
```

**Delete BGP configuration**
```
build ygorelik$ ./bgp_delete ssh://admin:admin@127.0.0.1:12022 -v
...
[2023-01-04 10:14:43.478] [ydk] [info] Path where models are to be downloaded: /Users/ygorelik/.ydk/127.0.0.1
[2023-01-04 10:14:43.488] [ydk] [info] Connected to 127.0.0.1 on port 12022 using ssh with timeout of -1
[2023-01-04 10:14:43.488] [ydk] [info] Executing CRUD delete operation on [openconfig-bgp:bgp]
[2023-01-04 10:14:43.488] [ydk] [info] Executing 'edit-config' RPC on [openconfig-bgp:bgp]
[2023-01-04 10:14:43.511] [ydk] [info] ============= Sending RPC to device =============
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <candidate/>
  </target>
  <config><bgp xmlns="http://openconfig.net/yang/bgp" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
</config>
</edit-config>
</rpc>
[2023-01-04 10:14:43.515] [ydk] [info] ============= Received RPC from device =============
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="2">
  <ok/>
</rpc-reply>

[2023-01-04 10:14:43.515] [ydk] [info] Executing 'commit' RPC
[2023-01-04 10:14:43.515] [ydk] [info] ============= Sending RPC to device =============
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>
</rpc>
[2023-01-04 10:14:43.527] [ydk] [info] ============= Received RPC from device =============
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="3">
  <ok/>
</rpc-reply>

[2023-01-04 10:14:43.527] [ydk] [info] Operation succeeded
Delete yfilter success
[2023-01-04 10:14:43.527] [ydk] [info] Disconnected from device
```
