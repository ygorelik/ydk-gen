/*  ----------------------------------------------------------------
YDK - YANG Development Kit
Copyright 2017-2019 Cisco Systems. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-------------------------------------------------------------------
This file has been modified by Yan Gorelik, YDK Solutions.
All modifications in original under CiscoDevNet domain
introduced since October 2019 are copyrighted.
All rights reserved under Apache License, Version 2.0.
------------------------------------------------------------------*/

package path

import (
	"path/filepath"
	"runtime"
	"testing"

	"github.com/CiscoDevNet/ydk-go/ydk"
	oc_bgp "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/openconfig_bgp"
	"github.com/CiscoDevNet/ydk-go/ydk/providers"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	encoding "github.com/CiscoDevNet/ydk-go/ydk/types/encoding_format"
)

func TestExecuteRpc(t *testing.T) {
	ydk.EnableLogging(ydk.Info)
	provider := providers.NetconfServiceProvider{Address: "127.0.0.1", Username: "admin", Password: "admin", Port: 12022}
	provider.Connect()

	bgp := oc_bgp.Bgp{}
	data := make(map[string]string)
	result := provider.ExecuteRpc("create", &bgp, data)
	if result.Private == nil {
		t.Error("Operation failed")
	} else {
		provider.ExecuteRpc("delete", &bgp, data)
	}

	provider.Disconnect()
}

func TestNetconfSessionConnectNoRepo(t *testing.T) {
	ydk.EnableLogging(ydk.Info)
	session := NetconfSession{Address: "127.0.0.1", Username: "admin", Password: "admin", Port: 12022}
	session.Connect()

	rootSchema := session.GetRootSchemaNode()

	bgp := CreateRootDataNode(rootSchema, "openconfig-bgp:bgp")
	CreateDataNode(bgp, "global/config/as", 65172)
	bgpCreatePayload := CodecEncode(bgp, encoding.XML, false)
	ydk.YLogInfo("RPC Payload:\n" + bgpCreatePayload)

	createRpc := CreateRpc(rootSchema, "ydk:create")
	CreateDataNode(createRpc.Input, "entity", bgpCreatePayload)
	session.ExecuteRpc(createRpc)

	session.Disconnect()
}

func TestNetconfSessionConnectWithRepo(t *testing.T) {
	ydk.EnableLogging(ydk.Debug)
	_, callerFile, _, _ := runtime.Caller(0)
	executablePath := filepath.Dir(callerFile)
	repopath := executablePath + "/../../../../cpp/core/tests/models"
	repo := types.Repository{Path: repopath}
	session := NetconfSession{Repo: repo, Address: "127.0.0.1", Username: "admin", Password: "admin", Port: 12022}
	session.Connect()
	schema := session.GetRootSchemaNode()
	if schema.Private == nil {
		t.Error("Could not get root schema")
	}
	session.Disconnect()
}

func TestRestconfSessionConnect(t *testing.T) {
	ydk.EnableLogging(ydk.Debug)
	_, callerFile, _, _ := runtime.Caller(0)
	executablePath := filepath.Dir(callerFile)
	repopath := executablePath + "/../../../../cpp/core/tests/models"
	repo := types.Repository{Path: repopath}
	session := RestconfSession{Repo: repo, Address: "127.0.0.1", Username: "admin", Password: "admin", Port: 12306, Encoding: encoding.XML}
	session.Connect()
	schema := session.GetRootSchemaNode()
	if schema.Private == nil {
		t.Error("Could not get root schema")
	}
	session.Disconnect()
}
