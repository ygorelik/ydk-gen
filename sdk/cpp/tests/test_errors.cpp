/*  ----------------------------------------------------------------
 YDK - YANG Development Kit
 Copyright 2016-2019 Cisco Systems
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

#define TEST_MODULE LevelsTests
#include <string.h>
#include <iostream>

#include <ydk/netconf_provider.hpp>
#include <ydk/crud_service.hpp>
#include <ydk_ydktest/ydktest_sanity.hpp>
#include <ydk_ydktest/ydktest_sanity_types.hpp>

#include "catch.hpp"
#include "config.hpp"

using namespace ydk;
using namespace ydktest;
using namespace std;

#define CONTAINS_ERROR_MESSAGE \
            Catch::Contains("Invalid value") \
            || Catch::Contains("Failed to resolve") \
            || Catch::Contains("Unexpected character") \
            || Catch::Contains("does not satisfy the constraint") \
            || Catch::Contains("is an invalid value") \
            || Catch::Contains("is not a valid value") \
            || Catch::Contains("got unexpected data") \
            || Catch::Contains("YModelError")

TEST_CASE("int8_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->number8 = "test";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("int8_invalid_ignore_validation")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r = ydktest_sanity::Runner();
    bool reply = crud.delete_(provider, r);
    REQUIRE(reply);

    //CREATE
    r.ignore_validation = true;
    r.ytypes->built_in_t->number8 = "test";
    r.ytypes->built_in_t->number8 = YFilter::create;
    CHECK_THROWS_WITH(crud.update(provider, r), Catch::Contains("\"test\" is not a valid value"));
}

TEST_CASE("int16_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->number16 = "test";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("int64_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->number64 = "test";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("bits_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->bits_value["invalid"] = true;
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("deci_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->deci64 = "xyz";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("empty_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->emptee = 1;
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("enum_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->embeded_enum = ydktest_sanity::YdkEnumTest::none;
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);

    //CREATE
    r_1->ytypes->built_in_t->embeded_enum = "wrong";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("identity_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->identity_ref_value = "wrong";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("leaflist_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->identity_llist.append(1);
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("empty_invalid_1")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->emptee = 143;
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}


TEST_CASE("enum_leaflist_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->enum_llist.append(Empty());
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("int8_invalid_1")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->number8 = Empty();
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("leafref_invalid")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->leaf_ref->one->name_of_one = "test";
    r_1->leaf_ref->one->two->self_ref_one_name = "test";
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("leaflist_max_elements")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::local);
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::not_set);
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::remote);
    // r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::none);
    // CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE);
}

TEST_CASE("leaflist_duplicate")
{
    ydk::path::Repository repo{TEST_HOME};
    NetconfServiceProvider provider{repo, "127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::local);
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::not_set);
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::remote);
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::none);
    r_1->ytypes->built_in_t->enum_llist.append(ydktest_sanity::YdkEnumTest::none);
    CHECK_THROWS_WITH(crud.create(provider, *r_1), CONTAINS_ERROR_MESSAGE); //TODO
}

TEST_CASE("int8_valid_ignore_validation")
{
    NetconfServiceProvider provider{"127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->number8 = 88;
    r_1->ignore_validation = true;
    crud.create(provider, *r_1);

    //READ and VALIDATE
    auto rf = ydktest_sanity::Runner();
    rf.ignore_validation = true;
    auto r_ent = crud.read(provider, rf);
    REQUIRE(r_ent != nullptr);
    auto runner = dynamic_cast<ydktest_sanity::Runner*>(r_ent.get());
    REQUIRE(runner->ytypes->built_in_t->number8 == r_1->ytypes->built_in_t->number8);

    auto bintf = rf.ytypes->built_in_t;
    bintf->ignore_validation = true;
    auto bint_ent = crud.read(provider, *bintf);
    REQUIRE(bint_ent != nullptr);
    auto bint = dynamic_cast<ydktest_sanity::Runner::Ytypes::BuiltInT*>(bint_ent.get());
    REQUIRE(bint->number8 == r_1->ytypes->built_in_t->number8);
}

TEST_CASE("int8_list_ignore_validation")
{
    NetconfServiceProvider provider{"127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    //DELETE
    auto r_1 = make_unique<ydktest_sanity::Runner>();
    bool reply = crud.delete_(provider, *r_1);
    REQUIRE(reply);

    //CREATE
    r_1->ytypes->built_in_t->number8 = 88;
    r_1->ignore_validation = true;
    vector<Entity*> r_list{};
    r_list.push_back(r_1.get());
    crud.create(provider, r_list);

    //READ and VALIDATE
    auto rf = ydktest_sanity::Runner();
    auto bintf = rf.ytypes->built_in_t;
    bintf->ignore_validation = true;
    vector<Entity*> f_list{};
    f_list.push_back(bintf.get());

    auto bint_ent_list = crud.read(provider, f_list);
    REQUIRE(bint_ent_list.size() == 1);
    auto bint_ent = bint_ent_list[0];
    auto bint = dynamic_cast<ydktest_sanity::Runner::Ytypes::BuiltInT*>(bint_ent.get());
    REQUIRE(bint->number8 == r_1->ytypes->built_in_t->number8);
}

TEST_CASE("bool_value_invalid")
{
    NetconfServiceProvider provider{"127.0.0.1", "admin", "admin", 12022};
    CrudService crud{};

    auto runner = ydktest_sanity::Runner();
	runner.ytypes->built_in_t->bool_value = "a string";

	CHECK_THROWS_WITH(crud.create(provider, runner), CONTAINS_ERROR_MESSAGE);
}
