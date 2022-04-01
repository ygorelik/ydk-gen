#  ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
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
test_non_top_operations.py
Sanity test for ydktest-sanity.yang targeted specifically
to test support for non-top level objects in CRUD operations
"""

from __future__ import absolute_import
from __future__ import print_function

import unittest

from ydk.providers import NetconfServiceProvider
from ydk.services  import CRUDService, NetconfService
from ydk.filters import YFilter
from ydk.ext.services import Datastore

try:
    from ydk.models.ydktest.ydktest_sanity import Runner, ChildIdentity, Native
except ImportError:
    from ydk.models.ydktest.ydktest_sanity.runner.runner import Runner
    from ydk.models.ydktest.ydktest_sanity.native.native import Native
    from ydk.models.ydktest.ydktest_sanity.ydktest_sanity import ChildIdentity


class SanityTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ncc = NetconfServiceProvider(
            "127.0.0.1",
            "admin",
            "admin",
            12022,
            )
        cls.crud = CRUDService()

    def setUp(self):
        runner = Runner()
        self.crud.delete(self.ncc, runner)

    def test_delete_on_list_with_identitykey(self):
        a1 = Runner.OneList.IdentityList()
        a1.config.id = ChildIdentity()
        a1.id_ref = a1.config.id
        self.crud.create(self.ncc, a1)

        k = Runner.OneList.IdentityList()
        k.config.id = ChildIdentity()
        k.id_ref = k.config.id
        k.yfilter = YFilter.delete
        self.crud.update(self.ncc, k)

        runner_read = self.crud.read(self.ncc, Runner())
        self.assertIsNone(runner_read)

    def test_iden_list(self):
        # CREATE
        il = Runner.OneList.IdentityList()
        il.config.id = ChildIdentity()
        il.id_ref = ChildIdentity()
        self.crud.create(self.ncc, il)

        # READ & VALIDATE
        runner_filter = Runner()
        read_one = self.crud.read(self.ncc, runner_filter.one_list)
        self.assertIsNotNone(read_one)

        read_il = read_one.identity_list.get(ChildIdentity().to_string())
        self.assertIsNotNone(read_il)
        read_il.parent = None
        self.assertEqual(read_il, il)

        # DELETE & VALIDATE
        self.crud.delete(self.ncc, il)
        runner_read = self.crud.read(self.ncc, Runner())
        self.assertIsNone(runner_read)

    def test_crud_delete_container(self):
        # Build loopback configuration
        address = Native.Interface.Loopback.Ipv4.Address()
        address.ip = "2.2.2.2"
        address.netmask = "255.255.255.255"

        loopback = Native.Interface.Loopback()
        loopback.name = 2222
        loopback.ipv4.address.append(address)

        native = Native()
        native.interface.loopback.append(loopback)

        crud = CRUDService()
        result = crud.create(self.ncc, native)
        self.assertTrue(result)

        # Read ipv4 configuration
        native = Native()
        loopback = Native.Interface.Loopback()
        loopback.name = 2222
        native.interface.loopback.append(loopback)
        ipv4_config = crud.read(self.ncc, loopback.ipv4)
        self.assertIsNotNone(ipv4_config)
        self.assertEqual(ipv4_config.address['2.2.2.2'].netmask, "255.255.255.255")

        # Remove ipv4 configuration
        native = Native()
        loopback = Native.Interface.Loopback()
        loopback.name = 2222
        native.interface.loopback.append(loopback)
        result = crud.delete(self.ncc, loopback.ipv4)
        self.assertTrue(result)

        # Delete configuration
        native = Native()
        result = crud.delete(self.ncc, native)
        self.assertEqual(result, True)

    def test_netconf_delete_container(self):
        # Build loopback configuration
        address = Native.Interface.Loopback.Ipv4.Address()
        address.ip = "2.2.2.2"
        address.netmask = "255.255.255.255"

        loopback = Native.Interface.Loopback()
        loopback.name = 2222
        loopback.ipv4.address.append(address)

        native = Native()
        native.interface.loopback.append(loopback)

        ns = NetconfService()
        result = ns.edit_config(self.ncc, Datastore.candidate, native)
        self.assertTrue(result)

        # Read ipv4 configuration
        native = Native()
        loopback = Native.Interface.Loopback()
        loopback.name = 2222
        native.interface.loopback.append(loopback)
        ipv4_config = ns.get_config(self.ncc, Datastore.candidate, loopback.ipv4)
        self.assertIsNotNone(ipv4_config)
        self.assertEqual(ipv4_config.address['2.2.2.2'].netmask, "255.255.255.255")

        # Delete configuration
        result = ns.discard_changes(self.ncc)
        self.assertEqual(result, True)

    def test_twolist_non_top(self):
        # CREATE
        r_1, r_2 = Runner(), Runner()
        e_1, e_2 = Runner.TwoList.Ldata(), Runner.TwoList.Ldata()
        e_11, e_12 = Runner.TwoList.Ldata.Subl1(), Runner.TwoList.Ldata.Subl1()
        e_1.number = 21
        e_1.name = 'runner:twolist:ldata['+str(e_1.number)+']:name'
        e_11.number = 211
        e_11.name = 'runner:twolist:ldata['+str(e_1.number)+']:subl1['+str(e_11.number)+']:name'
        e_12.number = 212
        e_12.name = 'runner:twolist:ldata['+str(e_1.number)+']:subl1['+str(e_12.number)+']:name'
        e_1.subl1.append(e_11)
        e_1.subl1.append(e_12)
        e_21, e_22 = Runner.TwoList.Ldata.Subl1(), Runner.TwoList.Ldata.Subl1()
        e_2.number = 22
        e_2.name = 'runner:twolist:ldata['+str(e_2.number)+']:name'
        e_21.number = 221
        e_21.name = 'runner:twolist:ldata['+str(e_2.number)+']:subl1['+str(e_21.number)+']:name'
        e_22.number = 222
        e_22.name = 'runner:twolist:ldata['+str(e_2.number)+']:subl1['+str(e_22.number)+']:name'
        e_2.subl1.append(e_21)
        e_2.subl1.append(e_22)
        r_1.two_list.ldata.append(e_1)
        r_1.two_list.ldata.append(e_2)

        self.crud.create(self.ncc, r_1)

        # Get non-top level node - second level list element
        rf = Runner()
        ef1 = Runner.TwoList.Ldata()
        ef1.number = 21  # 'runner:twolist:ldata['+str(e_1.number)+']:name'
        ef11 = Runner.TwoList.Ldata.Subl1()
        ef11.number = 211  # 'runner:twolist:ldata['+str(e_1.number)+']:subl1['+str(e_11.number)+']:name'
        ef1.subl1.append(ef11)
        rf.two_list.ldata.append(ef1)

        ef11_read = self.crud.read(self.ncc, ef11)
        self.assertIsNotNone(ef11_read)
        self.assertEqual(ef11_read.name, 'runner:twolist:ldata['+str(e_1.number)+']:subl1['+str(e_11.number)+']:name')

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)

    def test_inbtw_list_node(self):
        # CREATE
        r_1 = Runner()
        e_1 = Runner.InbtwList.Ldata()
        e_2 = Runner.InbtwList.Ldata()
        e_1.number = 11
        e_1.name = 'runner:inbtwlist:['+str(e_1.number)+']:name'
        e_1.subc.number = 111
        e_1.subc.name = 'runner:inbtwlist:['+str(e_1.number)+']:subc:name'
        e_2.number = 12
        e_2.name = 'runner:inbtwlist:['+str(e_2.number)+']:name'
        e_2.subc.number = 121
        e_2.subc.name = 'runner:inbtwlist:['+str(e_2.number)+']:name'
        e_11 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_11.number = 111
        e_11.name = 'runner:inbtwlist:['+str(e_1.number)+']:subc:subcsubl1['+str(e_11.number)+']:name'
        e_12 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_12.number = 112
        e_12.name = 'runner:inbtwlist:['+str(e_1.number)+']:subc:subcsubl1['+str(e_12.number)+']:name'
        e_1.subc.subc_subl1.extend([e_11, e_12])
        e_21 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_21.number = 121
        e_21.name = 'runner:inbtwlist:['+str(e_2.number)+']:subc:subcsubl1['+str(e_21.number)+']:name'
        e_22 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_22.number = 122
        e_22.name = 'runner:inbtwlist:['+str(e_2.number)+']:subc:subcsubl1['+str(e_22.number)+']:name'
        e_2.subc.subc_subl1.extend([e_21, e_22])
        r_1.inbtw_list.ldata.extend([e_1, e_2])
        self.crud.create(self.ncc, r_1)

        # READ second level list element
        rf = Runner()
        ef2 = Runner.InbtwList.Ldata()
        ef2.number = 12
        ef22 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        ef22.number = 122
        ef2.subc.subc_subl1.append(ef22)
        rf.inbtw_list.ldata.append(ef2)

        ef22_read = self.crud.read(self.ncc, ef22)
        self.assertIsNotNone(ef22_read)
        self.assertEqual(ef22_read.name,
                         'runner:inbtwlist:['+str(e_2.number)+']:subc:subcsubl1['+str(e_22.number)+']:name')

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(SanityTest)
    for name in testnames:
        suite.addTest(SanityTest(name))
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
