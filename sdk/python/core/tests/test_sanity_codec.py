#  ----------------------------------------------------------------
# Copyright 2016-2019 Cisco Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------
# This file has been modified by Yan Gorelik, YDK Solutions.
# All modifications in original under CiscoDevNet domain
# introduced since October 2019 are copyrighted.
# All rights reserved under Apache License, Version 2.0.
# ------------------------------------------------------------------

"""
test_sanity_codec.py
sanity test for CodecService and CodecServiceProvider
"""

import unittest

try:
    from ydk.models.ydktest.ydktest_sanity import Runner, Native, YdkEnumTest
    from ydk.models.ydktest.openconfig_routing_policy import RoutingPolicy
    from ydk.models.ydktest.oc_pattern import OcA
    from ydk.models.ydktest.ydktest_sanity_typedefs import System, TopMode
except ImportError:
    from ydk.models.ydktest.ydktest_sanity.runner.runner import Runner
    from ydk.models.ydktest.ydktest_sanity.native.native import Native
    from ydk.models.ydktest.ydktest_sanity.ydktest_sanity import YdkEnumTest
    from ydk.models.ydktest import openconfig_routing_policy
    from ydk.models.ydktest.openconfig_routing_policy.routing_policy.routing_policy import RoutingPolicy
    from ydk.models.ydktest.oc_pattern.oc_a.oc_a import OcA
    from ydk.models.ydktest.ydktest_sanity_typedefs.system.system import System
    from ydk.models.ydktest.ydktest_sanity_typedefs.ydktest_sanity_typedefs import TopMode

from ydk.providers import CodecServiceProvider
from ydk.services import CodecService
from ydk.errors import YServiceError
from ydk.types import EncodingFormat

from test_utils import assert_with_error

_xml_enum_payload_1 = '''<built-in-t xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <enum-value>local</enum-value>
</built-in-t>
'''

_json_enum_payload_1 = """{
  "ydktest-sanity:built-in-t": {
    "enum-value": "local"
  }
}
"""

_xml_enum_payload_2 = '''<runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <ytypes>
    <built-in-t>
      <enum-value>local</enum-value>
    </built-in-t>
  </ytypes>
</runner>
'''

_xml_runner_payload = '''<runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <two-list>
    <ldata>
      <number>21</number>
      <name>runner:twolist:ldata[21]:name</name>
      <subl1>
        <number>211</number>
        <name>runner:twolist:ldata[21]:subl1[211]:name</name>
      </subl1>
      <subl1>
        <number>212</number>
        <name>runner:twolist:ldata[21]:subl1[212]:name</name>
      </subl1>
    </ldata>
    <ldata>
      <number>22</number>
      <name>runner:twolist:ldata[22]:name</name>
      <subl1>
        <number>221</number>
        <name>runner:twolist:ldata[22]:subl1[221]:name</name>
      </subl1>
      <subl1>
        <number>222</number>
        <name>runner:twolist:ldata[22]:subl1[222]:name</name>
      </subl1>
    </ldata>
  </two-list>
</runner>
'''

_json_runner_payload = """{
  "ydktest-sanity:runner": {
    "two-list": {
      "ldata": [
        {
          "number": 21,
          "name": "runner:twolist:ldata[21]:name",
          "subl1": [
            {
              "number": 211,
              "name": "runner:twolist:ldata[21]:subl1[211]:name"
            },
            {
              "number": 212,
              "name": "runner:twolist:ldata[21]:subl1[212]:name"
            }
          ]
        },
        {
          "number": 22,
          "name": "runner:twolist:ldata[22]:name",
          "subl1": [
            {
              "number": 221,
              "name": "runner:twolist:ldata[22]:subl1[221]:name"
            },
            {
              "number": 222,
              "name": "runner:twolist:ldata[22]:subl1[222]:name"
            }
          ]
        }
      ]
    }
  }
}
"""

_json_oc_pattern_payload = '''{
  "oc-pattern:oc-A": [
    {
      "a": "Hello",
      "B": {
        "b": "Hello"
      }
    }
  ]
}
'''


def _get_runner_entity():
    r_1 = Runner()
    e_1, e_2 = Runner.TwoList.Ldata(), Runner.TwoList.Ldata()
    e_11, e_12 = Runner.TwoList.Ldata.Subl1(), Runner.TwoList.Ldata.Subl1()
    e_1.number = 21
    e_1.name = 'runner:twolist:ldata[' + str(e_1.number) + ']:name'
    e_11.number = 211
    e_11.name = 'runner:twolist:ldata[' + str(e_1.number) + ']:subl1[' + str(e_11.number) + ']:name'
    e_12.number = 212
    e_12.name = 'runner:twolist:ldata[' + str(e_1.number) + ']:subl1[' + str(e_12.number) + ']:name'
    e_1.subl1.extend([e_11, e_12])
    e_21, e_22 = Runner.TwoList.Ldata.Subl1(), Runner.TwoList.Ldata.Subl1()
    e_2.number = 22
    e_2.name = 'runner:twolist:ldata[' + str(e_2.number) + ']:name'
    e_21.number = 221
    e_21.name = 'runner:twolist:ldata[' + str(e_2.number) + ']:subl1[' + str(e_21.number) + ']:name'
    e_22.number = 222
    e_22.name = 'runner:twolist:ldata[' + str(e_2.number) + ']:subl1[' + str(e_22.number) + ']:name'
    e_2.subl1.extend([e_21, e_22])
    r_1.two_list.ldata.extend([e_1, e_2])
    return r_1


class SanityYang(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        self.codec = CodecService()
        self.provider = CodecServiceProvider(type='xml')
        self.json_provider = CodecServiceProvider(type='json')

    def test_xml_encode_1(self):
        r_1 = _get_runner_entity()
        payload = self.codec.encode(self.provider, r_1)
        self.assertEqual(_xml_runner_payload, payload)

        ldata_list = r_1.two_list.ldata
        ldata_keys = ldata_list.keys()
        self.assertEqual(ldata_keys, ['21', '22'])

        for lkey in ldata_keys:
            ldata = ldata_list[lkey]
            self.assertNotEqual(ldata, None)

        ldata_21 = ldata_list['21']
        self.assertEqual(ldata_21.number, 21)
        self.assertEqual(ldata_21.name, 'runner:twolist:ldata[21]:name')

        subl_21 = ldata_21.subl1
        subl_21_keys = subl_21.keys()
        self.assertEqual(subl_21_keys, ['211', '212'])
        subl_21_212 = subl_21['212']
        self.assertEqual(subl_21_212.name, 'runner:twolist:ldata[21]:subl1[212]:name')

    def test_xml_encode_2(self):
        r_1 = Runner.Ytypes.BuiltInT()
        r_1.enum_value = YdkEnumTest.local

        payload = self.codec.encode(self.provider, r_1)
        self.assertEqual(_xml_enum_payload_1, payload)

    @assert_with_error("'provider' and 'entity_holder' cannot be None", YServiceError)
    def test_encode_invalid_1(self):
        self.codec.encode(self.provider, None)

    @assert_with_error("'provider' and 'entity_holder' cannot be None", YServiceError)
    def test_encode_invalid_2(self):
        self.codec.encode(None, _get_runner_entity())

    @assert_with_error("'provider' and 'entity_holder' cannot be None", YServiceError)
    def test_encode_invalid_3(self):
        self.codec.encode(None, None)

    def test_xml_decode_1(self):
        entity = self.codec.decode(self.provider, _xml_enum_payload_2)
        self.assertEqual(
            _xml_enum_payload_2, self.codec.encode(self.provider, entity))

    @assert_with_error("'provider' and 'payload_holder' cannot be None", YServiceError)
    def test_decode_invalid_1(self):
        self.codec.decode(None, _xml_enum_payload_2)

    @assert_with_error("'provider' and 'payload_holder' cannot be None", YServiceError)
    def test_decode_invalid_2(self):
        self.codec.decode(self.provider, None)

    @assert_with_error("'provider' and 'payload_holder' cannot be None", YServiceError)
    def test_decode_invalid_3(self):
        self.codec.decode(None, None)

    def test_xml_encode_decode(self):
        r_1 = _get_runner_entity()
        payload = self.codec.encode(self.provider, r_1)
        entity = self.codec.decode(self.provider, payload)

        self.assertEqual(r_1, entity)
        self.assertEqual(payload, self.codec.encode(self.provider, entity))

    def test_xml_encode_decode_dict(self):
        r_1 = _get_runner_entity()
        r_entity = {'ydktest-sanity': r_1}
        payload = self.codec.encode(self.provider, r_entity)
        entity = self.codec.decode(self.provider, payload)
        for module in entity:
            self.assertEqual(r_entity[module], entity[module])
        self.assertEqual(payload, self.codec.encode(self.provider, entity))

    def test_xml_decode_oc_pattern(self):
        obj_a = OcA()
        obj_a.a = 'Hello'

        xml_oc_pattern_payload = '''<oc-A xmlns="http://cisco.com/ns/yang/oc-pattern">
          <a>Hello</a>
        </oc-A>
        '''

        entity = self.codec.decode(self.provider, xml_oc_pattern_payload)

        self.assertEqual(obj_a.a, entity.a)

    # JSON

    def test_json_encode_1(self):
        entity = _get_runner_entity()
        payload = self.codec.encode(self.json_provider, entity)
        self.assertEqual(_json_runner_payload, payload)

    def test_json_encode_2(self):
        r_1 = Runner.Ytypes.BuiltInT()
        r_1.enum_value = YdkEnumTest.local

        payload = self.codec.encode(self.json_provider, r_1)
        self.assertEqual(_json_enum_payload_1, payload)

    def test_json_decode_1(self):
        entity = self.codec.decode(self.json_provider, _json_runner_payload)
        payload = self.codec.encode(self.json_provider, entity)
        self.assertEqual(_json_runner_payload, payload)

    def test_json_encode_decode(self):
        runner = _get_runner_entity()
        payload = self.codec.encode(self.json_provider, runner)
        entity = self.codec.decode(self.json_provider, payload)
        self.assertEqual(runner, entity)
        self.assertEqual(payload, self.codec.encode(self.json_provider, entity))

    def test_json_encode_decode_dict(self):
        entity = _get_runner_entity()
        entity_holder = {'ydktest-sanity': entity}
        payload_holder = self.codec.encode(self.json_provider, entity_holder)
        entities = self.codec.decode(self.json_provider, payload_holder)
        for module in entities:
            self.assertEqual(entities[module], entities[module])
            self.assertEqual(payload_holder[module],
                             self.codec.encode(self.json_provider, entities[module]))

    def test_json_encode_oc_pattern(self):
        obj_a = OcA()
        obj_a.a = 'Hello'
        obj_a.b.b = 'Hello'
        json_payload = self.codec.encode(self.json_provider, obj_a)
        self.assertEqual(_json_oc_pattern_payload, json_payload)

    @unittest.skip('YCoreError: Unknown element "oc-A".. Path:')
    def test_json_decode_oc_pattern(self):
        entity = self.codec.decode(self.json_provider, _json_oc_pattern_payload)

        self.assertEqual(entity.a.get(), 'Hello')
        self.assertEqual(entity.b.b.get(), 'Hello')

    def test_xml_subtree(self):
        r_1 = _get_runner_entity()
        payload = self.codec.encode(self.provider, r_1, subtree=True)
        self.assertEqual(_xml_runner_payload[:-1], payload)

        r_2 = self.codec.decode(self.provider, payload, subtree=True)
        self.assertEqual(r_1, r_2)

    @unittest.skip('Failing encode entity')
    def test_embedded_quote_leaflist_value(self):
        """<routing-policy xmlns="http://openconfig.net/yang/routing-policy">
  <defined-sets>
    <bgp-defined-sets xmlns="http://openconfig.net/yang/bgp-policy">
      <community-sets>
        <community-set>
          <community-set-name>COMMUNITY-SET1</community-set-name>
          <config>
            <community-set-name>COMMUNITY-SET1</community-set-name>
            <community-member>ios-regex '^65172:17...$'</community-member>
            <community-member>65172:16001</community-member>
          </config>
          <state>
            <community-set-name>COMMUNITY-SET1</community-set-name>
            <community-member>ios-regex '^65172:17...$'</community-member>
            <community-member>65172:16001</community-member>
          </state>
        </community-set>
      </community-sets>
    </bgp-defined-sets>
  </defined-sets>
</routing-policy>
"""
        routing_policy = RoutingPolicy()

        com = RoutingPolicy.DefinedSets.BgpDefinedSets.CommunitySets.CommunitySet()
        com.community_set_name = "COMMUNITY-SET1"
        com.config.community_set_name = "COMMUNITY-SET1"
        com.config.community_member.append("ios-regex '^65172:17...$'")
        com.config.community_member.append("65172:16001")

        com.state.community_set_name = "COMMUNITY-SET1"
        com.state.community_member.append("ios-regex '^65172:17...$'")
        com.state.community_member.append("65172:16001")

        routing_policy.defined_sets.bgp_defined_sets.community_sets.community_set.append(com)
        payload = self.codec.encode(self.provider, routing_policy)
        self.assertFalse(payload == "")  # TODO failing when bundle built with --one-module-per-class option

        routing_policy_decode = self.codec.decode(self.provider, payload)
        if routing_policy == routing_policy_decode:
            self.assertEqual(routing_policy, routing_policy_decode)

    def test_list_no_keys(self):
        payload = '''<runner xmlns="http://cisco.com/ns/yang/ydktest-sanity">
  <no-key-list>
    <test>abc</test>
  </no-key-list>
  <no-key-list>
    <test>xyz</test>
  </no-key-list>
</runner>'''
        no_key = self.codec.decode(self.provider, payload)
        no_key_payload = self.codec.encode(self.provider, no_key, subtree=True)
        self.assertEqual(payload, no_key_payload)

    def test_anyxml(self):
        payload = '<?xml version="1.0"?><runner xmlns="http://cisco.com/ns/yang/ydktest-sanity"/>'
        result = self.codec.decode(self.provider, payload)
        self.assertIsNotNone(result)

        payload = '''<?xml version="1.0"?>
        <runner xmlns="http://cisco.com/ns/yang/ydktest-sanity"/>'''
        result = self.codec.decode(self.provider, payload)
        self.assertIsNotNone(result)

    @assert_with_error("Subtree option can only be used with XML encoding", YServiceError)
    def test_decode_invalid_subtree_1(self):
        self.codec.decode(self.json_provider, '{"ydktest-sanity:runner": {}}', subtree=True)

    @assert_with_error("Subtree option can only be used with XML encoding", YServiceError)
    def test_decode_invalid_subtree_2(self):
        self.codec.encode(self.json_provider, Runner(), subtree=True)

    def test_encode_decode_typedefs(self):
        system_encode = System()
        system_encode.mode = TopMode.stand_alone
        system_encode.id = 22

        payload = self.codec.encode(self.provider, system_encode)

        system_decode = self.codec.decode(self.provider, payload)
        self.assertEqual(system_encode, system_decode)

    def test_encode_decode_list(self):
        runner = Runner()
        runner.two.number = 2

        native = Native()
        native.version = '0.1.0'

        xml_encode = self.codec.encode(self.provider, [runner, native])

        entity_list = self.codec.decode(self.provider, xml_encode)
        self.assertEqual(entity_list, [runner, native])

    def test_codec_json(self):
        runner = Runner()
        runner.two.number = 2

        native = Native()
        native.version = '0.1.0'

        json_encode = self.codec.encode(self.json_provider, [runner, native])

        entity_list = self.codec.decode(self.json_provider, json_encode)
        self.assertEqual(entity_list, [runner, native])

    def test_passive_codec(self):
        e='''<runner xmlns="http://cisco.com/ns/yang/ydktest-sanity"><passive><name>xyz</name><interfac><test>abc</test></interfac><testc xmlns="http://cisco.com/ns/yang/ydktest-sanity-augm"><xyz><xyz>25</xyz></xyz></testc></passive></runner>'''
        runner = Runner()
        p = runner.Passive()
        p.name = "xyz"
        i = runner.Passive.Interfac()
        i.test = "abc"
        p.interfac.append(i)
        p.testc.xyz = runner.Passive.Testc.Xyz()
        p.testc.xyz.xyz = 25
        runner.passive.append(p)

        x = self.codec.encode(self.provider, runner, False)
        self.assertEqual(x, e)


if __name__ == '__main__':
    import sys
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityYang)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
