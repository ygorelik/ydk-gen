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
# This file has been modified by Yan Gorelik, YDK Solutions.
# All modifications in original under CiscoDevNet domain
# introduced since October 2019 are copyrighted.
# All rights reserved under Apache License, Version 2.0.
# ------------------------------------------------------------------

"""
 module_printer.py

 YANG model driven API, python emitter.

"""
import sys
from ydkgen.api_model import Class, Enum, Package
from ydkgen.common import convert_to_reStructuredText

from .class_printer import ClassPrinter
from .enum_printer import EnumPrinter
from ydkgen.printer.file_printer import FilePrinter


class ModulePrinter(FilePrinter):

    def __init__(self, ctx, extra_args):
        if sys.version_info > (3,):
            super().__init__(ctx)
        else:
            super(ModulePrinter, self).__init__(ctx)
        self.one_class_per_module = extra_args.get('one_class_per_module', False)
        self.identity_subclasses = extra_args.get('identity_subclasses', {})
        self.module_namespace_lookup = extra_args.get('module_namespace_lookup', {})
        self.generate_meta = extra_args.get('generate_meta', False)

    def print_header(self, package):
        self._print_module_description(package)
        self._print_imports(package)

    def print_body(self, package):
        if self.one_class_per_module:
            if isinstance(package, Package):
                self._print_module_enums(package)
                identities = [child for child in package.owned_elements if
                              isinstance(child, Class) and child.is_identity()]
                ClassPrinter(self.ctx, self.module_namespace_lookup, self.one_class_per_module,
                             self.generate_meta,
                             self.identity_subclasses).print_output(identities)
            else:
                self._print_module_classes(package)
        else:
            self._print_module_enums(package)
            self._print_module_classes(package)
        self.ctx.bline()

    def _print_module_description(self, package):
        comment = package.stmt.search_one('description')
        self.ctx.writeln('""" %s ' % package.name)
        self.ctx.bline()

        if comment is not None:
            comment = comment.arg
            for line in comment.split('\n'):
                self.ctx.writeln(convert_to_reStructuredText(line))
        self.ctx.bline()
        self.ctx.writeln('"""')

    def _print_static_imports(self):
        self.ctx.writeln("import sys")
        self.ctx.writeln("from collections import OrderedDict")
        self.ctx.bline()
        self.ctx.writeln("from ydk.types import Entity as _Entity_")
        self.ctx.writeln("from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64")
        self.ctx.writeln("from ydk.filters import YFilter")
        self.ctx.writeln("from ydk.errors import YError, YModelError")
        self.ctx.writeln("from ydk.errors.error_handler import handle_type_error as _handle_type_error")
        self.ctx.bline()

    def _print_imports(self, package):
        self._print_static_imports()
        imports_to_print = set()

        for imported_type in package.imported_types():
            if all((id(imported_type) in self.identity_subclasses,
                    self.is_derived_identity(package, imported_type))):
                if self.one_class_per_module:
                    imported_stmt = 'from %s.%s import %s' % (
                        imported_type.get_py_mod_name(), imported_type.get_py_mod_name().split('.')[-1],
                        imported_type.qn().split('.')[0])
                else:
                    imported_stmt = 'from %s import %s' % (
                        imported_type.get_py_mod_name(), imported_type.qn().split('.')[0])
                imports_to_print.add(imported_stmt)

        for imported_stmt in sorted(imports_to_print):
            self.ctx.writeln(imported_stmt)

        self.ctx.bline()
        # self.ctx.bline()

    def _print_module_enums(self, package):
        enumz = []
        enumz.extend(
            [element for element in package.owned_elements if isinstance(element, Enum)])
        for nested_enumz in sorted(enumz, key=lambda element: element.name):
            self._print_enum(nested_enumz)

    def _print_module_classes(self, package):
        if self.one_class_per_module:
            ClassPrinter(self.ctx, self.module_namespace_lookup, self.one_class_per_module,
                         self.generate_meta,
                         self.identity_subclasses).print_output([package])
        else:
            ClassPrinter(self.ctx, self.module_namespace_lookup, self.one_class_per_module,
                         self.generate_meta,
                         self.identity_subclasses).print_output(
                        [clazz for clazz in package.owned_elements if isinstance(clazz, Class)])

    def _print_enum(self, enum_class):
        EnumPrinter(self.ctx).print_enum(enum_class, self.generate_meta)
