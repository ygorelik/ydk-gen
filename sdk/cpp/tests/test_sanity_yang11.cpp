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

#include "ydk/netconf_provider.hpp"
#include "ydk/crud_service.hpp"
#include "ydk_ydktest/ydktest_sanity_yang11.hpp"

#include "config.hpp"
#include "catch.hpp"

using namespace ydk;
using namespace ydktest;
using namespace std;

TEST_CASE("test_yang11_container")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    // DELETE
    auto container = make_unique<ydktest_sanity_yang11::BackwardIncompatible>();
    bool reply = crud.delete_(provider, *container);
    REQUIRE(reply);

    // CREATE
    container->test_node = "Testing node";
    reply = crud.create(provider, *container);
    REQUIRE(reply);

    // READ and TEST
    auto filter = ydktest_sanity_yang11::BackwardIncompatible();
    auto read_entity = crud.read(provider, filter);
    REQUIRE(read_entity != nullptr);

    auto container_read = dynamic_cast<ydktest_sanity_yang11::BackwardIncompatible*>(read_entity.get());
    REQUIRE(container_read->test_node.value == "Testing node");

    // DELETE
    container = make_unique<ydktest_sanity_yang11::BackwardIncompatible>();
    reply = crud.delete_(provider, *container);
    REQUIRE(reply);
}
