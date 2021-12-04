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

"""Parser implementations."""

import abc
import types
import typing

import pandas
from forml.io import dsl

from openlake import provider


class Mixin(typing.Generic[provider.Format], abc.ABC):
    """Parser mixin base class."""

    @abc.abstractmethod
    def parse(
        self,
        content: provider.Format,
        columns: typing.Optional[typing.Iterable[dsl.Feature]],
        predicate: typing.Optional[dsl.Feature],
    ) -> pandas.DataFrame:
        """Load the origin dataset."""


class CSV(Mixin[typing.IO], metaclass=abc.ABCMeta):
    """CSV parser mixin."""

    CSV_PARAMS: typing.Mapping = types.MappingProxyType({})

    def parse(
        self,
        content: typing.IO,
        columns: typing.Optional[typing.Iterable[dsl.Feature]],
        predicate: typing.Optional[dsl.Feature],
    ) -> pandas.DataFrame:
        return pandas.read_csv(content, **self.CSV_PARAMS)
