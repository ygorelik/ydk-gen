/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2020 Yan Gorelik, YDK Solutions. All rights reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
  ------------------------------------------------------------------*/

//#include <iostream>
//#include <sstream>
//#include <string.h>

#include <ydk/codec_provider.hpp>
#include <ydk/codec_service.hpp>

#include "ydk_ydktest_yang11/ydktest_sanity_yang11.hpp"

#include "config.hpp"
#include "catch.hpp"

using namespace ydk;
using namespace ydktest_yang11;
using namespace std;

TEST_CASE("test_yang11_container")
{
    //ydk::path::Repository repo{TEST_HOME};
    CodecServiceProvider codec_provider{EncodingFormat::XML};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::BackwardIncompatible();
    container.test_node = "Testing node";

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <test-node>Testing node</test-node>
</backward-incompatible>
)";
    REQUIRE(expected == xml);
}

TEST_CASE("test_type_empty_in_union")
{
    ydk::path::Repository repo{TEST_HOME};
    CodecServiceProvider codec_provider{repo, EncodingFormat::XML};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::EmptyType();
    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = true;
    list_elem->prop = "one";
    list_elem->outbound_filter = Empty();
    container.filter.append(list_elem);

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>filter-name</name>
    <enabled>true</enabled>
    <prop>one</prop>
    <outbound-filter/>
  </filter>
</empty-type>
)";
    REQUIRE(expected == xml);

    auto entity = codec_service.decode(codec_provider, xml, make_shared<ydktest_sanity_yang11::EmptyType>());
    CHECK(container == *entity);
}

TEST_CASE("test_type_empty_in_union_json")
{
    CodecServiceProvider codec_provider{EncodingFormat::JSON};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::EmptyType();
    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = true;
    list_elem->prop = "one";
    list_elem->outbound_filter = Empty();
    container.filter.append(list_elem);

    string json = codec_service.encode(codec_provider, container, true);
    string expected = R"({
  "ydktest-sanity-yang11:empty-type": {
    "filter": [
      {
        "name": "filter-name",
        "enabled": true,
        "prop": "one",
        "outbound-filter": ""
      }
    ]
  }
}
)";
    REQUIRE(expected == json);
}

TEST_CASE("test_type_leafref_in_union")
{
    CodecServiceProvider codec_provider{EncodingFormat::XML};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::EmptyType();
    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = true;
    list_elem->prop = "one";
    list_elem->outbound_filter = "filter-name";
    container.filter.append(list_elem);

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>filter-name</name>
    <enabled>true</enabled>
    <prop>one</prop>
    <outbound-filter>filter-name</outbound-filter>
  </filter>
</empty-type>
)";
    REQUIRE(expected == xml);
}
