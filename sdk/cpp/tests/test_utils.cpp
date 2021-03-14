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
#include <sstream>

#include <ydk/entity_data_node_walker.hpp>
#include <ydk/filters.hpp>

#include "test_utils.hpp"

using namespace std;

static std::string yfilter2str(ydk::path::DataNode* dn)
{
    auto filter = ydk::get_data_node_yfilter(dn);
    if (filter == ydk::YFilter::not_set)
        return "";
    std::string filter_str = " yfilter=";
    filter_str += to_string(filter);
    return filter_str;
}

std::string print_tree(ydk::path::DataNode* dn, const std::string& indent)
{
    std::ostringstream buffer;
    try {
        auto filter = yfilter2str(dn);
        ydk::path::Statement s = dn->get_schema_node().get_statement();
        if(s.keyword == "leaf" || s.keyword == "leaf-list" || s.keyword == "anyxml" || s.keyword == "anydata") {
            auto val = dn->get_value();
            buffer << indent << "<" << s.arg << filter << ">" << val << "</" << s.arg << ">" << std::endl;
        }
         else {
            std::string child_indent{indent};
            child_indent+="  ";
            buffer << indent << "<" << s.arg << filter << ">" << std::endl;
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
    cout << data_node_to_xml(dn) << endl;
}

std::string data_node_to_xml(shared_ptr<ydk::path::DataNode> dn)
{
    std::ostringstream buffer;
    try {
        buffer << "\n=====>  Printing DataNode: '" << dn->get_path() << "'" << endl;
        buffer << print_tree(dn.get(), " ");
    }
    catch (ydk::path::YCoreError &ex) {
        std::cout << ex.what() << std::endl;
    }
    return buffer.str();
}

std::string data_node_to_xml(ydk::path::DataNode & dn)
{
    std::ostringstream buffer;
    try {
        buffer << "\n=====>  Printing DataNode: '" << dn.get_path() << "'" << endl;
        buffer << print_tree(&dn, " ");
    }
    catch (ydk::path::YCoreError &ex) {
        std::cout << ex.what() << std::endl;
    }
    return buffer.str();
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
    return print_tree( &dn, "");
}
