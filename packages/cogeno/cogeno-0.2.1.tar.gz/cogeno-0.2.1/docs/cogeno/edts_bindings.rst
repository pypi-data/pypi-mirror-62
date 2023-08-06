..
    Copyright (c) 2018,2019 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_edts_bindings:

EDTS bindings
#############

The EDTS database module uses bindings (a kind of data schema) to know what data
to extract and to know the kind of data. A set of generic bindings controls
the extraction process. The generic bindings are part of the EDTS database module.

.. contents::
   :depth: 2
   :local:
   :backlinks: top

Fixed partition
===============

::

    include: fixed-partition.yaml

.. literalinclude:: ../../cogeno/modules/edtsdb/dts/bindings/fixed-partition.yaml
    :language: yaml
    :lines: 6-

Flash
=====

::

    include: flash.yaml

.. literalinclude:: ../../cogeno/modules/edtsdb/dts/bindings/flash.yaml
    :language: yaml
    :lines: 6-

Flash controller
================

::

    include: flash-controller.yaml

.. literalinclude:: ../../cogeno/modules/edtsdb/dts/bindings/flash-controller.yaml
    :language: yaml
    :lines: 6-

Partitions
==========

::

    include: partition.yaml

.. literalinclude:: ../../cogeno/modules/edtsdb/dts/bindings/partition.yaml
    :language: yaml
    :lines: 6-

SoC non-volatile flash
======================

::

    include: soc-nv-flash.yaml

.. literalinclude:: ../../cogeno/modules/edtsdb/dts/bindings/soc-nv-flash.yaml
    :language: yaml
    :lines: 6-


