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

"""
 module_printer.py

 YANG model driven API, python emitter.
"""

from ydkgen.api_model import Class, Enum

from .class_meta_printer import ClassMetaPrinter
from .enum_printer import EnumPrinter
from ydkgen.printer.file_printer import FilePrinter


class ModuleMetaPrinter(FilePrinter):

    def __init__(self, ctx, one_class_per_module, identity_subclasses):
        super(ModuleMetaPrinter, self).__init__(ctx)
        self.one_class_per_module = one_class_per_module
        self.identity_subclasses = identity_subclasses

    def print_header(self, packages):
        self.ctx.str('''
"""
This is auto-generated file,
which includes metadata for module %s
"""

from ydk._core._dm_meta_info import _MetaInfoClassMember, _MetaInfoClass, _MetaInfoEnum
from ydk._core._dm_meta_info import ATTRIBUTE, REFERENCE_LIST, REFERENCE_LEAFLIST, REFERENCE_BITS, REFERENCE_UNION
from ydk._core._dm_meta_info import REFERENCE_CLASS, REFERENCE_IDENTITY_CLASS, REFERENCE_ENUM_CLASS, ANYXML_CLASS
from ydk._core._importer import _yang_ns

''' % packages.name)

    def print_body(self, packages):
        self.ctx.writeln('_meta_table = {')
        self.ctx.lvl_inc()
        for nested_enumz in [e for e in packages.owned_elements if isinstance(e, Enum)]:
            self.print_enum_meta(nested_enumz)
        self.print_classes_meta([c for c in packages.owned_elements if isinstance(c, Class)])
        self.ctx.lvl_dec()
        self.ctx.writeln('}')
        self.print_classes_meta_parents(
            [c for c in packages.owned_elements if isinstance(c, Class)])

    def print_classes_meta(self, unsorted_classes):
        ClassMetaPrinter(self.ctx, self.one_class_per_module, self.identity_subclasses).print_output(
            unsorted_classes)

    def print_enum_meta(self, enum_class):
        EnumPrinter(self.ctx).print_enum_meta(enum_class)

    def print_classes_meta_parents(self, unsorted_classes):
        ClassMetaPrinter(self.ctx, self.one_class_per_module, self.identity_subclasses).print_parents(
            unsorted_classes)
