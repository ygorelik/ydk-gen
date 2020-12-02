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

import sys
import unittest
import logging

from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService

try:
    from ydk.models.ydktest.ydktest_sanity_yang11 import BackwardIncompatible
    from ydk.models.ydktest.ydktest_sanity_action import Data
except ImportError:
    from ydk.models.ydktest.ydktest_sanity_yang11.backward_incompatible.backward_incompatible import BackwardIncompatible
    from ydk.models.ydktest.ydktest_sanity_action.data.data import Data

from test_utils import ParametrizedTestCase
from test_utils import get_device_info, enable_logging


class SanityYang11Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ncc = NetconfServiceProvider(
            cls.hostname,
            cls.username,
            cls.password,
            cls.port,
            cls.protocol,
            cls.on_demand,
            cls.common_cache,
            cls.timeout)
        cls.crud = CRUDService()
        enable_logging(logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        container = BackwardIncompatible()
        self.crud.delete(self.ncc, container)

    def test_container(self):
        # Create container
        container = BackwardIncompatible()
        container.test_node = 'Testing node'
        self.crud.create(self.ncc, container)

        # Read container
        container_read = self.crud.read(self.ncc, BackwardIncompatible())
        self.assertIsNotNone(container_read)

        # Compare containers
        self.assertEqual(container, container_read)

    # def test_anyxml_action(self):
    #     data = Data()
    #     data.action_node.test = 'xyz'
    #     self.crud.create(self.ncc, data)


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
