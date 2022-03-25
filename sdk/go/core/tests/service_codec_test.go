package test

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
	"github.com/CiscoDevNet/ydk-go/ydk"
	"github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/oc_pattern"
	ysanity_bgp "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/openconfig_bgp"
	ysanity_bgp_types "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/openconfig_bgp_types"
	ysanity "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/sanity"
	ysanity_typedefs "github.com/CiscoDevNet/ydk-go/ydk/models/ydktest/sanity_typedefs"
	"github.com/CiscoDevNet/ydk-go/ydk/providers"
	"github.com/CiscoDevNet/ydk-go/ydk/services"
	"github.com/CiscoDevNet/ydk-go/ydk/types"
	"github.com/CiscoDevNet/ydk-go/ydk/types/ylist"
	encoding "github.com/CiscoDevNet/ydk-go/ydk/types/encoding_format"
	"github.com/stretchr/testify/suite"
	"testing"
)

const (
	xmlBgpPayload = `<?xml version="1.0"?><bgp xmlns="http://openconfig.net/yang/bgp">
  <global>
    <config>
      <as>65172</as>
      <router-id>1.2.3.4</router-id>
    </config>
    <afi-safis>
      <afi-safi>
        <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:IPV6_UNICAST</afi-safi-name>
        <config>
          <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:IPV6_UNICAST</afi-safi-name>
          <enabled>true</enabled>
        </config>
      </afi-safi>
      <afi-safi>
        <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:IPV4_UNICAST</afi-safi-name>
        <config>
          <afi-safi-name xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types">oc-bgp-types:IPV4_UNICAST</afi-safi-name>
          <enabled>true</enabled>
        </config>
      </afi-safi>
    </afi-safis>
  </global>
</bgp>
`

	jsonBgpPayload = `{
  "openconfig-bgp:bgp": {
    "global": {
      "afi-safis": {
        "afi-safi": [
          {
            "afi-safi-name": "openconfig-bgp-types:IPV6_UNICAST",
            "config": {
              "afi-safi-name": "openconfig-bgp-types:IPV6_UNICAST",
              "enabled": true
            }
          },
          {
            "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
            "config": {
              "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
              "enabled": true
            }
          }
        ]
      },
      "config": {
        "as": 65172,
        "router-id": "1.2.3.4"
      }
    }
  }
}
`

	xmlRunnerPayload = `<?xml version="1.0"?><runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <two-list>
    <ldata>
      <number>21</number>
      <name>runner:twolist:ldata:21</name>
      <subl1>
        <number>211</number>
        <name>runner:twolist:ldata:21:subl1:211</name>
      </subl1>
      <subl1>
        <number>212</number>
        <name>runner:twolist:ldata:21:subl1:212</name>
      </subl1>
    </ldata>
    <ldata>
      <number>22</number>
      <name>runner:twolist:ldata:22</name>
      <subl1>
        <number>221</number>
        <name>runner:twolist:ldata:22:subl1:221</name>
      </subl1>
      <subl1>
        <number>222</number>
        <name>runner:twolist:ldata:22:subl1:222</name>
      </subl1>
    </ldata>
  </two-list>
</runner>
`

	xmlRunnerPayload2 = `<?xml version="1.0"?><runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <ytypes>
    <built-in-t>
      <enum-value>local</enum-value>
    </built-in-t>
  </ytypes>
</runner>`

	jsonRunnerPayload = `{
  "ydktest-sanity:runner": {
    "two-list": {
      "ldata": [
        {
          "number": 21,
          "name": "runner:twolist:ldata:21",
          "subl1": [
            {
              "number": 211,
              "name": "runner:twolist:ldata:21:subl1:211"
            },
            {
              "number": 212,
              "name": "runner:twolist:ldata:21:subl1:212"
            }
          ]
        },
        {
          "number": 22,
          "name": "runner:twolist:ldata:22",
          "subl1": [
            {
              "number": 221,
              "name": "runner:twolist:ldata:22:subl1:221"
            },
            {
              "number": 222,
              "name": "runner:twolist:ldata:22:subl1:222"
            }
          ]
        }
      ]
    }
  }
}
`

	jsonRunnerPayload2 = `{
  "ydktest-sanity:built-in-t": {
    "enum-value": "local"
  }
}`

	xmlOCPatternPayload = `<?xml version="1.0"?><oc-A xmlns="http://cisco.com/ns/yang/oc-pattern">
  <a>Hello</a>
</oc-A>
`
	jsonNoKeyList = `{
  "ydktest-sanity:runner": {
    "no-key-list": [
      {
        "test": "t1"
      },
      {
        "test": "t2"
      },
      {
        "test": "t3"
      }
    ]
  }
}
`
)

func equalPayload(s1, s2 string, um func([]uint8, interface{}) error, m func(interface{}) ([]byte, error)) bool {
	var o1 interface{}
	var o2 interface{}

	var err error
	err = um([]byte(s1), &o1)
	if err != nil {
		panic(fmt.Sprintf("Error unmashalling string 1: %s", err.Error()))
	}
	err = um([]byte(s2), &o2)
	if err != nil {
		panic(fmt.Sprintf("Error unmashalling string 1: %s", err.Error()))
	}

	// Unmarshal and Marshal the payload in case list items in payload shows in random order
	p1, err := m(o1)
	if err != nil {
		panic(fmt.Sprintf("Error mashalling object 1: %s", err.Error()))
	}
	p2, err := m(o1)
	if err != nil {
		panic(fmt.Sprintf("Error mashalling object 1: %s", err.Error()))
	}

	return string(p1) == string(p2)
}

type CodecTestSuite struct {
	suite.Suite
	Provider providers.CodecServiceProvider
	Codec    services.CodecService
}

func (suite *CodecTestSuite) SetupSuite() {
	suite.Codec = services.CodecService{}
	suite.Provider = providers.CodecServiceProvider{}
}

func (suite *CodecTestSuite) BeforeTest(suiteName, testName string) {
	fmt.Printf("%v: %v ...\n", suiteName, testName)
}

func (suite *CodecTestSuite) TearDownSuite() {
}

func config(bgp *ysanity_bgp.Bgp) {
	bgp.Global.Config.As = 65172
	bgp.Global.Config.RouterId = "1.2.3.4"

	ipv6Afisafi := ysanity_bgp.Bgp_Global_AfiSafis_AfiSafi{}
	ipv6Afisafi.AfiSafiName = &ysanity_bgp_types.IPV6UNICAST{}
	ipv6Afisafi.Config.AfiSafiName = &ysanity_bgp_types.IPV6UNICAST{}
	ipv6Afisafi.Config.Enabled = true
	bgp.Global.AfiSafis.AfiSafi = append(bgp.Global.AfiSafis.AfiSafi, &ipv6Afisafi)

	ipv4Afisafi := ysanity_bgp.Bgp_Global_AfiSafis_AfiSafi{}
	ipv4Afisafi.AfiSafiName = &ysanity_bgp_types.IPV4UNICAST{}
	ipv4Afisafi.Config.AfiSafiName = &ysanity_bgp_types.IPV4UNICAST{}
	ipv4Afisafi.Config.Enabled = true
	bgp.Global.AfiSafis.AfiSafi = append(bgp.Global.AfiSafis.AfiSafi, &ipv4Afisafi)
}

func configRunner(runner *ysanity.Runner) {
	elem1 := ysanity.Runner_TwoList_Ldata{}
	elem2 := ysanity.Runner_TwoList_Ldata{}

	elem1.Number = 21
	elem1.Name = "runner:twolist:ldata:21"

	elem2.Number = 22
	elem2.Name = "runner:twolist:ldata:22"

	elem11 := ysanity.Runner_TwoList_Ldata_Subl1{}
	elem12 := ysanity.Runner_TwoList_Ldata_Subl1{}

	elem11.Number = 211
	elem11.Name = "runner:twolist:ldata:21:subl1:211"
	elem12.Number = 212
	elem12.Name = "runner:twolist:ldata:21:subl1:212"

	elem1.Subl1 = append(elem1.Subl1, &elem11)
	elem1.Subl1 = append(elem1.Subl1, &elem12)

	elem21 := ysanity.Runner_TwoList_Ldata_Subl1{}
	elem22 := ysanity.Runner_TwoList_Ldata_Subl1{}

	elem21.Number = 221
	elem21.Name = "runner:twolist:ldata:22:subl1:221"
	elem22.Number = 222
	elem22.Name = "runner:twolist:ldata:22:subl1:222"

	elem2.Subl1 = append(elem2.Subl1, &elem21)
	elem2.Subl1 = append(elem2.Subl1, &elem22)

	runner.TwoList.Ldata = append(runner.TwoList.Ldata, &elem1)
	runner.TwoList.Ldata = append(runner.TwoList.Ldata, &elem2)
}

func (suite *CodecTestSuite) TestXMLEncode() {
	bgp := ysanity_bgp.Bgp{}
	config(&bgp)

	suite.Provider.Encoding = encoding.XML
	payload := suite.Codec.Encode(&suite.Provider, &bgp)

	result := equalPayload(payload, xmlBgpPayload, xml.Unmarshal, xml.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestXMLDecode() {

	for i := 0; i < 100; i++ {
		bgp := ysanity_bgp.Bgp{}
		config(&bgp)

		suite.Provider.Encoding = encoding.XML

		entity := suite.Codec.Decode(&suite.Provider, xmlBgpPayload)
		bgpDecodec := entity.(*ysanity_bgp.Bgp)

		suite.Equal(types.EntityEqual(&bgp, bgpDecodec), true)
	}
}

func (suite *CodecTestSuite) TestXMLEncodeDecode() {
	bgp := ysanity_bgp.Bgp{}
	config(&bgp)

	suite.Provider.Encoding = encoding.XML

	payload := suite.Codec.Encode(&suite.Provider, &bgp)
	entity := suite.Codec.Decode(&suite.Provider, payload)
	bgpDecodec := entity.(*ysanity_bgp.Bgp)

	suite.Equal(types.EntityEqual(&bgp, bgpDecodec), true)
}

func (suite *CodecTestSuite) TestXMLDecodeEncode() {
	suite.Provider.Encoding = encoding.XML

	entity := suite.Codec.Decode(&suite.Provider, xmlBgpPayload)
	bgpDecodec := entity.(*ysanity_bgp.Bgp)
	payload := suite.Codec.Encode(&suite.Provider, bgpDecodec)

	result := equalPayload(payload, xmlBgpPayload, xml.Unmarshal, xml.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestJSONEncode() {
	bgp := ysanity_bgp.Bgp{}
	config(&bgp)

	suite.Provider.Encoding = encoding.JSON
	payload := suite.Codec.Encode(&suite.Provider, &bgp)

	result := equalPayload(payload, jsonBgpPayload, json.Unmarshal, json.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestJSONDecode() {
	bgp := ysanity_bgp.Bgp{}
	config(&bgp)

	suite.Provider.Encoding = encoding.JSON

	entity := suite.Codec.Decode(&suite.Provider, jsonBgpPayload)
	bgpDecodec := entity.(*ysanity_bgp.Bgp)

	suite.Equal(types.EntityEqual(&bgp, bgpDecodec), true)
}

func (suite *CodecTestSuite) TestJSONDecodeEncode() {
	bgp := ysanity_bgp.Bgp{}
	config(&bgp)

	suite.Provider.Encoding = encoding.JSON

	entity := suite.Codec.Decode(&suite.Provider, jsonBgpPayload)
	bgpDecodec := entity.(*ysanity_bgp.Bgp)
	payload := suite.Codec.Encode(&suite.Provider, bgpDecodec)

	result := equalPayload(payload, jsonBgpPayload, json.Unmarshal, json.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestJSONEncodeDecode() {
	bgp := ysanity_bgp.Bgp{}
	config(&bgp)

	suite.Provider.Encoding = encoding.JSON

	payload := suite.Codec.Encode(&suite.Provider, &bgp)
	entity := suite.Codec.Decode(&suite.Provider, payload)
	bgpDecodec := entity.(*ysanity_bgp.Bgp)

	suite.Equal(types.EntityEqual(&bgp, bgpDecodec), true)
}

func (suite *CodecTestSuite) TestXMLEncode1() {
	suite.Provider.Encoding = encoding.XML
	runner := ysanity.Runner{}
	configRunner(&runner)

	payload := suite.Codec.Encode(&suite.Provider, &runner)

	result := equalPayload(payload, xmlRunnerPayload, xml.Unmarshal, xml.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestXMLEncode2() {
	suite.Provider.Encoding = encoding.XML
	r1 := ysanity.Runner{}
	r1.Ytypes.BuiltInT.EnumValue = ysanity.YdkEnumTest_local

	payload := suite.Codec.Encode(&suite.Provider, &r1)
	result := equalPayload(payload, xmlRunnerPayload2, xml.Unmarshal, xml.Marshal)
	suite.Equal(result, true)
	ydk.YLogDebug(payload)
}

func (suite *CodecTestSuite) TestJSONEncode1() {
	suite.Provider.Encoding = encoding.JSON
	runner := ysanity.Runner{}
	configRunner(&runner)

	payload := suite.Codec.Encode(&suite.Provider, &runner)

	result := equalPayload(payload, jsonRunnerPayload, json.Unmarshal, json.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestJSONEncode2() {
	suite.Provider.Encoding = encoding.JSON
	r1 := ysanity.Runner{}
	r1.Ytypes.BuiltInT.EnumValue = ysanity.YdkEnumTest_local

	payload := suite.Codec.Encode(&suite.Provider, &r1)
	result := equalPayload(payload, jsonRunnerPayload2, json.Unmarshal, json.Marshal)
	suite.Equal(result, true)
}

func (suite *CodecTestSuite) TestXMLDecodeOCPattern() {
	suite.Provider.Encoding = encoding.XML
	objA := oc_pattern.OcA{}

	objA.A = "Hello"

	entity := suite.Codec.Decode(&suite.Provider, xmlOCPatternPayload)
	ocA := entity.(*oc_pattern.OcA)

	suite.Equal(types.EntityEqual(entity, ocA), true)
}

func (suite *CodecTestSuite) TestTypedefsXMLEncodeDecode() {
	systemEncode := ysanity_typedefs.System{}
	systemEncode.Id = 22
	systemEncode.Mode = ysanity_typedefs.TopMode_stand_alone

	suite.Provider.Encoding = encoding.XML

	payload := suite.Codec.Encode(&suite.Provider, &systemEncode)

	entity := suite.Codec.Decode(&suite.Provider, payload)
	systemDecode := entity.(*ysanity_typedefs.System)

	suite.Equal(types.EntityEqual(&systemEncode, systemDecode), true)
}

func (suite *CodecTestSuite) TestXMLEncodeDecodeMultiple() {

	runnerConfig := ysanity.Runner{}
	runnerConfig.Two.Number = 2

	nativeConfig := ysanity.Native{}
	nativeConfig.Version = "0.1.0"

	config := types.NewConfig(&runnerConfig, &nativeConfig)

	suite.Provider.Encoding = encoding.XML
	payload := suite.Codec.Encode(&suite.Provider, &config)

	entity := suite.Codec.Decode(&suite.Provider, payload)
	suite.Equal(types.IsEntityCollection(entity), true)

	// Check results
	ec := types.EntityToCollection(entity)
	suite.Equal(ec.Len(), 2)

	payload2 := suite.Codec.Encode(&suite.Provider, ec)
	suite.Equal(payload2, payload)
}

func (suite *CodecTestSuite) TestPassiveInterfaceCodec() {
	runner := ysanity.Runner{}
	ospf := ysanity.Runner_One_Ospf{}
	ospf.Id = 22
	ospf.PassiveInterface.Interface = "xyz"
	test := ysanity.Runner_One_Ospf_Test{}
	test.Name = "abc"
	ospf.Test = append(ospf.Test, &test)
	runner.One.Ospf = append(runner.One.Ospf, &ospf)
	suite.Provider.Encoding = encoding.XML
	payload := suite.Codec.Encode(&suite.Provider, &runner)
	suite.Equal(payload,
`<runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <one>
    <ospf xmlns="http://cisco.com/ns/yang/ydktest-sanity-augm">
      <id>22</id>
      <passive-interface>
        <interface>xyz</interface>
      </passive-interface>
      <test>
        <name>abc</name>
      </test>
    </ospf>
  </one>
</runner>
`)
	entity := suite.Codec.Decode(&suite.Provider, payload)
	runnerDecode := entity.(*ysanity.Runner)
	suite.Equal(types.EntityEqual(&runner, runnerDecode), true)
}

func (suite *CodecTestSuite) TestOneKeyList() {
	runner := ysanity.Runner{}
	configRunner(&runner)

	// Get first level list element
	_, ldata := ylist.Get(runner.TwoList.Ldata, 22)
	suite.NotNil(ldata)
	suite.Equal(types.EntityToString(ldata), "Type: *sanity.Runner_TwoList_Ldata, Path: ldata[number='22']")

	// Try non-existant key
	_, ldataNE := ylist.Get(runner.TwoList.Ldata, 222)
	suite.Nil(ldataNE)

	// Get second level list element
	sublist := ldata.(*ysanity.Runner_TwoList_Ldata).Subl1
	_, sublData:= ylist.Get(sublist, 221)
	suite.NotNil(sublData)
	suite.Equal(types.EntityToString(sublData), "Type: *sanity.Runner_TwoList_Ldata_Subl1, Path: subl1[number='221']")

	// Iterate over key list
	sublistKeys := ylist.Keys(sublist)
	suite.Equal(len(sublistKeys), 2)
	suite.Equal(fmt.Sprintf("%v", sublistKeys), "[221 222]")
	for _, key := range sublistKeys {
		_, entity := ylist.Get(sublist, key)
		suite.NotNil(entity)
		ydk.YLogDebug(fmt.Sprintf("For key: %v, Found Entity: %v", key, types.EntityToString(entity)))
	}

	// Remove element from the ylist
	i, rdata := ylist.Get(runner.TwoList.Ldata, 22)
	suite.Equal(i, 1)
	suite.NotNil(rdata)
	if rdata != nil {
		runner.TwoList.Ldata = append(runner.TwoList.Ldata[:i], runner.TwoList.Ldata[i+1:]...)
		suite.Equal(len(runner.TwoList.Ldata), 1)
		i, rdata = ylist.Get(runner.TwoList.Ldata, 22)
		suite.Nil(rdata)
	}
}

func (suite *CodecTestSuite) TestListNoKeys() {
	runner := ysanity.Runner{}
	t1 := ysanity.Runner_NoKeyList{Test: "t1"}
	t2 := ysanity.Runner_NoKeyList{Test: "t2"}
	t3 := ysanity.Runner_NoKeyList{Test: "t3"}
	runner.NoKeyList = []*ysanity.Runner_NoKeyList {&t1, &t2, &t3}

	suite.Provider.Encoding = encoding.JSON
	payload := suite.Codec.Encode(&suite.Provider, &runner)
	suite.Equal(jsonNoKeyList, payload)

	runnerDecode := suite.Codec.Decode(&suite.Provider, payload)
	suite.Equal(types.EntityEqual(&runner, runnerDecode), true)
}

func (suite *CodecTestSuite) TestLeafList() {
	runner := ysanity.Runner{}
	runner.Ytypes.BuiltInT.EnumLlist = append(runner.Ytypes.BuiltInT.EnumLlist, ysanity.YdkEnumTest_local)
	runner.Ytypes.BuiltInT.EnumLlist = append(runner.Ytypes.BuiltInT.EnumLlist, ysanity.YdkEnumTest_remote)

	payload := suite.Codec.Encode(&suite.Provider, &runner)
	fmt.Printf("%s\n", payload)
	runnerDecode := suite.Codec.Decode(&suite.Provider, payload)
	suite.True(types.EntityEqual(&runner, runnerDecode))
}

func (suite *CodecTestSuite) TestNative() {
	// Build loopback configuration
	address := ysanity.Native_Interface_Loopback_Ipv4_Address{}
	address.Ip = "2.2.2.2"
	address.PrefixLength = 32

	loopback := ysanity.Native_Interface_Loopback{}
	loopback.Name = 2222
	loopback.Ipv4.Address = append(loopback.Ipv4.Address, &address)

	native := ysanity.Native{}
        native.Interface.Loopback = append(native.Interface.Loopback, &loopback)

	suite.Provider.Encoding = encoding.JSON
	payload := suite.Codec.Encode(&suite.Provider, &native)
	fmt.Printf("%s\n", payload)
	runnerDecode := suite.Codec.Decode(&suite.Provider, payload)
	suite.Equal(types.EntityEqual(&native, runnerDecode), true)
}

func (suite *CodecTestSuite) TestBoolLists() {
	r := ysanity.Runner{}
	r.Ytypes.BuiltInT.BoolLeafList.append(true)
        r.Ytypes.BuiltInT.BoolLeafList.append(False)

        boolListElem = ysanity.Runner.Ytypes.BuiltInT.BoolList()
        boolListElem.BoolLeaf = true
        r.Ytypes.BuiltInT.BoolList.append(&boolListElem)

        xml := suite.Codec.Encode(&suite.Provider, &r)
        expected := '<runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <ytypes>
    <built-in-t>
      <bool-leaf-list>true</bool-leaf-list>
      <bool-leaf-list>false</bool-leaf-list>
      <bool-list>
        <bool-leaf>true</bool-leaf>
      </bool-list>
    </built-in-t>
  </ytypes>
</runner>
'
        suite.Equal(expected, xml)

        entity := suite.Codec.Decode(suite.Provider, xml)
        suite.True(types.EntityEqual(entity, &r)
}

func TestCodecTestSuite(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	suite.Run(t, new(CodecTestSuite))
}
