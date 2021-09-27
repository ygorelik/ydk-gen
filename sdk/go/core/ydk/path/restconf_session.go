/* ----------------------------------------------------------------------
YANG Development Kit
Package path implements support for Restconf Session in Go.

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
	"unsafe"

	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/errors"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	encoding "github.com/CiscoDevNet/ydk-go/ydk/types/encoding_format"
)

// RestconfSession declaration and methods
//
type RestconfSession struct {
	Repo       types.Repository
	Address    string
	Username   string
	Password   string
	Port       int
	Encoding   encoding.EncodingFormat
	ConfigRoot string
	StateRoot  string

	Private interface{}
	State   errors.State
}

// Connect to Restconf Session
func (rs *RestconfSession) Connect() {
	var cAddress *C.char = C.CString(rs.Address)
	defer C.free(unsafe.Pointer(cAddress))

	var cUsername *C.char = C.CString(rs.Username)
	defer C.free(unsafe.Pointer(cUsername))

	var cPassword *C.char = C.CString(rs.Password)
	defer C.free(unsafe.Pointer(cPassword))

	if rs.Port == 0 {
		rs.Port = 80
	}
	var cPort C.int = C.int(rs.Port)

	var cEncoding C.EncodingFormat = C.JSON
	if rs.Encoding == encoding.XML {
		cEncoding = C.XML
	}

	if len(rs.ConfigRoot) == 0 {
		rs.ConfigRoot = "/data"
	}
	var cConfigRoot *C.char = C.CString(rs.ConfigRoot)
	defer C.free(unsafe.Pointer(cConfigRoot))

	if len(rs.StateRoot) == 0 {
		rs.StateRoot = "/data"
	}
	var cStateRoot *C.char = C.CString(rs.StateRoot)
	defer C.free(unsafe.Pointer(cStateRoot))

	AddCState(&rs.State)
	cstate := GetCState(&rs.State)

	var repo C.Repository
	if len(rs.Repo.Path) > 0 {
		var path *C.char = C.CString(rs.Repo.Path)
		repo = C.RepositoryInitWithPath(*cstate, path)
		defer C.RepositoryFree(repo)
		PanicOnCStateError(cstate)
	}

	rs.Private = C.RestconfSessionInit(*cstate, repo,
		cAddress, cUsername, cPassword, cPort,
		cEncoding, cConfigRoot, cStateRoot)
	PanicOnCStateError(cstate)
}

// Disconnect from gNMI Session
func (ns *RestconfSession) Disconnect() {
	if ns.Private == nil {
		return
	}
	realSession := ns.Private.(C.Session)
	C.RestconfSessionFree(realSession)
	CleanUpErrorState(&ns.State)
}

// Get root schema node
func (rs *RestconfSession) GetRootSchemaNode() types.RootSchemaNode {
	cstate := GetCState(&rs.State)

	realSession := rs.Private.(C.Session)

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
func (rs *RestconfSession) ExecuteRpc(rpc types.Rpc) types.DataNode {
	cstate := GetCState(&rs.State)

	csession := rs.Private.(C.Session)
	crpc := rpc.Private.(C.Rpc)

	cdn := C.SessionExecuteRpc(*cstate, csession, crpc)
	PanicOnCStateError(cstate)

	dn := types.DataNode{Private: cdn}
	return dn
}

// GetState returns error state from RestconfSession
func (rs *RestconfSession) GetState() *errors.State {
	return &rs.State
}

// GetCapabilities returns list of capabilities supported by RestconfSession
func (rs *RestconfSession) GetCapabilities() []string {

    session := types.Session{Private: rs.Private}
    return GetSessionCapabilities(session)
}
