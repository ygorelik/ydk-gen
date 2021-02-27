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
// 	"fmt"
	ysanity "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest_yang11/ydktest_sanity_yang11"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/providers"
	"github.com/CiscoDevNet/ydk-go/ydk/services"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	"github.com/stretchr/testify/suite"
// 	"strconv"
	"testing"
)

type SanityYang11TestSuite struct {
	suite.Suite
	Provider providers.NetconfServiceProvider
	CRUD     services.CrudService
}

func (suite *SanityYang11TestSuite) SetupSuite() {
	suite.CRUD = services.CrudService{}
	suite.Provider = providers.NetconfServiceProvider{
		Address:  "127.0.0.1",
		Username: "admin",
		Password: "admin",
		Port:     12022}
	suite.Provider.Connect()
}

// func (suite *SanityYang11TestSuite) BeforeTest(suiteName, testName string) {
// 	suite.CRUD.Delete(&suite.Provider, &ysanity.Runner{})
// 	fmt.Printf("%v: %v ...\n", suiteName, testName)
// }

func (suite *SanityYang11TestSuite) TearDownSuite() {
	suite.Provider.Disconnect()
}

func (suite *SanityYang11TestSuite) TestContainer() {
	container := ysanity.BackwardIncompatible{}
	container.TestNode = "Testing node"
	suite.CRUD.Create(&suite.Provider, &container)

	entityRead := suite.CRUD.Read(&suite.Provider, &ysanity.BackwardIncompatible{})
	suite.True(types.EntityEqual(entityRead, &container))

	suite.CRUD.Delete(&suite.Provider, &ysanity.BackwardIncompatible{})
}

func TestSanityYang11TestSuite(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Info)
	}
	suite.Run(t, new(SanityYang11TestSuite))
}