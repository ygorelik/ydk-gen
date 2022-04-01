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

#include "../src/types.hpp"
#include "../src/errors.hpp"
#include "catch.hpp"
#include <iostream>

using namespace ydk;

class TestIdentity : public Identity
{
  public:
    TestIdentity() : Identity("http://test.com", "test", "test-identity")
    {
    }
};

class TestEnum : public Enum
{
  public:
    TestEnum() {}
    ~TestEnum(){}

    static const Enum::YLeaf one;
    static const Enum::YLeaf two;
};

const Enum::YLeaf TestEnum::one {1, "one"};
const Enum::YLeaf TestEnum::two {2, "two"};

TEST_CASE("test_value_list_uint8")
{
    YLeafList test_value{YType::uint8, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}

TEST_CASE("test_value_list_uint16")
{
    YLeafList test_value{YType::uint16, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}


TEST_CASE("test_value_list_uint32")
{
    YLeafList test_value{YType::uint32, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}


TEST_CASE("test_value_list_uint64")
{
    YLeafList test_value{YType::uint64, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}


TEST_CASE("test_value_list_int8")
{
    YLeafList test_value{YType::int8, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}


TEST_CASE("test_value_list_int16")
{
    YLeafList test_value{YType::int16, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}


TEST_CASE("test_value_list_int32")
{
    YLeafList test_value{YType::int32, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}


TEST_CASE("test_value_list_int64")
{
    YLeafList test_value{YType::int64, "name"};
    test_value.append(4);
    REQUIRE(test_value[0].get()=="4");
    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="name[.=\"4\"]");
}

TEST_CASE("test_value_list_empty")
{
    YLeafList test_value{YType::empty, "name"};
    test_value.append(Empty());
    REQUIRE(test_value[0].get()=="");
}

TEST_CASE("test_value_list_identity")
{
    YLeafList test_value{YType::identityref, "name"};
    TestIdentity id{};
    test_value.append(id);
    REQUIRE(test_value[0].get()=="test-identity");
//    REQUIRE(test_value[0].value_namespace=="http://test.com"); //TODO
//    REQUIRE(test_value[0].value_namespace_prefix=="test");
}

TEST_CASE("test_value_list_enum_")
{
    YLeafList test_value{YType::enumeration, "enumval"};
    test_value.append(TestEnum::one);
    test_value.append(TestEnum::two);

    auto & leaf = test_value[0];
    REQUIRE(leaf.get()=="one");
    REQUIRE(leaf.enum_value==1);

    REQUIRE(test_value[1].get()=="two");
    REQUIRE(test_value[1].enum_value==2);

    auto nv = test_value.get_name_leafdata();
    REQUIRE(nv[0].first=="enumval[.=\"one\"]");
    REQUIRE(nv[1].first=="enumval[.=\"two\"]");
}

TEST_CASE("test_value_list_str")
{
    YLeafList test_value{YType::str, "name"};
    test_value.append("hello");
    REQUIRE(test_value[0].get()=="hello");
}

TEST_CASE("test_value_list_bool")
{
    YLeafList test_value{YType::boolean, "name"};
    test_value.append(true);
    REQUIRE(test_value[0].get()=="true");

    test_value.append(false);
    REQUIRE(test_value[1].get()=="false");
}

TEST_CASE("test_value_list_bits")
{
    YLeafList test_value{YType::bits, "bits-list"};
    Bits test;
    test["bit1"] = true;
    test["bit2"] = true;
    test["bit3"] = true;
    test["bit4"] = true;
    test_value.append(test);
    REQUIRE(test_value[0].get()=="bit1 bit2 bit3 bit4");

    test["bit3"] = false;
    test_value.append(test);
    REQUIRE(test_value[1].get()=="bit1 bit2 bit4");
}

TEST_CASE("test_value_list_deci64")
{
    YLeafList test_value{YType::decimal64, "value"};
    test_value.append("3.2");
    REQUIRE(test_value[0].get()=="3.2");

    test_value.append("1.2");
    REQUIRE(test_value[1].get()=="1.2");
}

TEST_CASE("test_value_list_duplicate")
{
    YLeafList test_value{YType::str, "value"};
    test_value.append("abc");
    test_value.append("abc");
    test_value.append("abc");
    auto leafs = test_value.getYLeafs();
    CHECK(leafs.size() == 3);
    CHECK(test_value[0].get() == test_value[2].get());
}

TEST_CASE("test_value_list_boolean")
{
    YLeafList test_value{YType::boolean, "value"};
    test_value.append(true);
    test_value.append(false);
    auto leafs = test_value.getYLeafs();
    CHECK(leafs.size() == 2);
    CHECK(test_value[0].get() == "true");
    CHECK(test_value[1].get() == "false");

    auto leaf_data = test_value.get_name_leafdata();
    CHECK(leaf_data[0].first == "value[.=\"true\"]");
    CHECK(leaf_data[1].first == "value[.=\"false\"]");
}
