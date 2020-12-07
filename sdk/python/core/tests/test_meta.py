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

"""test_meta.py
Tests how metadata is generated,
getting Enum and Union info
"""
from __future__ import absolute_import

import unittest

try:
    from ydk.models.ydktest.ydktest_sanity import Runner
    from ydk.models.ydktest import openconfig_bgp
    from ydk.models.ydktest import openconfig_bgp_types
except ImportError:
    from ydk.models.ydktest.ydktest_sanity.runner.runner import Runner
    from ydk.models.ydktest.openconfig_bgp.bgp.bgp import Bgp

from ydk._core._dm_meta_info import _MetaInfoEnum, REFERENCE_UNION
from ydk._core._dm_meta_info import module_meta, module_enums


class MetaSanityTest(unittest.TestCase):

    def test_runner(self):
        runner = Runner()
        runner_meta = runner._meta_info()
        self.assertEqual(runner_meta.module_name, "ydktest-sanity")
        self.assertEqual(runner_meta.name, "Runner")
        self.assertEqual(runner_meta.yang_name, "runner")
        print(runner_meta.name, runner_meta.doc)
        for member_meta in runner_meta.meta_info_class_members:
            print("{}  --  {}".format(member_meta.name, member_meta._doc.strip()))

        one_list_meta = runner_meta.member('one-list')
        self.assertIsNotNone(one_list_meta)
        self.assertEqual(one_list_meta.name, 'one-list')

        built_in_t_meta = runner.ytypes.built_in_t._meta_info()
        embeded_enum_meta = built_in_t_meta.member('embeded-enum')
        self.assertIsNotNone(embeded_enum_meta)
        embeded_enum_map = embeded_enum_meta.enum_dict()
        print("\nEnum dictionary:")
        for name in embeded_enum_map:
            print("%12s: %s" % (name, embeded_enum_map[name]))
        self.assertTrue(len(embeded_enum_map) > 0)
        self.assertEqual(embeded_enum_map['seven'].value, 7)

        test_enum_union_meta()
        test_module_meta()

    def test_mandatory_leaf(self):
        mand_list = Runner.MandList()
        mand_meta = mand_list._meta_info()
        self.assertFalse(mand_meta.has_must)
        self.assertFalse(mand_meta.has_when)

        num_meta = mand_meta.member('num')
        self.assertIsNotNone(num_meta)
        self.assertTrue(num_meta.is_mandatory)
        self.assertTrue(num_meta.is_config)

    def test_must_when(self):
        from ydk.models.ydktest import ydktest_sanity
        ifc = ydktest_sanity.ConditionalInterface()
        ifc_meta = ifc._meta_info()
        self.assertTrue(ifc_meta.has_must)
        self.assertFalse(ifc_meta.has_when)
        self.assertTrue(ifc_meta.is_config)
        self.assertFalse(ifc_meta.is_mandatory)
        self.assertFalse(ifc_meta.is_presence)


def test_enum_union_meta():
    nbr_ipv6 = openconfig_bgp.Bgp.Neighbors.Neighbor()
    nbr_ipv6.neighbor_address = '2001:db8:fff1::1'
    nbr_ipv6.config.neighbor_address = '2001:db8:fff1::1'
    nbr_ipv6.config.peer_as = 65002
    nbr_ipv6.config.peer_type = openconfig_bgp_types.PeerType.INTERNAL

    # Print neighbor address Union
    config_meta = nbr_ipv6.config._meta_info()
    print("{}  --  {}".format(config_meta.name, config_meta.doc))
    for member in config_meta.meta_info_class_members:
        if member.mtype == REFERENCE_UNION:
            print("\nUnion list of tuples:")
            for item in member.union_list():
                print("    {}".format(item))

    # Print PeerType enum
    peer_type_meta = openconfig_bgp_types.PeerType._meta_info()
    if isinstance(peer_type_meta, _MetaInfoEnum):
        peer_type_enum_dict = peer_type_meta.enum_dict()
        print("\nEnum dictionary:")
        for name in peer_type_enum_dict:
            print("%12s: %s" % (name, peer_type_enum_dict[name]))


def test_module_meta():
    bgp_name = Runner.__module__
    meta = module_meta(bgp_name)
    print("\nModule meta dictionary:")
    for name in sorted(meta):
        print("%40s: %s" % (name, meta[name]))
    meta = module_enums(bgp_name)
    print("\nModule enum meta dictionary:")
    for name in sorted(meta):
        print("%40s: %s" % (name, meta[name]))
    print('')


if __name__ == '__main__':
    import sys
    suite = unittest.TestLoader().loadTestsFromTestCase(MetaSanityTest)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
