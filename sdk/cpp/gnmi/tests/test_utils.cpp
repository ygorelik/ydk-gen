/// YANG Development Kit
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
//
//////////////////////////////////////////////////////////////////

#include <ydk/gnmi_service.hpp>
#include <ydk/entity_data_node_walker.hpp>

#include <ydk/filters.hpp>

#include "test_utils.hpp"

using namespace std;

using namespace ydk;
using namespace path;
using namespace ydktest;

std::string print_tree(ydk::path::DataNode* dn, const std::string& indent)
{
  ostringstream buffer;
  try {
    ydk::path::Statement s = dn->get_schema_node().get_statement();
    if(s.keyword == "leaf" || s.keyword == "leaf-list" || s.keyword == "anyxml" || s.keyword == "anydata") {
        auto val = dn->get_value();
        buffer << indent << "<" << s.arg << ">" << val << "</" << s.arg << ">" << std::endl;
    } else {
        std::string child_indent{indent};
        child_indent+="  ";
        buffer << indent << "<" << s.arg << ">" << std::endl;
        for(auto c : dn->get_children())
        	buffer << print_tree(c.get(), child_indent);
        buffer << indent << "</" << s.arg << ">" << std::endl;
    }
  }
  catch (ydk::path::YCoreError &ex) {
	  cout << ex.what() << endl;
  }
  return buffer.str();
}

void print_data_node(shared_ptr<ydk::path::DataNode> dn)
{
  try {
    cout << "\n=====>  Printing DataNode: '" << dn->get_path() << "'" << endl;
    cout << print_tree(dn.get(), " ");
  }
  catch (ydk::path::YCoreError &ex) {
    cout << ex.what() << endl;
  }
}

void print_entity(shared_ptr<ydk::Entity> entity, ydk::path::RootSchemaNode& root)
{
    ydk::path::DataNode& dn = get_data_node_from_entity( *entity, root);
    ydk::path::Statement s = dn.get_schema_node().get_statement();
    cout << "\n=====>  Printing DataNode: '" << s.arg << "'" << endl;
    cout << print_tree( &dn, " ");
}

string entity2string(shared_ptr<ydk::Entity> entity, ydk::path::RootSchemaNode& root)
{
    ydk::path::DataNode& dn = get_data_node_from_entity( *entity, root);
    ydk::path::Statement s = dn.get_schema_node().get_statement();
    return print_tree( &dn, " ");
}

void config_bgp(openconfig_bgp::Bgp& bgp)
{
    bgp.global->config->as = 65172;

    auto neighbor = make_shared<openconfig_bgp::Bgp::Neighbors::Neighbor>();
    neighbor->neighbor_address = "172.16.255.2";
    neighbor->config->neighbor_address = "172.16.255.2";
    neighbor->config->peer_as = 65172;

    bgp.neighbors->neighbor.append(neighbor);
}

void build_bgp_config(gNMIServiceProvider& provider)
{
    openconfig_bgp::Bgp bgp{};
    bgp.yfilter = YFilter::replace;
    config_bgp(bgp);

    gNMIService gs{};
    gs.set(provider, bgp);
}

void build_int_config(gNMIServiceProvider& provider)
{
    auto ifc = openconfig_interfaces::Interfaces::Interface();
    ifc.name = "Loopback10";
    ifc.config->name = "Loopback10";
    ifc.config->description = "Test";
    ifc.yfilter = YFilter::replace;

    gNMIService gs{};
    gs.set(provider, ifc);
}

void delete_bgp_config(gNMIServiceProvider& provider)
{
    openconfig_bgp::Bgp bgp{};
    bgp.yfilter = YFilter::delete_;

    gNMIService gs{};
    gs.set(provider, bgp);
}

void delete_int_config(gNMIServiceProvider& provider)
{
    openconfig_interfaces::Interfaces ifcs{};
    ifcs.yfilter = YFilter::delete_;

    gNMIService gs{};
    gs.set(provider, ifcs);
}
