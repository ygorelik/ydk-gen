..
  #  YDK-YANG Development Kit
  #  Copyright 2016 Cisco Systems. All rights reserved
  # *************************************************************
  # Licensed to the Apache Software Foundation (ASF) under one
  # or more contributor license agreements.  See the NOTICE file
  # distributed with this work for additional information
  # regarding copyright ownership.  The ASF licenses this file
  # to you under the Apache License, Version 2.0 (the
  # "License"); you may not use this file except in compliance
  # with the License.  You may obtain a copy of the License at
  #
  #   http:#www.apache.org/licenses/LICENSE-2.0
  #
  #  Unless required by applicable law or agreed to in writing,
  # software distributed under the License is distributed on an
  # "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  # KIND, either express or implied.  See the License for the
  # specific language governing permissions and limitations
  # under the License.
  # *************************************************************
  # This file has been modified by Yan Gorelik, YDK Solutions.
  # All modifications in original under CiscoDevNet domain
  # introduced since October 2019 are copyrighted.
  # All rights reserved under Apache License, Version 2.0.
  # *************************************************************

Errors
======

.. module:: ydk.errors
    :synopsis: YDK Exceptions

This module contains YDK Python errors classes. These errors are thrown in case of data not conforming to the yang model or due to a server-side error.

.. py:exception:: YError

    Bases: :exc:`exceptions.Exception`

    Base class for Y Errors. The subclasses give a specialized view of the error that has occurred.

.. py:exception:: YCoreError

    Bases: :exc:`ydk.errors.YError`

    Core Error. Base exception class for all YDK core errors.

.. py:exception:: YCodecError

    Bases: :exc:`ydk.errors.YCoreError`

    Codec Error. Thrown when a Path Codec fails to perform encoding or decoding.

.. py:exception:: YModelError

    Bases: :exc:`ydk.errors.YError`

    Model Error. Thrown when a model constraint is violated.

.. py:exception:: YServiceProviderError

    Bases: :exc:`ydk.errors.YError`

    Exception for Service Provider. Thrown in case of a server-side error.

.. py:exception:: YClientError

    Bases: :exc:`ydk.errors.YError`

    Exception for client connection

.. py:exception:: YIllegalStateError

    Bases: :exc:`ydk.errors.YError`

    Illegal State Error. Thrown when an operation/service is invoked on an object that is not in the right state. Use the error_msg for the error.

.. py:exception:: YInvalidArgumentError

    Bases: :exc:`ydk.errors.YError`

    Invalid Argument. Use the error_msg for the error.

.. py:exception:: YOperationNotSupportedError

    Bases: :exc:`ydk.errors.YError`

    Operation Not Supported Error. Thrown when an operation is not supported.

.. py:exception:: YServiceError

    Bases: :exc:`ydk.errors.YError`

    Exception for Service Side Validation.
