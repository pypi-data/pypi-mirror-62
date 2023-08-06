..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_modules_edts:

Extended device tree specification (EDTS) database
##################################################

The EDTS database module extracts device tree information from the device tree
specification.

THE EDTS database is a key value store. The keys are pathes to the device tree information.

You may get access to the database by :func:`cogeno.edts()`.

In case you want to use the extended device tree database in another Python
project import it by:

::

    import cogeno.modules.edtsdatabase


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   edts_bindings
