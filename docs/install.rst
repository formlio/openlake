 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at
 ..   http://www.apache.org/licenses/LICENSE-2.0
 .. Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

.. _install:

Installation
============

To install Openlake, simply use :doc:`pip <pip:cli/pip_install>`:

.. code-block:: console

    $ pip install --constraints https://raw.githubusercontent.com/formlio/openlake/main/constraints.txt 'openlake[all]'


.. _install-extras:

Extra Options
-------------

+-----------+---------------------------------------+----------------------------------------------+
| Feature   | Install Command                       | Description                                  |
+===========+=======================================+==============================================+
| all       | ``pip install 'openlake[all]'``       | All providers                                |
+-----------+---------------------------------------+----------------------------------------------+
| dev       | ``pip install 'openlake[dev]'``       | Openlake development tools                   |
+-----------+---------------------------------------+----------------------------------------------+
| docs      | ``pip install 'openlake[docs]'``      | Documentation publishing dependencies        |
+-----------+---------------------------------------+----------------------------------------------+
| kaggle    | ``pip install 'openlake[kaggle]'``    | Kaggle datasets provider                     |
+-----------+---------------------------------------+----------------------------------------------+
| sklearn   | ``pip install 'openlake[sklearn]'``   | Sklearn datasets provider                    |
+-----------+---------------------------------------+----------------------------------------------+
| providers | ``pip install 'openlake[providers]'`` | All providers combined                       |
+-----------+---------------------------------------+----------------------------------------------+

Configuration
-------------

This Openlake feed becomes available within the ForML platform after referencing it from
the :doc:`platform configuration <forml:platform>`. Following is snippet of the configuration file
enabling the :class:`openlake.Local` feed:

.. code-block:: toml
   :caption: config.toml

    [FEED.openlake]
    provider = "openlake:Local"
