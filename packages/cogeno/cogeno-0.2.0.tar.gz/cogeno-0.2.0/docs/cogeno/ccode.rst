..
    Copyright (c) 2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_modules_ccode:

C code generation functions
###########################

The ccode module supports code generation for the C language.

To use the module in inline code generation import it by:

::

    cogeno.import_module('ccode')

In case you want to use the ccode module in another Python
project import it by:

::

    import cogeno.modules.ccode


.. doxygenfunction:: cogeno::modules::ccode::outl_config_guard()
    :project: cogeno

.. doxygenfunction:: cogeno::modules::ccode::outl_config_unguard()
    :project: cogeno

.. doxygenfunction:: cogeno::modules::ccode::out_comment()
    :project: cogeno

.. doxygenfunction:: cogeno::modules::ccode::outl_edts_defines()
    :project: cogeno

