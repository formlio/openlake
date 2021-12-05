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
"""
Scikit-learn datasets providers.
"""
import typing

import numpy
import pandas

from forml.io import dsl
from openschema import sklearn as schema
from openlake import provider

try:
    from sklearn import datasets
except Exception as err:  # pylint: disable=broad-except
    datasets = provider.Unavailable('sklearn', err)

if typing.TYPE_CHECKING:
    from sklearn import utils


class BreastCancer(provider.Origin['utils.Bunch']):
    """Breast cancer dataset."""

    @property
    def source(self) -> dsl.Queryable:
        return schema.BreastCancer

    def fetch(
        self, columns: typing.Optional[typing.Iterable[dsl.Feature]], predicate: typing.Optional[dsl.Feature]
    ) -> 'utils.Bunch':
        return datasets.load_breast_cancer()

    def parse(
        self,
        content: 'utils.Bunch',
        columns: typing.Optional[typing.Iterable[dsl.Feature]],
        predicate: typing.Optional[dsl.Feature],
    ) -> pandas.DataFrame:
        data = numpy.column_stack([content['data'], content['target']])
        return pandas.DataFrame(data, columns=[f.name for f in self.source.features])  # pylint: disable=not-an-iterable


class Iris(provider.Origin['utils.Bunch']):
    """Iris dataset."""

    @property
    def source(self) -> dsl.Queryable:
        return schema.Iris

    def fetch(
        self, columns: typing.Optional[typing.Iterable[dsl.Feature]], predicate: typing.Optional[dsl.Feature]
    ) -> 'utils.Bunch':
        return datasets.load_iris()

    def parse(
        self,
        content: 'utils.Bunch',
        columns: typing.Optional[typing.Iterable[dsl.Feature]],
        predicate: typing.Optional[dsl.Feature],
    ) -> pandas.DataFrame:
        data = numpy.column_stack([content['data'], content['target']])
        return pandas.DataFrame(data, columns=[f.name for f in self.source.features])  # pylint: disable=not-an-iterable
