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

from ydk.types import Empty
from ydk.path import Repository
from ydk.providers import CodecServiceProvider
from ydk.services import CodecService
from ydk.entity_utils import XmlSubtreeCodec, JsonSubtreeCodec

from ydk.models.ydktest_yang11.ydktest_sanity_yang11 import BackwardIncompatible, EmptyType
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

    # def test_container(self):
    #     # Create container
    #     container = BackwardIncompatible()
    #     container.test_node = 'Testing node'
    #     self.crud.create(self.ncc, container)
    #
    #     # Read container
    #     container_read = self.crud.read(self.ncc, BackwardIncompatible())
    #     self.assertIsNotNone(container_read)
    #
    #     # Compare containers
    #     self.assertEqual(container, container_read)

#     def test_anyxml_action(self):
#         expected = '''<data xmlns="http://cisco.com/ns/yang/ydktest-action">
#   <action-node>
#     <test>xyz</test>
#   </action-node>
# </data>
# '''
#         rpc = self.root_schema.create_datanode("ydktest-sanity-action:data", "")
#         a = rpc.create_action("action-node")
#         a.create_datanode("test", "xyz")
#
#         xml = self.codec.encode(rpc, EncodingFormat.XML)
#         self.assertEqual(xml, expected)
#
#         try:
#             rpc(self.ncs)
#         except Exception as e:
#             self.assertTrue(isinstance(e, RuntimeError))

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
        self.assertIsNotNone(payload)
        self.assertIsNot('', payload)

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
