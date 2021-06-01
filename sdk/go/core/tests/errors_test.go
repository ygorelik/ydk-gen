/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2016-2019 Cisco Systems. All rights reserved.

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

package test

import (
	"fmt"
	ysanity "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/sanity"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/providers"
	"github.com/CiscoDevNet/ydk-go/ydk/services"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
	"testing"
)

type ErrorsTestSuite struct {
	suite.Suite
	Provider providers.NetconfServiceProvider
	CRUD     services.CrudService
}

func (suite *ErrorsTestSuite) SetupSuite() {
	suite.CRUD = services.CrudService{}
	suite.Provider = providers.NetconfServiceProvider{
		Address:  "127.0.0.1",
		Username: "admin",
		Password: "admin",
		Port:     12022}
	suite.Provider.Connect()
	suite.CRUD.Delete(&suite.Provider, &ysanity.Runner{})
}

func (suite *ErrorsTestSuite) TearDownSuite() {
	suite.Provider.Disconnect()
}

func (suite *ErrorsTestSuite) BeforeTest(suiteName, testName string) {
	fmt.Printf("%v: %v ...\n", suiteName, testName)
}

func (suite *ErrorsTestSuite) TestInvalidInt8() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.Number8 = 8.5
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"number8\" element. Path: '/ydktest-sanity:number8'",
		runner.Ytypes.BuiltInT.Number8)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

// TODO: string representation always treated as valid value
// func (suite *ErrorsTestSuite) TestInvalidInt16() {
// 	runner := ysanity.Runner{}
// 	runner.Ytypes.BuiltInT.Number16 = "16"
// 	suite.CRUD.Create(&suite.Provider, &runner)
// }

func (suite *ErrorsTestSuite) TestInvalidInt16() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.Number16 = true
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"number16\" element. Path: '/ydktest-sanity:number16'",
		runner.Ytypes.BuiltInT.Number16)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

func (suite *ErrorsTestSuite) TestInvalidInt32() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.Number32 = make([]int, 0)
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"number32\" element. Path: '/ydktest-sanity:number32'",
		runner.Ytypes.BuiltInT.Number32)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

// Invalid test case, go int64 range: -9223372036854775808 through 9223372036854775807
// func (suite *ErrorsTestSuite) TestInvalidInt64() {
// 	runner := ysanity.Runner{}
// 	runner.Ytypes.BuiltInT.Number64 = int64(9223372036854775808)
// 	suite.CRUD.Create(&suite.Provider, &runner)
// }

func (suite *ErrorsTestSuite) TestInvalidUint8() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.UNumber8 = -1
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"u_number8\" element. Path: '/ydktest-sanity:u_number8'",
		runner.Ytypes.BuiltInT.UNumber8)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

func (suite *ErrorsTestSuite) TestInvalidUint16() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.UNumber16 = "non uint16"
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"u_number16\" element. Path: '/ydktest-sanity:u_number16'",
		runner.Ytypes.BuiltInT.UNumber16)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

func (suite *ErrorsTestSuite) TestInvalidUint32() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.UNumber32 = 4294967296
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"u_number32\" element. Path: '/ydktest-sanity:u_number32'",
		runner.Ytypes.BuiltInT.UNumber32)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

// Invalid test case, go int64 range: -9223372036854775808 through 9223372036854775807
// func (suite *ErrorsTestSuite) TestInvalidUint64() {
// 	runner := ysanity.Runner{}
// 	runner.Ytypes.BuiltInT.UNumber64 = 18446744073709551616
// 	suite.CRUD.Create(&suite.Provider, &runner)
// }

// TODO: should raise error
// func (suite *ErrorsTestSuite) TestInvalidString() {
// 	runner := ysanity.Runner{}
// 	runner.Ytypes.BuiltInT.Name = [...]string{"name", "string", "list"}
// 	suite.CRUD.Create(&suite.Provider, &runner)
// }

func (suite *ErrorsTestSuite) TestInvalidBoolean() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.BoolValue = "a string"
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"bool-value\" element. Path: '/ydktest-sanity:bool-value'",
		runner.Ytypes.BuiltInT.BoolValue)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

// TODO: should raise error
// func (suite *ErrorsTestSuite) TestInvalidEmpty() {
// 	runner := ysanity.Runner{}
// 	runner.Ytypes.BuiltInT.Emptee = 123
// 	suite.CRUD.Create(&suite.Provider, &runner)
// }

func (suite *ErrorsTestSuite) TestInvalidEnum() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.EnumValue = "non enum"
	errMsg := fmt.Sprintf("YModelError: Invalid value \"%v\" in \"enum-value\" element. Path: '/ydktest-sanity:enum-value'",
		runner.Ytypes.BuiltInT.EnumValue)
	assert.PanicsWithValue(suite.T(), errMsg, func() { suite.CRUD.Create(&suite.Provider, &runner) })
}

func TestErrorsTestSuite(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	suite.Run(t, new(ErrorsTestSuite))
}
