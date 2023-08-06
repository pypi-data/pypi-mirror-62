..
    Copyright (c) 2004-2015 Ned Batchelder
    SPDX-License-Identifier: MIT
    Copyright (c) 2018 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_functions:

Code generation functions
#########################

A module called ``cogeno`` provides the core functions for inline
code generation. It encapsulates all the functions to retrieve information
(options, device tree properties, CMake variables, config properties) and
to output the generated code.

.. contents::
   :depth: 2
   :local:
   :backlinks: top

The ``cogeno`` module is automatically imported by all code snippets. No
explicit import is necessary.

.. note::
    The ``cogeno`` module provides the public functions of the code generator
    'mixin' classes as cogeno functions. Instead of:

        **cogeno.xxx.XxxMixin.func(self, ...)**

    you have to write:

        **cogeno.func(...)**

Output
******

cogeno.out(sOut='', dedent=False, trimblanklines=False)
-------------------------------------------------------

.. doxygenfunction:: cogeno::output::OutputMixin::out()
    :project: cogeno


cogeno.outl(sOut='', dedent=False, trimblanklines=False)
--------------------------------------------------------

.. doxygenfunction:: cogeno::output::OutputMixin::outl()
    :project: cogeno


The cogeno module also provides a set of convenience functions:


Code generation module import
*****************************

cogeno.import_module(name)
--------------------------

.. doxygenfunction:: cogeno::importmodule::ImportMixin::import_module()
    :project: cogeno

See :ref:`cogeno_modules` for the available modules.

Template file inclusion
***********************

cogeno.out_include(include_file)
--------------------------------

.. doxygenfunction:: cogeno::include::IncludeMixin::out_include()
    :project: cogeno

cogeno.guard_include()
----------------------

.. doxygenfunction:: cogeno::include::IncludeMixin::guard_include()
    :project: cogeno


Configuration property access
*****************************

cogeno.config_property(property_name [, default="<unset>"])
-----------------------------------------------------------

.. doxygenfunction:: cogeno::stdmodules::stdmodules::config_property()
    :project: cogeno

See :ref:`cogeno_invoke_cogeno` and :ref:`cogeno_build` for how to provide config
variables to cogeno.

CMake variable access
*********************

.. function:: cogeno.cmake_variable(variable_name [, default="<unset>"])

    Get the value of a CMake variable. If variable_name is not provided to
    cogeno by CMake the default value is returned.

    See :ref:`cogeno_invoke_cogeno` and :ref:`cogeno_build` for how to provide CMake
    variables to cogeno.

    A typical set of CMake variables that are not available in the
    :file:`CMakeCache.txt` file and have to be provided as defines
    to cogeno if needed:

    - "PROJECT_NAME"
    - "PROJECT_SOURCE_DIR"
    - "PROJECT_BINARY_DIR"
    - "CMAKE_SOURCE_DIR"
    - "CMAKE_BINARY_DIR"
    - "CMAKE_CURRENT_SOURCE_DIR"
    - "CMAKE_CURRENT_BINARY_DIR"
    - "CMAKE_CURRENT_LIST_DIR"
    - "CMAKE_FILES_DIRECTORY"
    - "CMAKE_PROJECT_NAME"
    - "CMAKE_SYSTEM"
    - "CMAKE_SYSTEM_NAME"
    - "CMAKE_SYSTEM_VERSION"
    - "CMAKE_SYSTEM_PROCESSOR"
    - "CMAKE_C_COMPILER"
    - "CMAKE_CXX_COMPILER"
    - "CMAKE_COMPILER_IS_GNUCC"
    - "CMAKE_COMPILER_IS_GNUCXX"

.. function:: cogeno.cmake_cache_variable(variable_name [, default="<unset>"])

    Get the value of a CMake variable from CMakeCache.txt. If variable_name
    is not given in CMakeCache.txt the default value is returned.

Extended device tree database access
************************************

.. function:: cogeno.edts()

    Get the extended device tree database.

    :return: extended device tree database

    See :ref:`cogeno_invoke_cogeno` and :ref:`cogeno_build` for how to provide all
    files to enable cogeno to build the extended device tree database.

Guarding chunks of source code
******************************

.. function:: cogeno.outl_guard_config(property_name)

    Write a guard (#if [guard]) C preprocessor directive to output.

    If there is a configuration property of the given name the property value
    is used as guard value, otherwise it is set to 0.

    :param property_name: Name of the configuration property.

.. function:: cogeno.outl_unguard_config(property_name)

    Write an unguard (#endif) C preprocessor directive to output.

    This is the closing command for cogeno.outl_guard_config().

    :param property_name: Name of the configuration property.

Error handling
**************

.. function:: cogeno.error(msg='Error raised by cogeno.' [, frame_index=0] [, snippet_lineno=0])

    Raise a cogeno.Error exception.

    Instead of raising standard python errors, cogen generators can use
    this function. Extra information is added that maps the python snippet
    line seen by the Python interpreter to the line of the file that inlines
    the python snippet.

    :param msg: Exception message.
    :param frame_index: Call frame index. The call frame offset of the function
                        calling cogeno.error(). Zero if directly called in a
                        snippet. Add one for every level of function call.
    :param snippet_lineno: Line number within snippet.

Logging
*******

cogeno.log(message, message_type=None, end="\n", logonly=True)
--------------------------------------------------------------

.. doxygenfunction:: cogeno::log::LogMixin::log()
    :project: cogeno

cogeno.msg(message)
-------------------

.. doxygenfunction:: cogeno::log::LogMixin::msg()
    :project: cogeno

cogeno.warning(message)
-----------------------

.. doxygenfunction:: cogeno::log::LogMixin::warning()
    :project: cogeno

cogeno.prout(message, end="\n")
-------------------------------

.. doxygenfunction:: cogeno::log::LogMixin::prout()
    :project: cogeno

cogeno.prerr(message, end="\n")
-------------------------------

.. doxygenfunction:: cogeno::log::LogMixin::prerr()
    :project: cogeno

Standard Modules - config
*************************

cogeno.config_properties()
--------------------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::config_properties()
    :project: cogeno

cogeno.config_property(property_name, default="<unset>")
--------------------------------------------------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::config_property()
    :project: cogeno

