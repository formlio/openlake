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

import forml
import pandas
from forml.provider.feed import lazy

from openlake import cache


class Partition(abc.ABC):
    """Provider specific representation of a data partition."""

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.key == self.key

    @property
    @abc.abstractmethod
    def key(self) -> str:
        """Get the partition identifier key."""


PayloadT = typing.TypeVar('PayloadT')
PartitionT = typing.TypeVar('PartitionT', bound=Partition)


class Origin(typing.Generic[PartitionT, PayloadT], lazy.Origin[PartitionT], metaclass=abc.ABCMeta):
    """Abstract base class for OpenLake data-source integrations."""

    @property
    def _cachedir(self) -> pathlib.Path:
        """Root directory for this origin cache."""
        return cache.DIR / self.__class__.__module__.rsplit('.', 1)[-1]

    def load(self, partition: typing.Optional[lazy.Partition]) -> pandas.DataFrame:
        """Caching loader."""
        key = self.key
        if partition:
            key += f':{partition.key}'
        return cache.dataframe(key, lambda: self.parse(partition, self.fetch(partition)), self._cachedir)

    @abc.abstractmethod
    def fetch(self, partition: typing.Optional[lazy.Partition]) -> PayloadT:
        """Fetch the content and return a data content object.

        Args:
            partition: Partition identifiers to be fetched.

        Returns:
            Data content object in a generic PayloadT to be parsed.
        """

    @abc.abstractmethod
    def parse(self, partition: typing.Optional[lazy.Partition], content: PayloadT) -> pandas.DataFrame:
        """Parse the origin dataset.

        Args:
            partition: Partition identifier representing the content.
            content: The data content object as returned by `.fetch()`.

        Returns:
            Data in Pandas DataFrame format.
        """


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
