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
#include <sstream>
#include <algorithm>

#include "path_api.hpp"
#include "errors.hpp"
#include "types.hpp"

namespace ydk {

std::string to_str(YType t)
{
#define TOSTRING(t) case YType::t: return #t
    switch(t)
    {
        TOSTRING(uint8);
        TOSTRING(uint16);
        TOSTRING(uint32);
        TOSTRING(uint64);
        TOSTRING(int8);
        TOSTRING(int16);
        TOSTRING(int32);
        TOSTRING(int64);
        TOSTRING(empty);
        TOSTRING(identityref);
        TOSTRING(str);
        TOSTRING(boolean);
        TOSTRING(enumeration);
        TOSTRING(bits);
        TOSTRING(decimal64);
        case YType::anydata: return "anydata";
        case YType::union_: return "union";
    }
    return "";
#undef TOSTRING
}

YLeaf::YLeaf(YType type, std::string name, const std::vector<ydk::YType> & types):
        is_set(false),
        yfilter(YFilter::not_set),
        name(name),
        value(""),
        enum_value(0),
        type(type),
        union_types{types}
{
}

YLeaf::YLeaf(const YLeaf& val):
    is_set{val.is_set},
    yfilter(YFilter::not_set),
    name{val.name},
    value{val.value},
    enum_value{val.enum_value},
    type{val.type},
    bits_value{val.bits_value},
    union_types{val.union_types}
{
}


YLeaf::YLeaf(YLeaf&& val):
    is_set{val.is_set},
    yfilter(YFilter::not_set),
    name{std::move(val.name)},
    value{std::move(val.value)},
    enum_value{std::move(val.enum_value)},
    type{val.type},
    bits_value{val.bits_value},
    union_types{val.union_types}
{
}


YLeaf::~YLeaf()
{
}

const std::string  YLeaf::get() const
{
    if (type == YType::bits ||
        (type == YType::union_ && !bits_value.get_bitmap().empty() &&
         std::find(union_types.begin(), union_types.end(), YType::bits) != union_types.end()))
    {
        return get_bits_string();
    }
    return value;
}

std::pair<std::string, LeafData> YLeaf::get_name_leafdata() const
{
    auto leaf_type = (type == YType::union_) ? value_type : type;
    return {name, { get(), leaf_type, yfilter, is_set, value_namespace, value_namespace_prefix }};
}

void YLeaf::operator = (uint8 val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::uint8 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (uint32 val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::uint32 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (uint64 val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::uint64 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (long val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::int64 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (int8 val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::int8 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (int32 val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::int32 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (Enum::YLeaf val)
{
    std::ostringstream value_buffer;

    value_buffer << val.name;
    store_value(value_buffer.str());
    enum_value = val.value;
    value_type = YType::enumeration;
}

void YLeaf::operator = (Bits val)
{
    std::ostringstream value_buffer;

    bits_value = val;
    value_buffer << get_bits_string();
    store_value(value_buffer.str());
    value_type = YType::bits;
}

void YLeaf::operator = (int64 val)
{
    std::ostringstream value_buffer;

    value_type = (type == YType::union_) ? YType::int64 : type;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (double val)
{
    std::ostringstream value_buffer;

    value_buffer << val;
    store_value(value_buffer.str());
    value_type = YType::decimal64;
}

void YLeaf::operator = (Empty val)
{
    bool purposely_unused_if_condition_to_avoid_compiler_warning = val.set;
    if(purposely_unused_if_condition_to_avoid_compiler_warning){}

    store_value(""); // store empty string
    value_type = YType::empty;
}

void YLeaf::operator = (Identity val)
{
    std::ostringstream value_buffer;

    value_buffer << val.to_string();
    store_value(value_buffer.str());
    value_namespace = val.name_space;
    value_namespace_prefix = val.namespace_prefix;
    value_type = YType::identityref;
}

void YLeaf::operator = (std::string val)
{
    std::ostringstream value_buffer;

    value_type = YType::str;
    value_buffer << val;
    store_value(value_buffer.str());
}

void YLeaf::operator = (Decimal64 val)
{
    std::ostringstream value_buffer;

    value_buffer << val.value;
    store_value(value_buffer.str());
    value_type = YType::decimal64;
}

void YLeaf::set(uint8 val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(uint32 val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(uint64 val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(long val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(int8 val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(int32 val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(Enum::YLeaf val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(Bits val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(int64 val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(double val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(Empty val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(Identity val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(std::string val)
{
    YLeaf::operator=(val);
}

void YLeaf::set(Decimal64 val)
{
    YLeaf::operator=(val);
}

void YLeaf::store_value(std::string && val)
{
    is_set=true;
    if (type == YType::boolean ||
        (type == YType::union_ && std::find(union_types.begin(), union_types.end(), YType::boolean) != union_types.end()))
    {
        value = get_bool_string(val);
        if (value == "true" || value == "false")
        {
            value_type = YType::boolean;
        }
    }
    else
    {
        value = val;
    }
}

YLeaf::operator std::string() const
{
    return get();
}

bool YLeaf::operator == (YLeaf & other) const
{
    return get() == other.get();
}

bool YLeaf::operator == (const YLeaf & other) const
{
    return get() == other.get();
}

bool & YLeaf::operator [] (std::string key)
{
    is_set = true;
    return bits_value[key];
}

std::string YLeaf::get_bits_string() const
{
    std::string value;
    for(auto const & entry : bits_value.get_bitmap())
    {
        if(entry.second)
        {
            value += entry.first + " ";
        }
    }

    value = value.substr(0, value.size()-1);

    return (value);
}

std::ostream& operator<< (std::ostream& stream, const YLeaf& value)
{
    stream << value.get();
    return stream;
}

std::string get_bool_string(const std::string & value)
{
    if(value == "1" || value == "true")
    {
        return "true";
    }
    else if(value == "0" || value == "false")
    {
        return "false";
    }
    else
    {
        return value;
    }
}

}
