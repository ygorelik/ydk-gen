/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2021 Yan Gorelik, YDK Solutions. All rights reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 ------------------------------------------------------------------*/

package test

import (
	"fmt"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/path"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	encoding "github.com/CiscoDevNet/ydk-go/ydk/types/encoding_format"
	"github.com/stretchr/testify/suite"
	"testing"
)

type PathApiTestSuite struct {
	suite.Suite
	Session    path.NetconfSession
	RootSchema types.RootSchemaNode
}

func (suite *PathApiTestSuite) SetupSuite() {
	suite.Session = path.NetconfSession{
		Address:  "127.0.0.1",
		Username: "admin",
		Password: "admin",
		Port:     12022}
	suite.Session.Connect()
	suite.RootSchema = suite.Session.GetRootSchemaNode()
}

func (suite *PathApiTestSuite) TearDownSuite() {
	suite.Session.Disconnect()
}

func (suite *PathApiTestSuite) BeforeTest(suiteName, testName string) {
	runner := path.CreateRootDataNode( suite.RootSchema, "ydktest-sanity:runner")
	payload := path.CodecEncode( runner, encoding.XML, false)

	deleteRpc := path.CreateRpc( suite.RootSchema, "ydk:delete")
	path.CreateDataNode( deleteRpc.Input, "entity", payload)
	suite.Session.ExecuteRpc(deleteRpc);

	fmt.Printf("%v: %v ...\n", suiteName, testName)
}

func (suite *PathApiTestSuite) TestBgpConfig() {
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
	suite.NotNil(result)
	config := path.CodecEncode( result, encoding.XML, true)
	// ydk.YLogInfo("Got BGP config:\n" + config)
	expected :=
`<bgp xmlns="http://openconfig.net/yang/bgp">
  <global>
    <config>
      <as>65172</as>
      <router-id>1.2.3.4</router-id>
    </config>
  </global>
  <neighbors>
    <neighbor>
      <neighbor-address>172.16.255.2</neighbor-address>
      <config>
        <neighbor-address>172.16.255.2</neighbor-address>
        <peer-as>65172</peer-as>
      </config>
    </neighbor>
  </neighbors>
</bgp>
`
	suite.Equal(expected, config)

	// Delete BGP config
	suite.Session.ExecuteRpc(deleteRpc)
}

func (suite *PathApiTestSuite) TestCapabilities() {
    capabilities := suite.Session.GetCapabilities()
    suite.True(len(capabilities) > 0)
    fmt.Printf("===== Capabilities (%d):\n", len(capabilities))
    for i := 0; i < 2; i++ {
        fmt.Println(capabilities[i])
    }
}

func TestPathApiTestSuite(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	suite.Run(t, new(PathApiTestSuite))
}

func TestRestconfSessionPathApi(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	_, callerFile, _, _ := runtime.Caller(0)
	executablePath := filepath.Dir(callerFile)
	repopath := executablePath + "/../../../cpp/core/tests/models"
	repo := types.Repository{Path: repopath}
	session := path.RestconfSession{Repo: repo, Address: "127.0.0.1", Username: "admin", Password: "admin", Port: 12306, Encoding: encoding.JSON}
	session.Connect()
	schema := session.GetRootSchemaNode()
	if schema.Private == nil {
		t.Error("Could not get root schema")
	}
	// check capabilities
	capabilities := session.GetCapabilities()
	fmt.Printf("===== Capabilities (%d):\n", len(capabilities))
	for i := 0; i < 2; i++ {
		fmt.Println(capabilities[i])
	}

	// first delete
	runner := path.CreateRootDataNode(schema, "ydktest-sanity:runner")

	deleteRpc := path.CreateRpc(schema, "ydk:delete")
	path.CreateDataNode(deleteRpc.Input, "entity", path.CodecEncode(runner, encoding.JSON, true))
	session.ExecuteRpc(deleteRpc)

	// config
	path.CreateDataNode(runner, "ytypes/built-in-t/number8", "3")
	json := path.CodecEncode(runner, encoding.JSON, true)

	createRpc := path.CreateRpc(schema, "ydk:create")
	path.CreateDataNode(createRpc.Input, "entity", path.CodecEncode(runner, encoding.JSON, true))
	session.ExecuteRpc(createRpc)

	// read and check result
	runnerRead := path.CreateRootDataNode(schema, "ydktest-sanity:runner")

	readRpc := path.CreateRpc(schema, "ydk:read")
	path.CreateDataNode(readRpc.Input, "filter", path.CodecEncode(runnerRead, encoding.JSON, true))
	path.CreateDataNode(readRpc.Input, "only-config", "")
	readRunner := session.ExecuteRpc(readRpc)
	if readRunner.Private == nil {
		t.Error("Unexpected nil for read RPC result")
	}
	json = path.CodecEncode(readRunner, encoding.JSON, false)
	if `{"ydktest-sanity:runner":{"ytypes":{"built-in-t":{"number8":3}}}}` != json {
		t.Error("Incorrect RPC read result")
	}

	// delete config
	session.ExecuteRpc(deleteRpc)

	session.Disconnect()
}
