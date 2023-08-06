..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_api:

Cogeno API
##########

.. module:: cogeno
    :synopsis: Inline code generator

`cogeno` is a Python module that provides access to the public functions
of the class: ``CodeGenerator`` and the sub-classes of it. See
:ref:`cogeno_functions` for a description of all ``cogeno`` module's functions.

The interfaces listed hereafter are the internal interface of cogeno.

.. contents::
   :depth: 2
   :local:
   :backlinks: top

:mod:`CodeGenerator`
====================

.. doxygenclass:: cogeno::generator::CodeGenerator
    :project: cogeno
    :members:
    :undoc-members:

The ``CodeGenerator`` class includes (sub-classes) several mixin classes:

:mod:`ErrorMixin`
-----------------

.. doxygenclass:: cogeno::error::ErrorMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`GenericMixin`
-------------------

.. doxygenclass:: cogeno::generic::GenericMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`LockMixin`
----------------

.. doxygenclass:: cogeno::lock::LockMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`OptionsMixin`
-------------------

.. doxygenclass:: cogeno::options::OptionsMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`StdModulesMixin`
----------------------

.. doxygenclass:: cogeno::stdmodules::StdModulesMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`Context`
==============

.. doxygenclass:: cogeno::context::Context
    :project: cogeno
    :members:
    :undoc-members:
