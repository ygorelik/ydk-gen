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
class_docstring_printer.py

 Printer for the docstrings.

"""
from ydkgen.printer.meta_data_util import get_class_docstring


class ClassDocstringPrinter(object):

    def __init__(self, ctx):
        """
            Class doc string printer

            :attribute ctx The printer context
        """
        self.ctx = ctx

    def print_output(self, clazz):
        """
            Prints the doc strings for the clazz

            :param `api_model.Class` clazz :- The Class object.
        """
        self.ctx.lvl_inc()
        self.ctx.writeln('"""')
        self._print_class_docstring_text(clazz)
        self._print_class_docstring_presence(clazz)
        self.ctx.writeln('"""')
        self.ctx.lvl_dec()

    def _print_class_docstring_text(self, clazz):
        class_docstring = get_class_docstring(clazz, 'py')
        if len(class_docstring) > 0:
            prev_line = ''
            for line in class_docstring.split('\n'):
                if line or prev_line:
                    self.ctx.writeln('%s' % line)
                prev_line = line

    def _print_class_docstring_presence(self, clazz):
        if clazz.stmt.search_one('presence') is not None:
            self.ctx.bline()
            line = """This class is a :ref:`presence class<presence-class>`"""
            self.ctx.writeln(line)
