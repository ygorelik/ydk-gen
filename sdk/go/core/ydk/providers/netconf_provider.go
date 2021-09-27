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

package providers

import (
	"fmt"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/errors"
	"github.com/CiscoDevNet/ydk-go/ydk/path"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	"github.com/CiscoDevNet/ydk-go/ydk/types/yfilter"
)

// NetconfServiceProvider Implementation of ServiceProvider for the NETCONF protocol: https://tools.ietf.org/html/rfc6241
type NetconfServiceProvider struct {
	Repo     	types.Repository
	Address  	string
	Username 	string
	Password 	string
	Port     	int
	Protocol 	string
	OnDemand 	bool
	CommonCache	bool
	Timeout		int
	ServerCert	string
	PrivateKey	string

	Private types.CServiceProvider
	State   errors.State
}

// Connect to NetconfServiceProvider using Repo/Address/Username/Password/Port
func (provider *NetconfServiceProvider) Connect() {
	if len(provider.Protocol) == 0 {
		provider.Protocol = "ssh"
	}
	if provider.Port == 0 {
		provider.Port = 830
	}
	if provider.Timeout == 0 {
		provider.Timeout = -1
	}
	provider.Private = path.ConnectToNetconfProvider(
		&provider.State,
		provider.Repo,
		provider.Address,
		provider.Username,
		provider.Password,
		provider.Port,
		provider.Protocol,
		provider.OnDemand,
		provider.CommonCache,
		provider.Timeout,
		provider.ServerCert,
		provider.PrivateKey)
}

// Disconnect from NetconfServiceProvider
func (provider *NetconfServiceProvider) Disconnect() {
	if provider.Private.Private == nil {
		return
	}
	path.DisconnectFromNetconfProvider(provider.Private)
	path.CleanUpErrorState(&provider.State)
}

// GetPrivate returns private pointer for NetconfServiceProvider
func (provider *NetconfServiceProvider) GetPrivate() interface{} {
	return provider.Private
}

// GetState returns error state from NetconfServiceProvider
func (provider *NetconfServiceProvider) GetState() *errors.State {
	return &provider.State
}

// GetCapabilities returns the capabilities supported by NetconfServiceProvider
func (provider *NetconfServiceProvider) GetCapabilities() []string {
	session := path.ServiceProviderGetSession(provider.Private)
	return path.GetSessionCapabilities(session)
}

func (provider *NetconfServiceProvider) ExecuteRpc(operation string, entity types.Entity, params map[string]string) types.DataNode {
	return executeNetconfRpc(provider, operation, entity, params)
}

func executeNetconfRpc(provider types.ServiceProvider, operation string, entity types.Entity, params map[string]string) types.DataNode {
	rpcTag := getRpcTag(operation)
	dataTag := "entity"
	if operation == "read" {
		dataTag = "filter"
		types.SetNontopEntityFilter(entity, yfilter.Read)
	} else {
		if operation == "delete" {
			types.SetNontopEntityFilter(entity, yfilter.Delete)
		}
	}
	data := make(map[string]interface{})
	data[dataTag] = entity

	setConfigFlag := false
	mode, ok := params["mode"]
	if ok && mode == "config" {
		setConfigFlag = true
	}
	dn := path.ExecuteRPC(provider, rpcTag, data, setConfigFlag)
	types.SetNontopEntityFilter(entity, yfilter.NotSet)
	return dn
}

func getRpcTag(operation string) string {
	var rpc string
	if operation == "create" {
		rpc = "ydk:create"
	} else if operation == "update" {
		rpc = "ydk:update"
	} else if operation == "delete" {
		rpc = "ydk:delete"
	} else if operation == "read" {
		rpc = "ydk:read"
	} else {
		ydk.YLogError(fmt.Sprintf("getRpcTag: Operation '%s' is not supported", operation));
		panic(1)
	}
	return rpc;
}
