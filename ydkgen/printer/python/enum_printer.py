#  ----------------------------------------------------------------
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
"""
 enum_printer.py

 YANG model driven API, python emitter.
"""

from ydkgen.api_model import Enum
from ydkgen.common import get_module_name
from ydkgen.printer.meta_data_util import get_enum_class_docstring


class EnumPrinter(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def print_enum(self, enum_class, meta_assign):
        assert isinstance(enum_class, Enum)
        self._print_enum_header(enum_class)
        self._print_enum_body(enum_class, meta_assign)
        self._print_enum_trailer(enum_class)

    def print_enum_meta(self, enum_class):
        self.ctx.writeln("'%s': _MetaInfoEnum(" % enum_class.qn())
        self.ctx.lvl_inc()
        self.ctx.writeln("'%s'," % enum_class.name)
        self.ctx.writeln("'%s', '%s'," % (
                         enum_class.get_py_mod_name(),
                         enum_class.qn()))
        # description = " "
        # for st in enum_class.stmt.parent.substmts:
        #     if st.keyword == 'description':
        #         description = st.arg
        #         break
        self.ctx.writeln('"""%s""",' % enum_class.comment)
        self.ctx.writeln("{")
        self.ctx.lvl_inc()
        for literal in enum_class.literals:
            self.ctx.writeln("'%s': '%s'," % (literal.stmt.arg, literal.name))
        self.ctx.lvl_dec()
        self.ctx.writeln("}, '%s', _yang_ns.NAMESPACE_LOOKUP['%s'])," %
                         (get_module_name(enum_class.stmt), get_module_name(enum_class.stmt)))
        self.ctx.lvl_dec()

    def _print_enum_header(self, enum_class):
        self.ctx.writeln('class %s(Enum):' % enum_class.name)
        self.ctx.lvl_inc()

    def _print_enum_body(self, enum_class, meta_assign):
        self._print_enum_docstring(enum_class)
        self._print_enum_literals(enum_class)
        if meta_assign:
            self._print_enum_meta_assignment(enum_class)

    def _print_enum_docstring(self, enum_class):
        self.ctx.writeln('"""')
        enumz_docstring = get_enum_class_docstring(enum_class, 'py')
        if len(enumz_docstring):
            for line in enumz_docstring.split('\n'):
                if line.strip() != '':
                    self.ctx.writeln(line)
                    self.ctx.bline()
        self.ctx.writeln('"""')
        self.ctx.bline()

    def _print_enum_literals(self, enum_class):
        for enum_literal in enum_class.literals:
            self._print_enum_literal(enum_literal)

    def _print_enum_literal(self, enum_literal):
        name = enum_literal.name
        value = enum_literal.value
        self.ctx.writeln('%s = Enum.YLeaf(%s, "%s")' % (name, value, enum_literal.stmt.arg))
        self.ctx.bline()

    def _print_enum_meta_assignment(self, enum_class):
        self.ctx.bline()
        self.ctx.writeln('@staticmethod')
        self.ctx.writeln('def _meta_info():')
        self.ctx.lvl_inc()

        self.ctx.writeln('from %s import _%s as meta' % (
            enum_class.get_meta_py_mod_name(), enum_class.get_package().name))
        self.ctx.writeln("return meta._meta_table['%s']" % (enum_class.qn()))
        self.ctx.lvl_dec()
        self.ctx.bline()

    def _print_enum_trailer(self, enum_class):
        self.ctx.lvl_dec()
        self.ctx.bline()
