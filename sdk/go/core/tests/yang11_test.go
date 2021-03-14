// YANG-1.1 feature unit tests for Go.
//
// YDK - YANG Development Kit
// Copyright 2020 Yan Gorelik, YDK Solutions. All rights reserved.
//
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.package test

package test

import (
	"fmt"
	ysanity "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest_yang11/ydktest_sanity_yang11"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/providers"
	"github.com/CiscoDevNet/ydk-go/ydk/services"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	encoding "github.com/CiscoDevNet/ydk-go/ydk/types/encoding_format"
	"github.com/CiscoDevNet/ydk-go/ydk/types/ylist"
	"github.com/stretchr/testify/suite"
	"testing"
	"strings"
)

type SanityYang11TestSuite struct {
	suite.Suite
	Provider providers.CodecServiceProvider
	JsonProvider providers.CodecServiceProvider
	Codec services.CodecService
}

func (suite *SanityYang11TestSuite) SetupSuite() {
	suite.Codec = services.CodecService{}
	suite.Provider = providers.CodecServiceProvider{Encoding: encoding.XML}
	suite.JsonProvider = providers.CodecServiceProvider{Encoding: encoding.JSON}
}

// func (suite *SanityYang11TestSuite) TestContainer() {
// 	container := ysanity.BackwardIncompatible{}
// 	container.TestNode = "Testing node"
// 	suite.CRUD.Create(&suite.Provider, &container)
//
// 	entityRead := suite.CRUD.Read(&suite.Provider, &ysanity.BackwardIncompatible{})
// 	suite.True(types.EntityEqual(entityRead, &container))
//
// 	suite.CRUD.Delete(&suite.Provider, &ysanity.BackwardIncompatible{})
// }

func (suite *SanityYang11TestSuite) TestTypeEmpty() {
        top := ysanity.EmptyType{}
        list_elem := ysanity.EmptyType_Filter{}
        list_elem.Name = "filter-name"
        list_elem.Enabled = types.Empty{}
        list_elem.Prop = "one"
        list_elem.OutboundFilter = types.Empty{}
        top.Filter = append(top.Filter, &list_elem)

        payload := suite.Codec.Encode(&suite.Provider, &top)
        suite.False(payload == "")

        entity := suite.Codec.Decode(&suite.Provider, payload)
        suite.True(types.EntityEqual(&top, entity))

        suite.Equal("[filter-name]", fmt.Sprintf("%v", ylist.Keys(top.Filter)))
        _, ldata := ylist.Get(top.Filter, "filter-name")
		suite.NotNil(ldata)
        suite.True(types.EntityEqual(&list_elem, ldata))
}

func (suite *SanityYang11TestSuite) TestTypeEmptyJson() {
        top := ysanity.EmptyType{}
        list_elem := ysanity.EmptyType_Filter{}
        list_elem.Name = "filter-name"
        list_elem.Enabled = types.Empty{}
        list_elem.Prop = "one"
        list_elem.OutboundFilter = types.Empty{}
        top.Filter = append(top.Filter, &list_elem)

        payload := suite.Codec.Encode(&suite.JsonProvider, &top)
        suite.False(payload == "")

        entity := suite.Codec.Decode(&suite.JsonProvider, payload)
        suite.True(types.EntityEqual(&top, entity))

        suite.Equal("[filter-name]", fmt.Sprintf("%v", ylist.Keys(top.Filter)))
        _, ldata := ylist.Get(top.Filter, "filter-name")
		suite.NotNil(ldata)
        suite.True(types.EntityEqual(&list_elem, ldata))
}

func (suite *SanityYang11TestSuite) TestTypeAnydata() {
        top := ysanity.AnydataType{}
        payload := suite.Codec.Encode(&suite.Provider, &top)
        suite.Equal(strings.TrimSpace(payload), `<anydata-type xmlns="http://cisco.com/ns/yang/ydktest-yang11"/>`)
}

func TestSanityYang11TestSuite(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	suite.Run(t, new(SanityYang11TestSuite))
}