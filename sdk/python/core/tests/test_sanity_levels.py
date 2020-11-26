#  ----------------------------------------------------------------
# Copyright 2016 Cisco Systems
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

"""test_sanity_levels.py
sanity test for ydktest-sanity.yang
"""
from __future__ import absolute_import

import sys
import unittest

from ydk.types import Empty
try:
    from ydk.models.ydktest.ydktest_sanity import Runner, ChildIdentity
    from ydk.models.ydktest.oc_pattern import OcA
except ImportError:
    from ydk.models.ydktest.ydktest_sanity.runner.runner import Runner
    from ydk.models.ydktest.ydktest_sanity.ydktest_sanity import ChildIdentity
    from ydk.models.ydktest.oc_pattern.oc_a.oc_a import OcA

from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService

from test_utils import assert_with_error
from test_utils import ParametrizedTestCase
from test_utils import get_device_info


class SanityYang(unittest.TestCase):

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

    def setUp(self):
        runner = Runner()
        self.crud.delete(self.ncc, runner)

    def tearDown(self):
        runner = Runner()
        self.crud.delete(self.ncc, runner)

    def _create_runner(self):
        runner = Runner()
        runner.ytypes = runner.Ytypes()
        runner.ytypes.built_in_t = runner.ytypes.BuiltInT()
        return runner

    def test_one_level_pos(self):
        # READ
        r_1, r_2 = Runner(), Runner()
        r_1.one.number, r_1.one.name = 1, 'runner:one:name'
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        r_1.one.number, r_1.one.name = 10, 'runner/one/name'
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_one_aug_level_pos(self):
        # READ
        r_1 = Runner()
        r_1.ydktest_sanity_augm_one.twin_number = 1
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, Runner())

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1= Runner()
        r_1.ydktest_sanity_augm_one.twin_number = 10
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, Runner())

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, Runner())

        self.assertEqual(r_2, None)

    def test_two_level_pos(self):
        # READ
        r_1 = Runner()
        r_1.two.number, r_1.two.name, r_1.two.sub1.number = 2, 'runner:two:name', 21
        self.crud.create(self.ncc, r_1)
        r_2 = Runner()
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        r_1.two.number, r_1.two.name, r_1.two.sub1.number = 20, 'runner/two/name', 210
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_three_level_pos(self):
        # READ
        r_1 = self._create_runner()
        r_1.three.number, r_1.three.name, \
            r_1.three.sub1.number, r_1.three.sub1.sub2.number = 3, 'runner:three:name', 31, 311
        self.crud.create(self.ncc, r_1)
        r_2 = Runner()
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        r_1.three.number, r_1.three.name, \
            r_1.three.sub1.number, r_1.three.sub1.sub2.number = 30, 'runner/three/name', 310, 3110
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_onelist_neg_dupkey(self):
        # netsim/enxr not complaining
        r_1, r_2 = Runner(), Runner()
        e_1, e_2 = Runner.OneList.Ldata(), Runner.OneList.Ldata()
        e_1.number = 1
        e_2.name = 'foo'
        e_2.number = 1
        e_2.name = 'bar'
        r_1.one_list.ldata.extend([e_1, e_2])
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

    def test_onelist_pos(self):
        # READ
        r_1, r_2 = Runner(), Runner()
        e_1, e_2 = Runner.OneList.Ldata(), Runner.OneList.Ldata()
        e_1.number = 1
        e_1.name = 'runner:onelist:ldata['+str(e_1.number)+']:name'
        e_2.number = 2
        e_2.name = 'runner:onelist:ldata['+str(e_2.number)+']:name'

        r_1.one_list.ldata.append(e_1)
        r_1.one_list.ldata.append(e_2)

        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        e_1, e_2 = Runner.OneList.Ldata(), Runner.OneList.Ldata()
        e_1.number = 1
        e_1.name = 'runner:onelist:ldata['+str(e_1.number)+']:name'
        e_2.number = 2
        e_2.name = 'runner:onelist:ldata['+str(e_2.number)+']:name'
        r_1.one_list.ldata.extend([e_1, e_2])
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_twolist_pos(self):
        # READ
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

        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        e_1, e_2 = Runner.TwoList.Ldata(), Runner.TwoList.Ldata()
        e_11, e_12 = Runner.TwoList.Ldata.Subl1(), Runner.TwoList.Ldata.Subl1()
        e_1.number = 21
        e_1.name = 'runner/twolist/ldata['+str(e_1.number)+']/name'
        e_11.number = 211
        e_11.name = 'runner/twolist/ldata['+str(e_1.number)+']/subl1['+str(e_11.number)+']/name'
        e_12.number = 212
        e_12.name = 'runner/twolist/ldata['+str(e_1.number)+']/subl1['+str(e_12.number)+']/name'
        e_1.subl1.extend([e_11, e_12])
        e_21, e_22 = Runner.TwoList.Ldata.Subl1(), Runner.TwoList.Ldata.Subl1()
        e_2.number = 22
        e_2.name = 'runner/twolist/ldata['+str(e_2.number)+']/name'
        e_21.number = 221
        e_21.name = 'runner/twolist/ldata['+str(e_2.number)+']/subl1['+str(e_21.number)+']/name'
        e_22.number = 222
        e_22.name = 'runner/twolist/ldata['+str(e_2.number)+']/subl1['+str(e_22.number)+']/name'
        e_2.subl1.extend([e_21, e_22])
        r_1.two_list.ldata.extend([e_1, e_2])
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_threelist_pos(self):
        # READ
        r_1, r_2 = Runner(), Runner()
        e_1 = Runner.ThreeList.Ldata()
        e_1.number = 31
        e_1.name = 'runner:threelist:ldata['+str(e_1.number)+']:name'
        e_2 = Runner.ThreeList.Ldata()
        e_2.number = 32
        e_2.name = 'runner:threelist:ldata['+str(e_2.number)+']:name'
        e_11 = Runner.ThreeList.Ldata.Subl1()
        e_12 = Runner.ThreeList.Ldata.Subl1()
        e_11.number = 311
        e_11.name = 'runner:threelist:ldata['+str(e_1.number)+']:subl1['+str(e_11.number)+']:name'
        e_12.number = 312
        e_12.name = 'runner:threelist:ldata['+str(e_1.number)+']:subl1['+str(e_12.number)+']:name'
        e_111 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_112 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_111.number = 3111
        e_111.name = 'runner:threelist:ldata['+str(e_1.number)+']:subl1['+str(e_11.number)+']:subsubl1['+str(e_111.number)+']:name'
        e_112.number = 3112
        e_112.name = 'runner:threelist:ldata['+str(e_1.number)+']:subl1['+str(e_11.number)+']:subsubl1['+str(e_112.number)+']:name'
        e_11.sub_subl1.extend([e_111, e_112])
        e_121 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_122 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_121.number = 3121
        e_121.name = 'runner:threelist:ldata['+str(e_1.number)+']:subl1['+str(e_12.number)+']:subsubl1['+str(e_121.number)+']:name'
        e_122.number = 3122
        e_121.name = 'runner:threelist:ldata['+str(e_1.number)+']:subl1['+str(e_12.number)+']:subsubl1['+str(e_122.number)+']:name'
        e_12.sub_subl1.extend([e_121, e_122])
        e_1.subl1.extend([e_11, e_12])
        e_21 = Runner.ThreeList.Ldata.Subl1()
        e_22 = Runner.ThreeList.Ldata.Subl1()
        e_21.number = 321
        e_21.name = 'runner:threelist:ldata['+str(e_2.number)+']:subl1['+str(e_21.number)+']:name'
        e_22.number = 322
        e_22.name = 'runner:threelist:ldata['+str(e_2.number)+']:subl1['+str(e_22.number)+']:name'
        e_211 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_212 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_211.number = 3211
        e_211.name = 'runner:threelist:ldata['+str(e_2.number)+']:subl1['+str(e_21.number)+']:subsubl1['+str(e_211.number)+']:name'
        e_212.number = 3212
        e_212.name = 'runner:threelist:ldata['+str(e_2.number)+']:subl1['+str(e_21.number)+']:subsubl1['+str(e_212.number)+']:name'
        e_21.sub_subl1.extend([e_211, e_212])
        e_221 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_222 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_221.number = 3221
        e_221.name = 'runner:threelist:ldata['+str(e_2.number)+']:subl1['+str(e_22.number)+']:subsubl1['+str(e_221.number)+']:name'
        e_222.number = 3222
        e_222.name = 'runner:threelist:ldata['+str(e_2.number)+']:subl1['+str(e_22.number)+']:subsubl1['+str(e_222.number)+']:name'
        e_22.sub_subl1.extend([e_221, e_222])
        e_2.subl1.extend([e_21, e_22])
        r_1.three_list.ldata.extend([e_1, e_2])
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        e_1 = Runner.ThreeList.Ldata()
        e_1.number = 31
        e_1.name = 'runner/threelist/ldata['+str(e_1.number)+']/name'
        e_2 = Runner.ThreeList.Ldata()
        e_2.number = 32
        e_2.name = 'runner/threelist/ldata['+str(e_2.number)+']/name'
        e_11 = Runner.ThreeList.Ldata.Subl1()
        e_12 = Runner.ThreeList.Ldata.Subl1()
        e_11.number = 311
        e_11.name = 'runner/threelistldata['+str(e_1.number)+']/subl1['+str(e_11.number)+']/name'
        e_12.number = 312
        e_12.name = 'runner/threelist/ldata['+str(e_1.number)+']/subl1['+str(e_12.number)+']/name'
        e_111 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_112 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_111.number = 3111
        e_111.name = 'runner/threelist/ldata['+str(e_1.number)+']/subl1['+str(e_11.number)+']/subsubl1['+str(e_111.number)+']/name'
        e_112.number = 3112
        e_112.name = 'runner/threelist/ldata['+str(e_1.number)+']/subl1['+str(e_11.number)+']/subsubl1['+str(e_112.number)+']/name'
        e_11.sub_subl1.extend([e_111, e_112])
        e_121 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_122 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_121.number = 3121
        e_121.name = 'runner/threelist/ldata['+str(e_1.number)+']/subl1['+str(e_12.number)+']/subsubl1['+str(e_121.number)+']/name'
        e_122.number = 3122
        e_121.name = 'runner/threelist/ldata['+str(e_1.number)+']/subl1['+str(e_12.number)+']/subsubl1['+str(e_122.number)+']/name'
        e_12.sub_subl1.extend([e_121, e_122])
        e_1.subl1.extend([e_11, e_12])
        e_21 = Runner.ThreeList.Ldata.Subl1()
        e_22 = Runner.ThreeList.Ldata.Subl1()
        e_21.number = 321
        e_21.name = 'runner/threelist/ldata['+str(e_2.number)+']/subl1['+str(e_21.number)+']/name'
        e_22.number = 322
        e_22.name = 'runner/threelist/ldata['+str(e_2.number)+']/subl1['+str(e_22.number)+']/name'
        e_211 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_212 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_211.number = 3211
        e_211.name = 'runner/threelist/ldata['+str(e_2.number)+']/subl1['+str(e_21.number)+']/subsubl1['+str(e_211.number)+']/name'
        e_212.number = 3212
        e_212.name = 'runner/threelist/ldata['+str(e_2.number)+']/subl1['+str(e_21.number)+']/subsubl1['+str(e_212.number)+']/name'
        e_21.sub_subl1.extend([e_211, e_212])
        e_221 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_222 = Runner.ThreeList.Ldata.Subl1.SubSubl1()
        e_221.number = 3221
        e_221.name = 'runner/threelist/ldata['+str(e_2.number)+']/subl1['+str(e_22.number)+']/subsubl1['+str(e_221.number)+']/name'
        e_222.number = 3222
        e_222.name = 'runner/threelist/ldata['+str(e_2.number)+']/subl1['+str(e_22.number)+']/subsubl1['+str(e_222.number)+']/name'
        e_22.sub_subl1.extend([e_221, e_222])
        e_2.subl1.extend([e_21, e_22])
        r_1.three_list.ldata.extend([e_1, e_2])
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    @unittest.skip('Skip due to issue with one class per module option')
    def test_nested_naming(self):
        n_1 = Runner.NestedNaming.NestedNaming()
        n_2 = Runner.NestedNaming()

        n_1.nested_naming = 1
        n_2.NestedNaming.nested_naming = 1

        self.assertEqual(n_1.nested_naming, n_2.NestedNaming.nested_naming)
        self.assertEqual(n_1.yang_name, n_2.yang_name)

    def test_inbtw_list_pos(self):
        # READ
        r_1, r_2 = Runner(), Runner()
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
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        e_1 = Runner.InbtwList.Ldata()
        e_2 = Runner.InbtwList.Ldata()
        e_1.number = 11
        e_1.name = 'runner/inbtwlist/['+str(e_1.number)+']/name'
        e_1.subc.number = 111
        e_1.subc.name = 'runnerinbtwlist/['+str(e_1.number)+']/subc/name'
        e_2.number = 12
        e_2.name = 'runner/inbtwlist/['+str(e_2.number)+']/name'
        e_2.subc.number = 121
        e_2.subc.name = 'runner/inbtwlist/['+str(e_2.number)+']/name'
        e_11 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_11.number = 111
        e_11.name = 'runner/inbtwlist/['+str(e_1.number)+']/subc/subcsubl1['+str(e_11.number)+']/name'
        e_12 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_12.number = 112
        e_12.name = 'runner/inbtwlist/['+str(e_1.number)+']/subc/subcsubl1['+str(e_12.number)+']/name'
        e_1.subc.subc_subl1.extend([e_11, e_12])
        e_21 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_21.number = 121
        e_21.name = 'runner/inbtwlist/['+str(e_2.number)+']/subc/subcsubl1['+str(e_21.number)+']/name'
        e_22 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_22.number = 122
        e_22.name = 'runner/inbtwlist/['+str(e_2.number)+']/subc/subcsubl1['+str(e_22.number)+']/name'
        e_2.subc.subc_subl1.extend([e_21, e_22])
        r_1.inbtw_list.ldata.extend([e_1, e_2])
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_leafref_simple_pos(self):
        # change ref and original data together
        # READ
        r_1, r_2 = Runner(), Runner()
        r_1.ytypes.built_in_t.number8 = 100
        r_1.ytypes.built_in_t.leaf_ref = r_1.ytypes.built_in_t.number8
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        r_1.ytypes.built_in_t.number8 = 110
        r_1.ytypes.built_in_t.leaf_ref = r_1.ytypes.built_in_t.number8
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_leafref_pos(self):
        # CREATE
        r_1, r_2 = Runner(), Runner()
        r_1.one.name = 'runner:one:name'
        r_1.two.sub1.number = 21
        r_1.three.sub1.sub2.number = 311
        e_1 = Runner.InbtwList.Ldata()
        e_2 = Runner.InbtwList.Ldata()
        e_1.number = 11
        e_2.number = 21
        e_1.name = 'runner:inbtwlist['+str(e_1.number)+']:name'
        e_2.name = 'runner:inbtwlist['+str(e_2.number)+']:name'
        e_1.subc.number = 111
        e_2.subc.number = 121
        e_1.subc.name = 'runner:inbtwlist['+str(e_1.number)+']:subc:name'
        e_2.subc.name = 'runner:inbtwlist['+str(e_2.number)+']:subc:name'
        e_11 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_12 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_11.number = 111
        e_12.number = 112
        e_11.name = 'runner:inbtwlist['+str(e_1.number)+']:subc:subcsubl1['+str(e_11.number)+']:name'
        e_12.name = 'runner:inbtwlist['+str(e_1.number)+']:subc:subcsubl1['+str(e_12.number)+']:name'
        e_1.subc.subc_subl1.extend([e_11, e_12])
        e_21 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_22 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_21.number = 311
        e_22.number = 122
        e_21.name = 'runner:inbtwlist['+str(e_2.number)+']:subc:subcsubl1['+str(e_21.number)+']:name'
        e_22.name = 'runner:inbtwlist['+str(e_2.number)+']:subc:subcsubl1['+str(e_22.number)+']:name'
        e_2.subc.subc_subl1.extend([e_21, e_22])
        r_1.inbtw_list.ldata.extend([e_1, e_2])

        r_1.leaf_ref.ref_one_name = r_1.one.name
        r_1.leaf_ref.ref_two_sub1_number = r_1.two.sub1.number
        r_1.leaf_ref.ref_three_sub1_sub2_number = r_1.three.sub1.sub2.number
        r_1.leaf_ref.ref_inbtw = e_21.name
        r_1.leaf_ref.one.two.self_ref_one_name = r_1.leaf_ref.ref_one_name
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        r_1.one.name = 'runner/one/name'
        r_1.two.sub1.number = 21
        r_1.three.sub1.sub2.number = 311
        e_1 = Runner.InbtwList.Ldata()
        e_2 = Runner.InbtwList.Ldata()
        e_1.number = 11
        e_2.number = 21
        e_1.name = 'runner/inbtwlist['+str(e_1.number)+']/name'
        e_2.name = 'runner/inbtwlist['+str(e_2.number)+']/name'
        e_1.subc.number = 111
        e_2.subc.number = 121
        e_1.subc.name = 'runner/inbtwlist['+str(e_1.number)+']/subc/name'
        e_2.subc.name = 'runner/inbtwlist['+str(e_2.number)+']/subc/name'
        e_11 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_12 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_11.number = 111
        e_12.number = 112
        e_11.name = 'runner/inbtwlist['+str(e_1.number)+']/subc/subcsubl1['+str(e_11.number)+']/name'
        e_12.name = 'runner/inbtwlist['+str(e_1.number)+']/subc/subcsubl1['+str(e_12.number)+']/name'
        e_1.subc.subc_subl1.extend([e_11, e_12])
        e_21 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_22 = Runner.InbtwList.Ldata.Subc.SubcSubl1()
        e_21.number = 311
        e_22.number = 122
        e_21.name = 'runner/inbtwlist['+str(e_2.number)+']/subc/subcsubl1['+str(e_21.number)+']/name'
        e_22.name = 'runner/inbtwlist['+str(e_2.number)+']/subc/subcsubl1['+str(e_22.number)+']/name'
        e_2.subc.subc_subl1.extend([e_21, e_22])
        r_1.inbtw_list.ldata.extend([e_1, e_2])

        r_1.leaf_ref.ref_one_name = r_1.one.name
        r_1.leaf_ref.ref_two_sub1_number = r_1.two.sub1.number
        r_1.leaf_ref.ref_three_sub1_sub2_number = r_1.three.sub1.sub2.number
        r_1.leaf_ref.ref_inbtw = e_21.name
        r_1.leaf_ref.one.two.self_ref_one_name = r_1.leaf_ref.ref_one_name
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_aug_one_pos(self):
        # CREATE
        r_1, r_2 = Runner(), Runner()
        r_1.one.one_aug.number = 1
        r_1.one.one_aug.name = "r_1.one.one_aug.name"
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        r_1.one.one_aug.number = 10
        r_1.one.one_aug.name = "r_1.one.one_aug.name".replace('.', ':')
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_1)

        self.assertEqual(r_2, None)

    def test_aug_onelist_pos(self):
        # CREATE
        r_1, r_2 = Runner(), Runner()
        e_1 = Runner.OneList.OneAugList.Ldata()
        e_2 = Runner.OneList.OneAugList.Ldata()
        e_1.number = 1
        e_1.name = "e_1.name"
        e_2.number = 2
        e_2.name = "e_2.name"
        r_1.one_list.one_aug_list.ldata.extend([e_1, e_2])
        r_1.one_list.one_aug_list.enabled = True
        self.crud.create(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # UPDATE
        r_1, r_2 = Runner(), Runner()
        e_1 = Runner.OneList.OneAugList.Ldata()
        e_2 = Runner.OneList.OneAugList.Ldata()
        e_1.number = 1
        e_1.name = "e_1.name".replace('.', ':')
        e_2.number = 2
        e_2.name = "e_2.name".replace('.', ':')
        r_1.one_list.one_aug_list.ldata.extend([e_1, e_2])
        r_1.one_list.one_aug_list.enabled = True
        self.crud.update(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_1, r_2)

        # DELETE
        r_1 = Runner()
        self.crud.delete(self.ncc, r_1)
        r_2 = self.crud.read(self.ncc, r_2)

        self.assertEqual(r_2, None)

    def test_parent_empty(self):
        runner = Runner()
        runner.ytypes.enabled = Empty()
        runner.ytypes.built_in_t.emptee = Empty()

        self.crud.create(self.ncc, runner)

        runner_read = self.crud.read(self.ncc, Runner())

        self.assertEqual(runner, runner_read)

    @unittest.skip('Fails on travis. Passes locally')
    def test_oc_pattern(self):
        # Create OcA
        oc = OcA()
        oc.a = 'xyz'
        oc.b.b = 'xyz'
        self.crud.create(self.ncc, oc)

        # Read into Runner1
        oc1 = self.crud.read(self.ncc, OcA())

        # Compare runners
        self.assertEqual(oc, oc1)

        # Delete
        oc = OcA()
        oc.a = 'xyz'
        self.crud.delete(self.ncc, oc)

    def test_mtu(self):
        runner = Runner()
        mt = runner.Mtus.Mtu()
        mt.owner = "test"
        mt.mtu = 12
        runner.mtus.mtu.append(mt)

        self.crud.create(self.ncc, runner)

        runner_read = self.crud.read(self.ncc, Runner())

        self.assertEqual(runner, runner_read)

    def test_passive(self):
        runner = Runner()
        p = runner.Passive()
        p.name = "xyz"
        i = runner.Passive.Interfac()
        i.test = "abc"
        p.interfac.append(i)
        p.testc.xyz = runner.Passive.Testc.Xyz()
        p.testc.xyz.xyz = 25
        runner.passive.append(p)

        self.crud.create(self.ncc, runner)

        runner_read = self.crud.read(self.ncc, Runner())
        self.assertEqual(runner, runner_read)

    def test_inner_pres(self):
        runner = Runner()
        runner.outer.inner = runner.Outer.Inner()
        self.crud.create(self.ncc, runner)

        runner_read = self.crud.read(self.ncc, Runner())
        self.assertEqual(runner, runner_read)

    def test_embedded_single_quote_list_key(self):
        r = Runner()
        t = Runner.TwoKeyList()
        t.first = "ab'c"
        t.second = 1233
        r.two_key_list.append(t)
        self.crud.create(self.ncc, r)

        runner_read = self.crud.read(self.ncc, Runner())
        self.assertEqual(r, runner_read)

    def test_embedded_double_quote_list_key(self):
        r = Runner()
        t = Runner.TwoKeyList()
        t.first = 'ab"c'
        t.second = 1233
        r.two_key_list.append(t)
        self.crud.create(self.ncc, r)

        runner_read = self.crud.read(self.ncc, Runner())
        self.assertEqual(r, runner_read)

    def test_embedded_slash_list_key(self):
        r = Runner()
        t = Runner.TwoKeyList()
        t.first = "ab/c"
        t.second = 1233
        r.two_key_list.append(t)
        self.crud.create(self.ncc, r)

        runner_read = self.crud.read(self.ncc, Runner())
        self.assertEqual(r, runner_read)


if __name__ == '__main__':
    device, non_demand, common_cache, timeout = get_device_info()

    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(
        SanityYang,
        device=device,
        non_demand=non_demand,
        common_cache=common_cache,
        timeout=timeout))
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
