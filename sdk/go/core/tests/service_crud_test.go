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
	ysanity_bgp "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/openconfig_bgp"
	"github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/ietf_netconf_acm"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/providers"
	"github.com/CiscoDevNet/ydk-go/ydk/services"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	"github.com/CiscoDevNet/ydk-go/ydk/types/yfilter"
	"github.com/CiscoDevNet/ydk-go/ydk/types/ylist"
	"github.com/stretchr/testify/suite"
	"strconv"
	"testing"
	"github.com/stretchr/testify/assert"
)

func getE(code int) ysanity.Runner_InbtwList_Ldata {
	e := ysanity.Runner_InbtwList_Ldata{}
	e.Number = code
	e.Name = strconv.Itoa(code)
	e.Subc.Number = code * 10
	e.Subc.Name = strconv.Itoa(code * 10)
	return e
}

func getEE(code int) ysanity.Runner_InbtwList_Ldata_Subc_SubcSubl1 {
	ee := ysanity.Runner_InbtwList_Ldata_Subc_SubcSubl1{}
	ee.Number = code
	ee.Name = strconv.Itoa(code)
	return ee
}

func getNestedObject() ysanity.Runner {
	runner := ysanity.Runner{}

	e1 := getE(1)
	e2 := getE(2)

	ee11 := getEE(11)
	ee12 := getEE(12)

	e1.Subc.SubcSubl1 = append(e1.Subc.SubcSubl1, &ee11)
	e1.Subc.SubcSubl1 = append(e1.Subc.SubcSubl1, &ee12)

	ee21 := getEE(21)
	ee22 := getEE(22)

	e2.Subc.SubcSubl1 = append(e2.Subc.SubcSubl1, &ee21)
	e2.Subc.SubcSubl1 = append(e2.Subc.SubcSubl1, &ee22)

	runner.InbtwList.Ldata = append(runner.InbtwList.Ldata, &e1)
	runner.InbtwList.Ldata = append(runner.InbtwList.Ldata, &e2)

	return runner
}

type CrudTestSuite struct {
	suite.Suite
	Provider providers.NetconfServiceProvider
	CRUD     services.CrudService
}

func (suite *CrudTestSuite) SetupSuite() {
	suite.CRUD = services.CrudService{}
	suite.Provider = providers.NetconfServiceProvider{
		Address:  "127.0.0.1",
		Username: "admin",
		Password: "admin",
		Port:     12022,
		OnDemand: true}
	suite.Provider.Connect()
}

func (suite *CrudTestSuite) TearDownSuite() {
	suite.Provider.Disconnect()
}

func (suite *CrudTestSuite) BeforeTest(suiteName, testName string) {
	suite.CRUD.Delete(&suite.Provider, &ysanity.Runner{})
	fmt.Printf("%v: %v ...\n", suiteName, testName)
}

func (suite *CrudTestSuite) TestReadVsReadConfig() {
    // Delete BGP config
    bgp := ysanity_bgp.Bgp{}
    suite.CRUD.Delete(&suite.Provider, &bgp)

    // Create BGP config
    bgp.Global.Config.As = 65172
    bgp.Global.Config.RouterId = "1.2.3.4"
    neighbor := ysanity_bgp.Bgp_Neighbors_Neighbor{}
    neighbor.NeighborAddress = "172.16.255.2"
    neighbor.Config.NeighborAddress = "172.16.255.2"
    neighbor.Config.PeerAs = 65172
    bgp.Neighbors.Neighbor = append(bgp.Neighbors.Neighbor, &neighbor)
    suite.CRUD.Create(&suite.Provider, &bgp)

    // Read  BGP Config and Status, then compare
    bgp = ysanity_bgp.Bgp{}
    bgpConfigEntity := suite.CRUD.ReadConfig(&suite.Provider, &bgp)
    bgpStatusEntity := suite.CRUD.Read(&suite.Provider, &bgp)
    suite.False(types.EntityEqual(bgpConfigEntity, bgpStatusEntity))

    suite.CRUD.Delete(&suite.Provider, &bgp)
}

func (suite *CrudTestSuite) TestDeleteObjectOnLeaf() {
	runnerCreate := ysanity.Runner{}
	runnerCreate.One.Name = "runner.YdktestSanityOne.Name"
	runnerCreate.Two.Name = "runner.Two.Name"
	suite.CRUD.Create(&suite.Provider, &runnerCreate)

	// Use YFilter Delete and CRUD update to remove leaf
	runnerUpdate := ysanity.Runner{}
	runnerUpdate.One.Name = yfilter.Delete
	suite.CRUD.Update(&suite.Provider, &runnerUpdate)

	entityRead := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})
	runnerCmp := ysanity.Runner{}
	runnerCmp.Two.Name = "runner.Two.Name"

	suite.Equal(types.EntityEqual(entityRead, &runnerCmp), true)
}

func (suite *CrudTestSuite) TestDeleteOnLeafListElement() {
    runnerCreate := ysanity.Runner{}
    runnerCreate.Ytypes.BuiltInT.Llstring = append(runnerCreate.Ytypes.BuiltInT.Llstring, "0")
    runnerCreate.Ytypes.BuiltInT.Llstring = append(runnerCreate.Ytypes.BuiltInT.Llstring, "1")
    runnerCreate.Ytypes.BuiltInT.Llstring = append(runnerCreate.Ytypes.BuiltInT.Llstring, "2")
    runnerCreate.Ytypes.BuiltInT.Llstring = append(runnerCreate.Ytypes.BuiltInT.Llstring, "3")
    runnerCreate.Ytypes.BuiltInT.Llstring = append(runnerCreate.Ytypes.BuiltInT.Llstring, "4")

    suite.CRUD.Create(&suite.Provider, &runnerCreate)

    runnerUpdate := ysanity.Runner{}
    deleteElement := types.LeafData{Value: "3", Filter: yfilter.Delete}
    runnerUpdate.Ytypes.BuiltInT.Llstring = append(runnerUpdate.Ytypes.BuiltInT.Llstring, deleteElement)

    suite.CRUD.Update(&suite.Provider, &runnerUpdate)

    // try delete again with expected error
    assert.Panicsf(suite.T(), func() { suite.CRUD.Update(&suite.Provider, &runnerUpdate) },
	"Did not receive OK reply from the device", "formatted")
}

func (suite *CrudTestSuite) TestDeleteOnListWithIdentitykey() {
	il := ysanity.Runner_OneList_IdentityList{}
	il.Config.Id = ysanity.ChildIdentity{}
	il.IdRef = ysanity.ChildIdentity{}

	suite.CRUD.Create(&suite.Provider, &il)

	il.YFilter = yfilter.Delete
	suite.CRUD.Update(&suite.Provider, &il)

	entityRead := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})
	suite.Nil(entityRead)
}

func (suite *CrudTestSuite) TestDeleteOnContainer() {
	runnerCreate := ysanity.Runner{}
	runnerCreate.One.Name = "runner.YdktestSanityOne.Name"
	runnerCreate.Two.Name = "runner.Two.Name"
	suite.CRUD.Create(&suite.Provider, &runnerCreate)

	runnerUpdate := ysanity.Runner{}
	runnerUpdate.Two.YFilter = yfilter.Delete
	suite.CRUD.Update(&suite.Provider, &runnerUpdate)

	runnerCmp := ysanity.Runner{}
	runnerCmp.One.Name = "runner.YdktestSanityOne.Name"

	entityRead := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})

	suite.Equal(types.EntityEqual(entityRead, &runnerCmp), true)
}

func (suite *CrudTestSuite) TestDeleteOnNestedList() {
	runnerCreate := getNestedObject()
	suite.CRUD.Create(&suite.Provider, &runnerCreate)

	entity := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})
	runnerUpdate := entity.(*ysanity.Runner)

	for _, e := range runnerUpdate.InbtwList.Ldata[1].Subc.SubcSubl1 {
	    e.YFilter = yfilter.Delete
	}
	suite.CRUD.Update(&suite.Provider, runnerUpdate)

	entity = suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})

	runnerCmp := getNestedObject()
	runnerCmp.InbtwList.Ldata[1].Subc.SubcSubl1 = []*ysanity.Runner_InbtwList_Ldata_Subc_SubcSubl1{}
	suite.True(types.EntityEqual(entity, &runnerCmp))
}

func (suite *CrudTestSuite) TestDeleteOnListElement() {
	runnerCreate := getNestedObject()
	suite.CRUD.Create(&suite.Provider, &runnerCreate)

	runnerUpdate := runnerCreate
	runnerUpdate.InbtwList.Ldata[1].YFilter = yfilter.Delete
	suite.CRUD.Update(&suite.Provider, &runnerUpdate)

	entity := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})

	runnerCmp := runnerCreate
	runnerCmp.InbtwList.Ldata = runnerCmp.InbtwList.Ldata[:1]

	suite.Equal(types.EntityEqual(entity, &runnerCmp), true)
}

func (suite *CrudTestSuite) TestDeleteOnFewListElements() {
	runnerCreate := ysanity.Runner{}
	runnerCreate.One.Name = "one"
	foo := ysanity.Runner_OneList_Ldata{}
	bar := ysanity.Runner_OneList_Ldata{}
	baz := ysanity.Runner_OneList_Ldata{}
	foo.Number = 1
	foo.Name = "foo"
	bar.Number = 2
	bar.Name = "bar"
	baz.Number = 3
	baz.Name = "baz"

	runnerCreate.OneList.Ldata = append(runnerCreate.OneList.Ldata, &foo)
	runnerCreate.OneList.Ldata = append(runnerCreate.OneList.Ldata, &bar)
	runnerCreate.OneList.Ldata = append(runnerCreate.OneList.Ldata, &baz)

	suite.CRUD.Create(&suite.Provider, &runnerCreate)

	entity := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})
	runnerUpdate := entity.(*ysanity.Runner)
	runnerUpdate.OneList.Ldata[1].YFilter = yfilter.Delete
	runnerUpdate.OneList.Ldata[2].YFilter = yfilter.Delete

	suite.CRUD.Update(&suite.Provider, runnerUpdate)

	entity = suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})

	runnerCmp := runnerCreate
	runnerCmp.OneList.Ldata = runnerCmp.OneList.Ldata[:1]

	suite.Equal(types.EntityEqual(entity, &runnerCmp), true)
}

func (suite *CrudTestSuite) TestSanityMultipleEntities() {
	// Build configuration collection
	runner := ysanity.Runner{}
	runner.Two.Number = 2
	runner.Two.Name = "runner-two-name"
	
	native := ysanity.Native{}
	native.Version = "0.1.0"
	native.Hostname = "MyHost"
	
	configEC := types.NewConfig(&runner, &native)

	// Create configuration
	result := suite.CRUD.Create(&suite.Provider, configEC)
	suite.Equal(result, true)
	
	// Build filter
	runnerFilter := ysanity.Runner{}
	nativeFilter := ysanity.Native{}
	filterEC := types.NewFilter(&runnerFilter, &nativeFilter)

	// Read running config
	readEntity := suite.CRUD.Read(&suite.Provider, filterEC)
	suite.Equal( types.IsEntityCollection(readEntity), true)

	// Get results
	readEC := types.EntityToCollection(readEntity)
	for _, entity := range readEC.Entities() {
		ydk.YLogDebug(fmt.Sprintf("Printing %s", GetEntityXMLString(entity)))
	}

	// Delete configuration
	result = suite.CRUD.Delete(&suite.Provider, configEC)
	suite.Equal(result, true)
}

func (suite *CrudTestSuite) TestSanityReadConfig() {
	// Import ietf_netconf_acm package in order to register otherwise missing entity 
	nacm := ietf_netconf_acm.Nacm{}
	
	// Build empty filter
	filterEC := types.NewFilter(&nacm)
	filterEC.Clear()

	// Read running config
	readEntity := suite.CRUD.ReadConfig(&suite.Provider, filterEC)
	suite.Equal( types.IsEntityCollection(readEntity), true)

	// Get results
	readEC := types.EntityToCollection(readEntity)
	for _, entity := range readEC.Entities() {
		ydk.YLogDebug(fmt.Sprintf("Printing %s", GetEntityXMLString(entity)))
	}
}

func (suite *CrudTestSuite) TestDeleteList() {
	// CREATE
	runnerCreate := ysanity.Runner{}
	runnerCreate.One.Name = "one"
	foo := ysanity.Runner_OneList_Ldata{}
	bar := ysanity.Runner_OneList_Ldata{}
	foo.Number = 1
	foo.Name = "foo"
	bar.Number = 2
	bar.Name = "bar"

	runnerCreate.OneList.Ldata = append(runnerCreate.OneList.Ldata, &foo)
	runnerCreate.OneList.Ldata = append(runnerCreate.OneList.Ldata, &bar)

	suite.CRUD.Create(&suite.Provider, &runnerCreate)

	// READ then DELETE all list elements
	entity := suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})
	runnerUpdate := entity.(*ysanity.Runner)
	for _, e := range runnerUpdate.OneList.Ldata {
		e.YFilter = yfilter.Delete
	}
	suite.CRUD.Update(&suite.Provider, runnerUpdate)

	// READ and VALIDATE
	entity = suite.CRUD.Read(&suite.Provider, &ysanity.Runner{})
	runnerCmp := runnerCreate
	runnerCmp.OneList.Ldata = []*ysanity.Runner_OneList_Ldata {}
	suite.Equal(types.EntityEqual(entity, &runnerCmp), true)
}

func (suite *CrudTestSuite) TestDeleteContainer() {
	// Build loopback configuration
	address := ysanity.Native_Interface_Loopback_Ipv4_Address{}
	address.Ip = "2.2.2.2"
	address.PrefixLength = 32

	loopback := ysanity.Native_Interface_Loopback{}
	loopback.Name = 2222
	loopback.Ipv4.Address = append(loopback.Ipv4.Address, &address)

	native := ysanity.Native{}
        native.Interface.Loopback = append(native.Interface.Loopback, &loopback)

	result := suite.CRUD.Create(&suite.Provider, &native)
	suite.True(result)

	// Read ipv4 configuration
	native = ysanity.Native{}
	loopback = ysanity.Native_Interface_Loopback{}
	loopback.Name = 2222
	native.Interface.Loopback = append(native.Interface.Loopback, &loopback)
	types.SetAllParents(&native)
	ipv4ConfigEnt := suite.CRUD.Read(&suite.Provider, &loopback.Ipv4)
	suite.NotNil(ipv4ConfigEnt)
	ipv4Config := ipv4ConfigEnt.(*ysanity.Native_Interface_Loopback_Ipv4)
	_, addressEnt := ylist.Get(ipv4Config.Address, "2.2.2.2")
	suite.NotNil(addressEnt)
	addressPtr := addressEnt.(*ysanity.Native_Interface_Loopback_Ipv4_Address)
	suite.Equal("32", addressPtr.PrefixLength)

	// Remove ipv4 configuration
	native = ysanity.Native{}
	loopback = ysanity.Native_Interface_Loopback{}
	loopback.Name = 2222
	native.Interface.Loopback = append(native.Interface.Loopback, &loopback)
	types.SetAllParents(&native)
	result = suite.CRUD.Delete(&suite.Provider, &loopback.Ipv4)
        suite.True(result)

	// Delete configuration
	native = ysanity.Native{}
	result = suite.CRUD.Delete(&suite.Provider, &native)
	suite.True(result)
}

func TestCrudTestSuite(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	suite.Run(t, new(CrudTestSuite))
}
