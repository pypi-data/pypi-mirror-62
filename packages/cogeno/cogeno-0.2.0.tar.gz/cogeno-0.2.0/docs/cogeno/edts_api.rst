..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_edts_api:

edtsdb API
##########

.. module:: edtsdb
    :synopsis: Extended DTS database

`edtsdb` is a Python module with the primary class: ``EDTSDb``.

The basis for the edtsb module is the ``edtlib`` library.

.. contents::
   :depth: 2
   :local:
   :backlinks: top

:mod:`EDTSDb`
=============

.. doxygenclass:: cogeno::modules::edtsdb::database::EDTSDb
    :project: cogeno
    :members:
    :undoc-members:

The ``EDTSDb`` class includes (sub-classes) several mixin classes:

.. doxygenclass:: cogeno::modules::edtsdb::consumer::EDTSConsumerMixin
    :project: cogeno
    :members:
    :undoc-members:

.. doxygenclass:: cogeno::modules::edtsdb::extractor::EDTSExtractorMixin
    :project: cogeno
    :members:
    :undoc-members:

.. doxygenclass:: cogeno::modules::edtsdb::provider::EDTSProviderMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`edtlib`
==============

.. doxygenclass:: cogeno::modules::edtsdb::libraries::edtlib::EDT
    :project: cogeno
    :members:
    :undoc-members:

.. doxygenclass:: cogeno::modules::edtsdb::libraries::edtlib::Node
    :project: cogeno
    :members:
    :undoc-members:

.. doxygenclass:: cogeno::modules::edtsdb::libraries::edtlib::Register
    :project: cogeno
    :members:
    :undoc-members:

.. doxygenclass:: cogeno::modules::edtsdb::libraries::edtlib::ControllerAndData
    :project: cogeno
    :members:
    :undoc-members:
