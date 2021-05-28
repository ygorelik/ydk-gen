# -----------------------------------------------------------------------
# YDK - YANG Development Kit
#
# Copyright 2020-2021 Yan Gorelik, YDK Solutions.
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
# ------------------------------------------------------------------------

import sys
import unittest
import logging

from ydk.types import Empty, Bits, EncodingFormat
from ydk.path import Repository, Codec
from ydk.providers import CodecServiceProvider
from ydk.services import CodecService
from ydk.entity_utils import XmlSubtreeCodec, JsonSubtreeCodec
from ydk.errors import YModelError

from ydk.models.ydktest_yang11.ydktest_sanity_yang11 import BackwardIncompatible, EmptyType, AnydataType
from ydk.models.ydktest_yang11.ydktest_sanity_yang11 import SslKey
from ydk.models.ydktest_yang11.ydktest_sanity_yang11 import BaseColors

import ydk.models.ydktest_yang11 as yang11

from test_utils import ParametrizedTestCase
from test_utils import get_device_info, enable_logging


class SanityYang11Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.codec_service = CodecService()
        cls.codec_provider = CodecServiceProvider(type='xml')
        cls.json_codec_provider = CodecServiceProvider(type='json')
        enable_logging(logging.ERROR)

    def test_anyxml_action(self):
        expected = '''<data xmlns="http://cisco.com/ns/yang/ydktest-action">
  <action-node>
    <test>xyz</test>
  </action-node>
</data>
'''
        repo = Repository(yang11.__path__[0] + '/_yang')
        root_schema = repo.create_root_schema([])
        rpc = root_schema.create_datanode("ydktest-sanity-action:data", "")
        a = rpc.create_action("action-node")
        a.create_datanode("test", "xyz")

        codec = Codec()
        xml = codec.encode(rpc, EncodingFormat.XML)
        self.assertEqual(expected, xml)

    def test_type_empty_key(self):
        top = EmptyType()
        list_elem = EmptyType.Filter()
        list_elem.name = 'filter-name'
        list_elem.enabled = Empty()
        list_elem.prop = '1'
        list_elem.outbound_filter = Empty()
        top.filter.append(list_elem)

        payload = self.codec_service.encode(self.codec_provider, top)
        self.assertIsNotNone(payload)
        self.assertIsNot('', payload)

        entity = self.codec_service.decode(self.codec_provider, payload)
        self.assertEqual(top, entity)

        self.assertEqual(top.filter.keys(), ['filter-name'])
        self.assertEqual(list_elem, top.filter['filter-name'])

    def test_type_empty_key_xml_codec(self):
        top = EmptyType()
        elem1, elem2 = EmptyType.Filter(), EmptyType.Filter()
        elem1.name, elem2.name = 'abc', 'xyz'
        elem1.enabled, elem2.enabled = Empty(), Empty()
        elem1.prop, elem2.prop = 'one', 'two'
        # elem1.outbound_filter, elem2.outbound_filter = 'abc', 'xyz'
        elem1.outbound_filter, elem2.outbound_filter = Empty(), Empty()
        top.filter.extend([elem1, elem2])

        self.assertEqual(top.filter.keys(), ['abc', 'xyz'])
        self.assertEqual(elem2, top.filter['xyz'])

        repo = Repository(yang11.__path__[0] + '/_yang')
        root_schema = repo.create_root_schema([])
        xml_codec = XmlSubtreeCodec()

        payload = xml_codec.encode(top, root_schema)
        expected = '''<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>abc</name>
    <enabled/>
    <prop>one</prop>
    <outbound-filter/>
  </filter>
  <filter>
    <name>xyz</name>
    <enabled/>
    <prop>two</prop>
    <outbound-filter/>
  </filter>
</empty-type>'''
        self.assertEqual(expected, payload)

        entity = xml_codec.decode(payload, EmptyType())
        self.assertEqual(top, entity)

    def test_type_empty_key_json_codec(self):
        top = EmptyType()
        elem1, elem2 = EmptyType.Filter(), EmptyType.Filter()
        elem1.name, elem2.name = 'abc', 'xyz'
        elem1.enabled, elem2.enabled = Empty(), Empty()
        elem1.prop, elem2.prop = 'one', 'two'
        elem1.outbound_filter, elem2.outbound_filter = Empty(), Empty()
        top.filter.extend([elem1, elem2])

        repo = Repository(yang11.__path__[0] + '/_yang')
        root_schema = repo.create_root_schema([])
        json_codec = JsonSubtreeCodec()

        payload = json_codec.encode(top, root_schema, True)
        self.assertIsNotNone(payload)
        self.assertIsNot('', payload)

        entity = json_codec.decode(payload, EmptyType())
        self.assertEqual(top, entity)

    def test_anydata(self):
        top = AnydataType()
        payload = self.codec_service.encode(self.codec_provider, top, False)
        self.assertEqual('''<anydata-type xmlns="http://cisco.com/ns/yang/ydktest-yang11"/>''', payload)

        payload = '''<anydata-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <logged-notification>
    <time>2014-07-29T13:43:12Z</time>
    <data>
      <![CDATA[
      <notification xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
        <eventTime>2014-07-29T13:43:01Z</eventTime>
        <event xmlns="urn:example:event">
          <event-class>fault</event-class>
          <reporting-entity>
            <card>Ethernet0</card>
          </reporting-entity>
          <severity>major</severity>
        </event>
      </notification>
      ]]>
    </data>
  </logged-notification>
</anydata-type>
'''
        entity_data = self.codec_service.decode(self.codec_provider, payload)
        self.assertIsNotNone(entity_data)
        self.assertEqual(len(entity_data.logged_notification), 1)
        notification = entity_data.logged_notification[0]
        self.assertTrue('<card>Ethernet0</card>' in notification.data)

    def test_duplicate_values_in_leaflist_xml(self):
        payload = '''<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <non-unique>abc</non-unique>
  <non-unique>abc</non-unique>
  <non-unique>abc</non-unique>
</backward-incompatible>
'''
        entity = self.codec_service.decode(self.codec_provider, payload)
        self.assertIsNotNone(entity)
        self.assertEqual(len(entity.non_unique), 3)
        self.assertEqual(entity.non_unique[2], 'abc')

        xml_codec = XmlSubtreeCodec()

        entity2 = xml_codec.decode(payload, BackwardIncompatible())
        self.assertEqual(entity, entity2)

    def test_duplicate_values_in_leaflist_json(self):
        payload = '''
{
  "ydktest-sanity-yang11:backward-incompatible": {
    "non-unique": [
      "abc",
      "abc",
      "abc"
     ]
  }
}
'''
        entity = self.codec_service.decode(self.json_codec_provider, payload)
        self.assertIsNotNone(entity)
        self.assertEqual(len(entity.non_unique), 3)
        self.assertEqual(entity.non_unique[2], 'abc')

        json_codec = JsonSubtreeCodec()

        entity2 = json_codec.decode(payload, BackwardIncompatible())
        self.assertEqual(entity, entity2)

    def test_derived_identity_type(self):
        top = BackwardIncompatible()
        top.key = SslKey()

        xml = self.codec_service.encode(self.codec_provider, top, False)
        self.assertIsNotNone(xml)
        self.assertEqual('''<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11"><key>ssl-key</key></backward-incompatible>''', xml)

        entity = self.codec_service.decode(self.codec_provider, xml)
        self.assertEqual(top, entity)

    def test_pattern_modifier(self):
        top = BackwardIncompatible()
        top.invert = '++++'  # inverted of pattern "[0-9a-fA-F]*"
        xml = self.codec_service.encode(self.codec_provider, top, False)
        self.assertEqual('''<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11"><invert>++++</invert></backward-incompatible>''', xml)

        top.invert = '1234'
        with self.assertRaises(YModelError):
            self.codec_service.encode(self.codec_provider, top)

    def test_choice_shortcut(self):
        top = BackwardIncompatible()
        top.ethernet = Empty()
        xml = self.codec_service.encode(self.codec_provider, top, False)
        self.assertEqual('''<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11"><ethernet/></backward-incompatible>''', xml)

        entity = self.codec_service.decode(self.codec_provider, xml)
        self.assertEqual(top, entity)

    def test_enum_subtyping(self):
        top = BackwardIncompatible()
        top.my_color = BaseColors.yellow    # value 'yellow' is not included to enum subtype, so expecting error
        with self.assertRaises(YModelError):
            self.codec_service.encode(self.codec_provider, top)

        top.my_color = BaseColors.white
        xml = self.codec_service.encode(self.codec_provider, top, False)
        self.assertEqual('''<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11"><my-color>white</my-color></backward-incompatible>''', xml)

        entity = self.codec_service.decode(self.codec_provider, xml)
        self.assertEqual(top, entity)

    def test_bits_subtyping(self):
        top = BackwardIncompatible()
        bit = Bits()
        bit['ten-mb-only'] = True    # bit value 'ten-mb-only' is not included to bits subtype, so expecting error
        top.my_bits.append(bit)
        with self.assertRaises(YModelError):
            self.codec_service.encode(self.codec_provider, top)

        bit_0, bit_1 = Bits(), Bits()
        bit_0['disable-nagle'] = True
        bit_1['auto-sense-speed'] = True
        top.my_bits.clear()
        top.my_bits.extend([bit_0, bit_1])

        xml = self.codec_service.encode(self.codec_provider, top)
        expected = '''<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <my_bits>disable-nagle</my_bits>
  <my_bits>auto-sense-speed</my_bits>
</backward-incompatible>
'''
        self.assertEqual(expected, xml)

        entity = self.codec_service.decode(self.codec_provider, xml)
        self.assertEqual(top, entity)

    def test_bits_subtyping_json_codec(self):
        top = BackwardIncompatible()
        bit_0, bit_1 = Bits(), Bits()
        bit_0['disable-nagle'] = True
        bit_1['auto-sense-speed'] = True
        top.my_bits.clear()
        top.my_bits.extend([bit_0, bit_1])

        expected = '''{
  "ydktest-sanity-yang11:backward-incompatible": {
    "my_bits": [
      "disable-nagle",
      "auto-sense-speed"
    ]
  }
}'''
        repo = Repository(yang11.__path__[0] + '/_yang')
        root_schema = repo.create_root_schema([])
        json_codec = JsonSubtreeCodec()

        payload = json_codec.encode(top, root_schema, True)
        self.assertEqual(expected, payload)

        entity = json_codec.decode(payload, BackwardIncompatible())
        self.assertEqual(top, entity)


if __name__ == '__main__':
    device, non_demand, common_cache, timeout = get_device_info()

    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(
        SanityYang11Test,
        device=device,
        non_demand=non_demand,
        common_cache=common_cache,
        timeout=timeout))
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
