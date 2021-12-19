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
Openlake providers.
"""
import abc
import pathlib
import types
import typing

import pandas

import forml
from forml.io import dsl

from openlake import cache

Format = typing.TypeVar('Format')


class Origin(typing.Generic[Format], metaclass=abc.ABCMeta):
    """Openlake origin base class."""

    def __hash__(self):
        return hash(self.source)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.source == self.source

    def __call__(
        self,
        columns: typing.Optional[typing.Iterable[dsl.Feature]] = None,
        predicate: typing.Optional[dsl.Feature] = None,
    ) -> pandas.DataFrame:
        frame = self._load(columns, predicate)
        expected = {f.name for f in self.source.features}
        assert set(frame.columns) == expected, f'Column name mismatch: {expected.symmetric_difference(frame.columns)}'
        return frame.astype({f.name: f.kind.__native__ for f in self.source.features})

    @property
    def _cachedir(self) -> pathlib.Path:
        """Root directory for this origin cache."""
        return cache.DIR / self.__class__.__qualname__.lower()

    def _load(
        self, columns: typing.Optional[typing.Iterable[dsl.Feature]], predicate: typing.Optional[dsl.Feature]
    ) -> pandas.DataFrame:
        """Content loader with caching capabilities."""
        return cache.dataframe(
            repr(tuple(columns or [])) + repr(predicate),
            lambda: self.parse(self.fetch(columns, predicate), columns, predicate),
            self._cachedir,
        )

    @property
    def name(self) -> str:
        """Name to be used for internal (unique) referencing.

        Must be a valid identifier -> [_a-zA-Z][_a-zA-Z0-9]*
        """
        return repr(self.source)

    @property
    @abc.abstractmethod
    def source(self) -> dsl.Queryable:
        """The source query this origin provides."""

    @abc.abstractmethod
    def fetch(
        self, columns: typing.Optional[typing.Iterable[dsl.Feature]], predicate: typing.Optional[dsl.Feature]
    ) -> Format:
        """Fetch the content and return a file object."""

    @abc.abstractmethod
    def parse(
        self,
        content: Format,
        columns: typing.Optional[typing.Iterable[dsl.Feature]],
        predicate: typing.Optional[dsl.Feature],
    ) -> pandas.DataFrame:
        """Load the origin dataset."""


class Unavailable(types.ModuleType):
    """Placeholder for missing provider functionality that raises upon access."""

    class Error(forml.MissingError):
        """Custom exception for indicating access to an unavailable provider."""

    def __init__(self, name: str, error: Exception):
        super().__init__(name)
        self.__error__: Exception = error

    def __getattr__(self, item: str):
        raise self.Error(
            f'Provider {self.__name__} not available when accessing {item}: {self.__error__}.'
        ) from self.__error__
