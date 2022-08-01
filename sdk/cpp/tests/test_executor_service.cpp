/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2016-2019 Cisco Systems, All rights reserved.
 -------------------------------------------------------------------
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

#include <ydk/crud_service.hpp>
#include <ydk/codec_provider.hpp>
#include <ydk/codec_service.hpp>
#include <ydk/netconf_provider.hpp>
#include <ydk/executor_service.hpp>
#include <ydk/types.hpp>

#include <ydk_ydktest/ydktest_sanity.hpp>
#include <ydk_ydktest/ietf_netconf.hpp>
#include <ydk_ydktest/ietf_netconf_monitoring.hpp>
#include <ydk_ydktest/openconfig_bgp.hpp>

#include "config.hpp"
#include "catch.hpp"

using namespace ydk;
using namespace ydktest;
using namespace std;

TEST_CASE("es_close_session_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::CloseSession rpc{};

    std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    REQUIRE(reply == nullptr);
}

// persist-id is broken?
TEST_CASE("es_commit_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::Commit rpc{};
    Empty e;
    e.set = true;
    rpc.input->confirmed = e;
    rpc.input->confirm_timeout = 5;
    // rpc.input->persist = "2";
    // rpc.input->persist_id = "2";

    std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    result = reply == nullptr;
    REQUIRE(result);

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    reply = es.execute_rpc(provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

TEST_CASE("es_copy_config_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::CopyConfig rpc{};
    Empty e;
    e.set = true;
    rpc.input->target->candidate = Empty();
    rpc.input->source->running = e;

    std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    result = reply == nullptr;
    REQUIRE(result);

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    reply = es.execute_rpc(provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

// issues in netsim
// If-feature 'url' is not enabled in confd-7.3, hence expected failure execute RPC
TEST_CASE("es_delete_config_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::DeleteConfig rpc{};

    rpc.input->target->url = "http://test";
    // std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);

    CHECK_THROWS_AS(
        es.execute_rpc(provider, rpc),
        YServiceProviderError
    );

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    std::shared_ptr<Entity> reply = es.execute_rpc(
        provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

TEST_CASE("es_discard_changes_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::DiscardChanges rpc{};

    std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    result = reply == nullptr;
    REQUIRE(result);

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    reply = es.execute_rpc(provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

// edit_config, get_config, commit, get
TEST_CASE("es_edit_config_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};
    CodecServiceProvider codec_provider{EncodingFormat::XML};
    CodecService codec_service{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    // runner and filter
    auto runner = make_shared<ydktest_sanity::Runner>();
    runner->one->number = 1;
    runner->one->name = "runner-one-name";
    std::string runner_xml = codec_service.encode(codec_provider, *runner, true);

    auto filter = make_unique<ydktest_sanity::Runner>();
    std::string filter_xml = codec_service.encode(codec_provider, *filter, true);

    // Edit Config Rpc
    ietf_netconf::EditConfig edit_config_rpc{};
    edit_config_rpc.input->target->candidate = Empty();
    edit_config_rpc.input->config = runner_xml;

    std::shared_ptr<Entity> reply = es.execute_rpc(provider, edit_config_rpc);
    CHECK(reply == nullptr);

    // Get Config Rpc
    ietf_netconf::GetConfig get_config_rpc{};
    get_config_rpc.input->source->candidate = Empty();
    get_config_rpc.input->filter = filter_xml;

    auto get_runner = make_shared<ydktest_sanity::Runner>();
    reply = es.execute_rpc(provider, get_config_rpc, get_runner);
    REQUIRE(reply);
    auto runner_entity = dynamic_cast<ydktest_sanity::Runner*>(reply.get());
    CHECK(*runner == *runner_entity);

    // Commit Rpc
    ietf_netconf::Commit commit_rpc{};
    reply = es.execute_rpc(provider, commit_rpc);
    CHECK(reply == nullptr);

    // Get Rpc
    ietf_netconf::Get get_rpc{};
    get_rpc.input->filter = filter_xml;

    reply = es.execute_rpc(provider, get_rpc, runner);
    CHECK(reply);

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    reply = es.execute_rpc(provider, discard_rpc);
    CHECK(reply == nullptr);
}

// kill_session
TEST_CASE("es_kill_session_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::KillSession rpc{};
    rpc.input->session_id = 3;

   // std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    CHECK_THROWS_AS(
        es.execute_rpc(provider, rpc),
        YServiceProviderError
    );

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    std::shared_ptr<Entity> reply = es.execute_rpc(
        provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

// lock, unlock
TEST_CASE("es_lock_rpc")
{
    // provider
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    ietf_netconf::Lock lock_rpc{};
    lock_rpc.input->target->running = Empty();

    std::shared_ptr<Entity> reply = es.execute_rpc(provider, lock_rpc);
    CHECK(reply == nullptr);

    ietf_netconf::Unlock unlock_rpc{};
    unlock_rpc.input->target->running = Empty();

    reply = es.execute_rpc(provider, unlock_rpc);
    CHECK(reply == nullptr);
}

TEST_CASE("es_validate_rpc_1")
{
    path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::Validate rpc{};
    rpc.input->source->candidate = Empty();
    // rpc.input->source->config = r_1;
    std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    result = reply == nullptr;
    REQUIRE(result);

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    reply = es.execute_rpc(provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

TEST_CASE("es_validate_rpc_2")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    // clean up
    CrudService crud{};
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool result = crud.delete_(provider, *r_1);
    REQUIRE(result);

    ietf_netconf::Validate rpc{};
    Empty e;
    e.set = true;
    rpc.input->source->running = e;
    std::shared_ptr<Entity> reply = es.execute_rpc(provider, rpc);
    result = reply == nullptr;
    REQUIRE(result);

    // Discard Changes
    ietf_netconf::DiscardChanges discard_rpc{};
    reply = es.execute_rpc(provider, discard_rpc);
    result = reply == nullptr;
    REQUIRE(result);
}

TEST_CASE("es_get_schema_rpc")
{
    NetconfServiceProvider provider{"127.0.0.1", "admin", "admin", 12022};
    ExecutorService es{};

    auto rpc_entity = ietf_netconf_monitoring::GetSchema{};
    rpc_entity.input->identifier = "main";
    auto return_output_entity = make_shared<ietf_netconf_monitoring::GetSchema::Output>();
    auto reply = es.execute_rpc(provider, rpc_entity, return_output_entity);
    REQUIRE(reply);

    auto get_schema_rpc_output = dynamic_cast<ietf_netconf_monitoring::GetSchema::Output*>(return_output_entity.get());
    string module = get_schema_rpc_output->data.get();
    REQUIRE(module.compare(0, 13, "module main {") == 0);
}
