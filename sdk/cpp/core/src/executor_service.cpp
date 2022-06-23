// YANG Development Kit
// Copyright 2016 Cisco Systems. All rights reserved
//
////////////////////////////////////////////////////////////////
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
// -------------------------------------------------------------
// This file has been modified by Yan Gorelik, YDK Solutions.
// All modifications in original under CiscoDevNet domain
// introduced since October 2019 are copyrighted.
// All rights reserved under Apache License, Version 2.0.
//////////////////////////////////////////////////////////////////

#include "entity_data_node_walker.hpp"
#include "entity_util.hpp"
#include "executor_service.hpp"
#include "logger.hpp"
#include "service_provider.hpp"
#include "types.hpp"


using namespace std;

namespace ydk {

ExecutorService::ExecutorService()
{
}

ExecutorService::~ExecutorService()
{
}

shared_ptr<Entity> ExecutorService::execute_rpc(
    ServiceProvider& provider,
    Entity & rpc_entity,
    shared_ptr<Entity> top_entity)
{
    // Get the operation - RPC Name
    auto const & operation = rpc_entity.get_segment_path();

    // Create RPC instance
    path::RootSchemaNode & root_schema = provider.get_session().get_root_schema();
    shared_ptr<path::Rpc> rpc = root_schema.create_rpc(operation);
    path::DataNode & rpc_input = rpc->get_input_node();

    // Handle input
    auto input = rpc_entity.get_child_by_name("input", "");
    if (input != nullptr && (input->has_operation() || input->has_data() || input->is_presence_container))
    {
        walk_children(*input, rpc_input);
    }

    // Execute
    auto result_datanode = (*rpc)(provider.get_session());

    // Handle output
    auto output = rpc_entity.get_child_by_name("output", "");
    if (output != nullptr && result_datanode != nullptr && top_entity != nullptr)
    {
        auto filter = result_datanode->get_children()[0].get();

        get_entity_from_data_node(filter, top_entity);
        return top_entity;
    }
    else
        return nullptr;
}

}
