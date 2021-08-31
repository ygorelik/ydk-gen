#  ----------------------------------------------------------------
# YDK - YANG Development Kit
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
  _types_extractor.py

 Extractor for types
"""

from pyang.types import EnumTypeSpec, BitTypeSpec, UnionTypeSpec, PathTypeSpec, IdentityrefTypeSpec


class TypesExtractor(object):
    def __init__(self):
        self.get_enum_type_stmt = lambda stmt: self._get_type_stmt(stmt, EnumTypeSpec)
        self.get_identity_ref_type_stmt = lambda stmt: self._get_type_stmt(
            stmt, IdentityrefTypeSpec)
        self.get_bits_type_stmt = lambda stmt: self._get_type_stmt(stmt, BitTypeSpec)
        self.get_union_type_stmt = lambda stmt: self._get_type_stmt(stmt, UnionTypeSpec)

    def _get_type_stmt(self, stmt, typeSpec):
        if stmt.keyword == 'type':
            type_stmt = stmt
        else:
            type_stmt = stmt.search_one('type')

        if hasattr(type_stmt, 'i_typedef') and type_stmt.i_typedef is not None:
            typedef_stmt = type_stmt.i_typedef
            return self._get_type_stmt(typedef_stmt, typeSpec)
        elif hasattr(type_stmt, 'i_type_spec'):
            type_spec = type_stmt.i_type_spec
            while isinstance(type_spec, PathTypeSpec):
                if not hasattr(type_spec, 'i_target_node'):
                    return None
                type_stmt = type_spec.i_target_node.search_one('type')
                type_spec = type_stmt.i_type_spec
                if hasattr(type_stmt, 'i_typedef') and type_stmt.i_typedef is not None:
                    typedef_stmt = type_stmt.i_typedef
                    return self._get_type_stmt(typedef_stmt, typeSpec)

            if isinstance(type_spec, typeSpec):
                return type_stmt
            else:
                return None
        else:
            return None

    def get_property_type(self, type_stmt):
        enum_type_stmt = self.get_enum_type_stmt(type_stmt)
        bits_type_stmt = self.get_bits_type_stmt(type_stmt)
        union_type_stmt = self.get_union_type_stmt(type_stmt)
        contained_property_type = type_stmt.i_type_spec
        if isinstance(contained_property_type, IdentityrefTypeSpec):
            contained_property_type = contained_property_type.idbases[0].i_identity.i_class
        elif enum_type_stmt is not None:
            # this is an enumeration
            contained_property_type = enum_type_stmt.i_enum
        elif bits_type_stmt is not None:
            # bits
            contained_property_type = bits_type_stmt.i_bits
        elif union_type_stmt is not None:
            contained_property_type = union_type_stmt
        return contained_property_type
