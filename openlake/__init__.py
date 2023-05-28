# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Openlake ForML feed."""

__version__ = '0.6'

import typing

from forml.provider.feed import lazy

from openlake.provider import kaggle, sklearn

#: Default list of origin integrations.
ORIGINS: typing.Collection[lazy.Origin] = {kaggle.Avazu(), kaggle.Titanic(), sklearn.BreastCancer(), sklearn.Iris()}


class Lite(lazy.Feed):
    """ForML feed providing access to a number of public datasets.

    External data sources are fetched using the Openlake integrations and cached locally.

    The provider can be enabled using the following :ref:`platform configuration
    <forml:platform-config>`:

    .. code-block:: toml
       :caption: config.toml

        [FEED.openlake]
        provider = "openlake:Lite"

    Important:
        Select the relevant :ref:`extras to install <install-extras>` OpenLake together with the
        particular integrations (e.g. Kaggle, Scikit-learn, etc.).
    """

    def __init__(self, *origins: lazy.Origin):
        if not origins:
            origins = ORIGINS
        super().__init__(*origins)
