/* ------------------------------------------------------------------
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

#include <ydk/codec_provider.hpp>
#include <ydk/codec_service.hpp>
#include <ydk/xml_subtree_codec.hpp>
#include <ydk/json_subtree_codec.hpp>
#include <ydk/common_utilities.hpp>

#include "ydk_ydktest_yang11/ydktest_sanity_yang11.hpp"

#include "config.hpp"
#include "catch.hpp"

using namespace ydk;
using namespace ydktest_yang11;
using namespace std;

TEST_CASE("test_yang11_container")
{
    CodecServiceProvider codec_provider{EncodingFormat::XML};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::BackwardIncompatible();
    container.test_node = "Testing node";

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<backward-incompatible xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <test-node>Testing node</test-node>
</backward-incompatible>
)";
    CHECK(expected == xml);
}

static string xml_empty_key_expected = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>filter-name</name>
    <enabled/>
    <prop>one</prop>
    <outbound-filter/>
  </filter>
</empty-type>
)";

TEST_CASE("test_type_empty_in_union")
{
    ydk::path::Repository repo{TEST_HOME};
    CodecServiceProvider codec_provider{repo, EncodingFormat::XML};
    CodecService codec_service{};

    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = Empty();
    list_elem->prop = "one";
    list_elem->outbound_filter = Empty();
    auto container = ydktest_sanity_yang11::EmptyType();
    container.filter.append(list_elem);

    string xml = codec_service.encode(codec_provider, container, true);
    CHECK(xml_empty_key_expected == xml);

    auto entity = codec_service.decode(codec_provider, xml, make_shared<ydktest_sanity_yang11::EmptyType>());
    CHECK(container == *entity);
}

TEST_CASE("test_type_empty_key_xml_codec")
{
    XmlSubtreeCodec xml_codec{};
    vector<path::Capability> caps {
        {"ydktest-sanity-yang11", ""}
    };
    ydk::path::Repository repo{TEST_HOME};
    auto root = repo.create_root_schema(caps);

    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = Empty();
    list_elem->prop = "one";
    list_elem->outbound_filter = Empty();
    auto container = ydktest_sanity_yang11::EmptyType();
    container.filter.append(list_elem);

    string payload = xml_codec.encode(container, *root);
    CHECK(trim(xml_empty_key_expected) == payload);

    auto entity = xml_codec.decode(payload, make_shared<ydktest_sanity_yang11::EmptyType>());
    CHECK(container == *entity);
}

TEST_CASE("test_type_empty_key_json_codec")
{
    JsonSubtreeCodec json_codec{};
    vector<path::Capability> caps {
        {"ydktest-sanity-yang11", ""}
    };
    ydk::path::Repository repo{TEST_HOME};
    auto root = repo.create_root_schema(caps);

    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = Empty();
    list_elem->prop = "one";
    list_elem->outbound_filter = Empty();
    auto container = ydktest_sanity_yang11::EmptyType();
    container.filter.append(list_elem);

    string payload = json_codec.encode(container, *root);
    string json_expected = R"({
  "ydktest-sanity-yang11:empty-type": {
    "filter": [
      {
        "enabled": null,
        "name": "filter-name",
        "outbound-filter": null,
        "prop": "one"
      }
    ]
  }
})";

    CHECK(json_expected == payload);

    auto entity = json_codec.decode(payload, make_shared<ydktest_sanity_yang11::EmptyType>());
    CHECK(container == *entity);
}

TEST_CASE("test_type_empty_in_union_json")
{
    CodecServiceProvider codec_provider{EncodingFormat::JSON};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::EmptyType();
    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = Empty();
    list_elem->prop = "one";
    list_elem->outbound_filter = Empty();
    container.filter.append(list_elem);

    string json = codec_service.encode(codec_provider, container, true);
    string json_expected = R"({
  "ydktest-sanity-yang11:empty-type": {
    "filter": [
      {
        "name": "filter-name",
        "enabled": null,
        "prop": "one",
        "outbound-filter": null
      }
    ]
  }
}
)";
    CHECK(json_expected == json);

    auto entity = codec_service.decode(codec_provider, json_expected, make_shared<ydktest_sanity_yang11::EmptyType>());
    CHECK(container == *entity);
}

TEST_CASE("test_type_leafref_in_union")
{
    CodecServiceProvider codec_provider{EncodingFormat::XML};
    CodecService codec_service{};

    auto container = ydktest_sanity_yang11::EmptyType();
    auto list_elem = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    list_elem->name = "filter-name";
    list_elem->enabled = Empty();
    list_elem->prop = "one";
    list_elem->outbound_filter = "filter-name";
    container.filter.append(list_elem);

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>filter-name</name>
    <enabled/>
    <prop>one</prop>
    <outbound-filter>filter-name</outbound-filter>
  </filter>
</empty-type>
)";
    CHECK(expected == xml);

    auto entity = codec_service.decode(codec_provider, xml, make_shared<ydktest_sanity_yang11::EmptyType>());
    CHECK(container == *entity);
}

static string vector_to_string(vector<string> & string_vector)
{
    ostringstream buf;
    for (auto item : string_vector) {
        if (buf.str().length() > 0)
            buf << ", ";
        buf << "\"" << item << "\"";
    }
    return buf.str();
}

TEST_CASE("test_type_empty_key")
{
    ydk::path::Repository repo{TEST_HOME};
    CodecServiceProvider codec_provider{repo, EncodingFormat::XML};
    CodecService codec_service{};

    auto elem1 = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    auto elem2 = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    elem1->name = "abc"; elem2->name = "xyz";
    elem1->enabled = Empty(); elem2->enabled = Empty();
    elem1->prop = "one";  elem2->prop = "two";

    auto container = ydktest_sanity_yang11::EmptyType();
    container.filter.extend({elem1, elem2});

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>abc</name>
    <enabled/>
    <prop>one</prop>
  </filter>
  <filter>
    <name>xyz</name>
    <enabled/>
    <prop>two</prop>
  </filter>
</empty-type>
)";
    CHECK(expected == xml);

    auto entity = codec_service.decode(codec_provider, xml, make_shared<ydktest_sanity_yang11::EmptyType>());
    auto empty_type = dynamic_cast<ydktest_sanity_yang11::EmptyType*>(entity.get());
    CHECK(container == *empty_type);

    auto keys = empty_type->filter.keys();
    CHECK("\"abc\", \"xyz\"" == vector_to_string(keys));
    CHECK(*elem1 == *(empty_type->filter["abc"]));
    CHECK(*elem2 == *(empty_type->filter["xyz"]));
    CHECK(!empty_type->filter.has_key("x"));
}

TEST_CASE("test_type_empty_key2")
{
    ydk::path::Repository repo{TEST_HOME};
    CodecServiceProvider codec_provider{repo, EncodingFormat::XML};
    CodecService codec_service{};

    auto elem1 = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    auto elem2 = make_shared<ydktest_sanity_yang11::EmptyType::Filter>();
    elem1->name = "abc"; elem2->name = "xyz";
    elem1->prop = "one";  elem2->prop = "two";

    auto container = ydktest_sanity_yang11::EmptyType();
    container.filter.extend({elem1, elem2});

    string xml = codec_service.encode(codec_provider, container, true);
    string expected = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>abc</name>
    <enabled/>
    <prop>one</prop>
  </filter>
  <filter>
    <name>xyz</name>
    <enabled/>
    <prop>two</prop>
  </filter>
</empty-type>
)";
    CHECK(expected == xml);

    string xml_minus_enabled = R"(<empty-type xmlns="http://cisco.com/ns/yang/ydktest-yang11">
  <filter>
    <name>abc</name>
    <prop>one</prop>
  </filter>
  <filter>
    <name>xyz</name>
    <prop>two</prop>
  </filter>
</empty-type>
)";
    auto entity = codec_service.decode(codec_provider, xml_minus_enabled, make_shared<ydktest_sanity_yang11::EmptyType>());
    auto empty_type = dynamic_cast<ydktest_sanity_yang11::EmptyType*>(entity.get());
    CHECK(container == *empty_type);

    auto keys = empty_type->filter.keys();
    CHECK("\"abc\", \"xyz\"" == vector_to_string(keys));
}
