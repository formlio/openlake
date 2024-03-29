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

    $ pip install --constraint https://raw.githubusercontent.com/formlio/openlake/main/constraints.txt 'openlake[all]'


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
| sklearn   | ``pip install 'openlake[sklearn]'``   | Scikit-learn datasets provider               |
+-----------+---------------------------------------+----------------------------------------------+
| providers | ``pip install 'openlake[providers]'`` | All providers combined                       |
+-----------+---------------------------------------+----------------------------------------------+

Configuration
-------------

This Openlake feed becomes available within the ForML platform after referencing it from
the :doc:`platform configuration <forml:platform>`. Following is snippet of the configuration file
enabling the :class:`openlake.Lite` feed:

.. code-block:: toml
   :caption: config.toml

    [FEED.openlake]
    provider = "openlake:Lite"


Kaggle API Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^

In order to fetch the datasets using the Kaggle API, you must first configure your access token
stored under the :file:`~/.kaggle/kaggle.json`. For more details, see the `Kaggle API
Documentation <https://www.kaggle.com/docs/api>`_.

 .. attention::
    You must read and accept the rules of *each individual Kaggle competition* in order to download
    its dataset. This cannot be done programmatically - you must do this by visiting the Kaggle
    website and accepting the rules there.
