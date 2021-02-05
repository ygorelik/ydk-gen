# -----------------------------------------------------------------------
# YDK - YANG Development Kit
#
# Copyright 2020 Yan Gorelik, YDK Solutions.
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
import os
import sys
import unittest
import logging

from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService
from ydk.path import NetconfSession, Codec, Repository
from ydk.types import EncodingFormat, Empty
from ydk.providers import CodecServiceProvider
from ydk.services import CodecService
from ydk.errors import YServiceError

from ydk.models.ydktest_yang11.ydktest_sanity_yang11 import BackwardIncompatible, EmptyType


# try:
#     from ydk.models.ydktest_yang11.ydktest_sanity_yang11 import BackwardIncompatible
#     from ydk.models.ydktest_yang11.ydktest_sanity_action import Data
# except ImportError:
#     # from ydk.models.ydktest_yang11.ydktest_sanity_yang11.backward_incompatible.backward_incompatible import BackwardIncompatible
#     from ydk.models.ydktest_yang11.ydktest_sanity_action.data.data import Data

from test_utils import ParametrizedTestCase
from test_utils import get_device_info, enable_logging


class SanityYang11Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # model_path = os.path.dirname(os.path.abspath(__file__)) + '/../../../cpp/core/tests/models'
        # repo = Repository(model_path)
        # cls.ncs = NetconfSession(repo,
        #                          cls.hostname,
        #                          cls.username,
        #                          cls.password,
        #                          cls.port,
        #                          cls.protocol,
        #                          cls.on_demand,
        #                          cls.timeout)
        # cls.crud = CRUDService()
        # cls.root_schema = cls.ncs.get_root_schema()
        # cls.codec = Codec()
        cls.codec_service = CodecService()
        cls.codec_provider = CodecServiceProvider(type='xml')
        enable_logging(logging.DEBUG)

    def setUp(self):
        pass

    # def tearDown(self):
    #     container = BackwardIncompatible()
    #     self.crud.delete(self.ncc, container)

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

    def test_union(self):
        top = EmptyType()
        list_elem = EmptyType.Filter()
        list_elem.name = 'filter-name'
        list_elem.enabled = True
        list_elem.prop = '1'
        list_elem.outbound_filter = 'filter-name'
        top.filter.append(list_elem)

        payload = self.codec_service.encode(self.codec_provider, top)
        self.assertIsNotNone(payload)
        self.assertIsNot('', payload)
        print(payload)


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
