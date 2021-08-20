/* ----------------------------------------------------------------------
 YANG Development Kit
 Package path implements support for Netconf Session in Go.

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
 --------------------------------------------------------------------- */

package path

// #include <ydk/ydk.h>
// #include <stdlib.h>
import "C"

import (
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/errors"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	"unsafe"
)

// NetconfSession declaration and methods
//
type NetconfSession struct {
	Repo        types.Repository
	Address     string
	Username    string
	Password    string
	Port        int
	Protocol    string
	OnDemand    bool
	CommonCache bool
	Timeout     int
	ServerCert  string
	PrivateKey  string

	Private     interface{}
	State       errors.State
}

// Connect to Netconf Session
func (ns *NetconfSession) Connect() {

	var caddress *C.char = C.CString(ns.Address)
	defer C.free(unsafe.Pointer(caddress))

	var cport C.int = C.int(ns.Port)
	if ns.Timeout == 0 {
		ns.Timeout = -1
	}
	var ctimeout C.int = C.int(ns.Timeout)

	var cprotocol *C.char = C.CString(ns.Protocol)
	defer C.free(unsafe.Pointer(cprotocol))

	var cOnDemand C.boolean = 1
	if ns.OnDemand { cOnDemand = 0 }
	var cCommonCache C.boolean = 0
	if ns.CommonCache { cCommonCache = 1 }

	var cserver *C.char = C.CString(ns.ServerCert)
	defer C.free(unsafe.Pointer(cserver))
	var cclient *C.char = C.CString(ns.PrivateKey)
	defer C.free(unsafe.Pointer(cclient))

	var cusername *C.char = C.CString(ns.Username)
	defer C.free(unsafe.Pointer(cusername))
	var cpassword *C.char = C.CString(ns.Password)
	defer C.free(unsafe.Pointer(cpassword))

	AddCState(&ns.State)
	cstate := GetCState(&ns.State)

	var repo C.Repository
	if len(ns.Repo.Path) > 0 {
		var path *C.char = C.CString(ns.Repo.Path)
		repo = C.RepositoryInitWithPath(*cstate, path)
		defer C.RepositoryFree(repo)
		PanicOnCStateError(cstate)
	}

	ns.Private = C.NetconfSessionInit( *cstate, repo, caddress, cusername, cpassword, cport,
	                                   cprotocol, cOnDemand, cCommonCache, ctimeout,
	                                   cserver, cclient);
	PanicOnCStateError(cstate)
}

// Disconnect from gNMI Session
func (ns *NetconfSession) Disconnect() {
	if ns.Private == nil {
		return
	}
	realSession := ns.Private.(C.Session)
	C.NetconfSessionFree(realSession)
	CleanUpErrorState(&ns.State)
}

// Get root schema node
func (ns *NetconfSession) GetRootSchemaNode() types.RootSchemaNode {
	cstate := GetCState(&ns.State)

	realSession := ns.Private.(C.Session)

	var rootSchema C.RootSchemaWrapper = C.SessionGetRootSchemaNode(*cstate, realSession)
	PanicOnCStateError(cstate)

	if rootSchema == nil {
		ydk.YLogError("Root schema is nil!")
		panic(1)
	}

	rsn := types.RootSchemaNode{Private: rootSchema}
	return rsn
}

// Execute RPC
func (ns *NetconfSession) ExecuteRpc(rpc types.Rpc) types.DataNode {
	cstate := GetCState(&ns.State)

	csession := ns.Private.(C.Session)
	crpc := rpc.Private.(C.Rpc)

	cdn := C.SessionExecuteRpc(*cstate, csession, crpc)
	PanicOnCStateError(cstate)

	dn := types.DataNode{Private: cdn}
	return dn
}

// GetState returns error state from NetconfSession
func (ns *NetconfSession) GetState() *errors.State {
	return &ns.State
}

// GetCapabilities returns list of capabilities supported by NetconfSession
func (ns *NetconfSession) GetCapabilities() []string {

	csession := ns.Private.(C.Session)
	cstate := GetCState(&ns.State)
	length := C.int(0)
	var theCArray **C.char = C.SessionGetCapabilities(*cstate, csession, &length)
	capLen := int(length)

	slice := (*[1 << 30]*C.char)(unsafe.Pointer(theCArray))[:capLen:capLen]
	capabilities := make([]string, capLen)
	for i := range capabilities {
		capabilities[i] = C.GoString(slice[i])
	}
	C.CapabilitiesArrayFree(theCArray, length)
	return capabilities
}
