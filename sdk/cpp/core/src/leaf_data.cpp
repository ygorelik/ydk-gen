/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2016-2019 Cisco Systems. All rights reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -------------------------------------------------------------------
 This file has been modified by Yan Gorelik, YDK Solutions.
 All modifications in original under CiscoDevNet domain
 introduced since October 2019 are copyrighted.
 All rights reserved under Apache License, Version 2.0.
 ------------------------------------------------------------------*/

#include <iostream>
#include "types.hpp"

using namespace std;

namespace ydk
{
LeafData::LeafData(const string & value, YType type, YFilter yfilter, bool is_set,
		const string & name_space, const string & name_space_prefix)
    : value(value), type(type), name_space(name_space),
	  name_space_prefix(name_space_prefix), yfilter(yfilter), is_set(is_set)
{
}

LeafData::~LeafData()
{
}

bool LeafData::operator == (LeafData & other) const
{
    return value == other.value && yfilter == other.yfilter && is_set == other.is_set;
}

bool LeafData::operator == (const LeafData & other) const
{
    return value == other.value && yfilter == other.yfilter && is_set == other.is_set;
}

std::ostream& operator<< (std::ostream& stream, const LeafData& value)
{
    stream<<value.value;
    return stream;
}


}
