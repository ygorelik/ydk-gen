/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2017-2019 Cisco Systems. All rights reserved.

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

#include <string.h>
#include <iostream>

#include "config.hpp"
#include "catch.hpp"

#include <ydk/path_api.hpp>
#include <ydk/restconf_provider.hpp>
#include <ydk/errors.hpp>

using namespace ydk;
using namespace std;


TEST_CASE("restconf_provider_crud")
{
    ydk::path::Repository repo{TEST_HOME};
    ydk::RestconfServiceProvider provider{repo, "localhost", "admin", "admin", 12306, EncodingFormat::JSON};

    ydk::path::RootSchemaNode& schema = provider.get_session().get_root_schema();

    ydk::path::Codec s{};

    auto & runner = schema.create_datanode("ydktest-sanity:runner", "");

    //first delete
    std::shared_ptr<ydk::path::Rpc> delete_rpc { schema.create_rpc("ydk:delete") };
    auto json = s.encode(runner, EncodingFormat::JSON, false);
    delete_rpc->get_input_node().create_datanode("entity", json);
    //call delete
    (*delete_rpc)(provider.get_session());

    auto & number8 = runner.create_datanode("ytypes/built-in-t/number8", "3");

    json = s.encode(runner, EncodingFormat::JSON, false);
    CHECK( !json.empty());
    //call create
    std::shared_ptr<ydk::path::Rpc> create_rpc { schema.create_rpc("ydk:create") };
    create_rpc->get_input_node().create_datanode("entity", json);
    (*create_rpc)(provider.get_session());

    //read
    std::shared_ptr<ydk::path::Rpc> read_rpc { schema.create_rpc("ydk:read") };
    auto & runner_read = schema.create_datanode("ydktest-sanity:runner", "");

    json = s.encode(runner_read, EncodingFormat::JSON, false);
    REQUIRE( !json.empty() );
    read_rpc->get_input_node().create_datanode("filter", json);

    auto read_result = (*read_rpc)(provider.get_session());

    runner = schema.create_datanode("ydktest-sanity:runner", "");
    number8 = runner.create_datanode("ytypes/built-in-t/number8", "5");

    json = s.encode(runner, EncodingFormat::JSON, false);
    CHECK( !json.empty());
    //call update
    std::shared_ptr<ydk::path::Rpc> update_rpc { schema.create_rpc("ydk:update") };
    update_rpc->get_input_node().create_datanode("entity", json);
    (*update_rpc)(provider.get_session());
}

TEST_CASE("restconf_provider_action")
{
    ydk::path::Repository repo{TEST_HOME};
    ydk::RestconfServiceProvider provider{repo, "localhost", "admin", "admin", 12306, EncodingFormat::JSON};

    ydk::path::RootSchemaNode& schema = provider.get_session().get_root_schema();

    ydk::path::Codec s{};

    auto & runner = schema.create_datanode("ydktest-sanity-action:data");
    REQUIRE_THROWS_AS((runner)(provider.get_session()), ydk::YOperationNotSupportedError);
}

TEST_CASE("restconf_session_crud")
{
    ydk::path::Repository repo{TEST_HOME};
    ydk::path::RestconfSession session{repo, "localhost", "admin", "admin", 12306, EncodingFormat::JSON};
    ydk::path::RootSchemaNode& schema = session.get_root_schema();
    ydk::path::Codec s{};

    //first delete
    auto & runner = schema.create_datanode("ydktest-sanity:runner", "");

    std::shared_ptr<ydk::path::Rpc> delete_rpc { schema.create_rpc("ydk:delete") };
    auto json = s.encode(runner, EncodingFormat::JSON, false);
    delete_rpc->get_input_node().create_datanode("entity", json);
    (*delete_rpc)(session);

    // config
    runner.create_datanode("ytypes/built-in-t/number8", "3");
    json = s.encode(runner, EncodingFormat::JSON, false);
    CHECK( !json.empty());

    std::shared_ptr<ydk::path::Rpc> create_rpc { schema.create_rpc("ydk:create") };
    create_rpc->get_input_node().create_datanode("entity", json);
    (*create_rpc)(session);

    //read
    auto & runner_read = schema.create_datanode("ydktest-sanity:runner", "");
    json = s.encode(runner_read, EncodingFormat::JSON, false);

    std::shared_ptr<ydk::path::Rpc> read_rpc { schema.create_rpc("ydk:read") };
    read_rpc->get_input_node().create_datanode("filter", json);
    auto read_result = (*read_rpc)(session);
    CHECK( read_result != nullptr );
    json = s.encode(*read_result, EncodingFormat::JSON, false);
    CHECK( R"({"ydktest-sanity:runner":{"ytypes":{"built-in-t":{"number8":3}}}})" == json );

    // delete config
    (*delete_rpc)(session);
}
