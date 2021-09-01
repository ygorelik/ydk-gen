#  ----------------------------------------------------------------
# Copyright 2017-2019 Cisco Systems
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
restconf_session.py
RestconfSession Python wrapper.
"""

from ydk.types import EncodingFormat as _EncodingFormat
from ydk.path import RestconfSession as _RestconfSession


class RestconfSession(object):
    """
     Python wrapper for RestconfSession.
    """

    def __init__(self, repo, address, username, password,
                 port=80, encoding=_EncodingFormat.JSON,
                 config_url_root="/data", state_url_root="/data"):

        self.rs = _RestconfSession(repo, address, username, password,
                                   port, encoding, config_url_root, state_url_root)

    def get_root_schema(self):
        return self.rs.get_root_schema()

    def invoke(self, rpc):
        return self.rs.invoke(rpc)

    def get_capabilities(self):
        return self.rs.get_capabilities()
