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

"""Opendata ForML feed."""

import types
import typing

import sqlalchemy
from forml import io
from forml.io import dsl, layout
from forml.io.dsl import parser as parsmod
from forml.lib.feed.reader.sql import alchemy
from sqlalchemy import sql
from sqlalchemy.engine import interfaces

from opendata import provider
from opendata.provider import kaggle, sklearn

__version__ = '0.1.dev0'
__author__ = 'ForML Authors'

ORIGINS: typing.Iterable[provider.Origin] = {kaggle.Titanic(), sklearn.BreastCancer(), sklearn.Iris()}


class _Tables(dsl.Source.Visitor):
    """Visitor extracting dsl.Table instances from the given query."""

    def __init__(self):
        self._match: set[dsl.Table] = set()

    @classmethod
    def extract(cls, query: dsl.Query) -> frozenset[dsl.Table]:
        """Frontend method for extracting tables from the given query."""
        return cls()(query)

    def __call__(self, query: dsl.Query) -> frozenset[dsl.Table]:
        """Apply this visitor to the given query.

        Args:
            query: Query to dissect.

        Returns:
            Set of dsl.Table instances.
        """
        query.accept(self)
        return frozenset(self._match)

    def visit_table(self, source: dsl.Table) -> None:
        self._match.add(source)


class Local(io.Feed, alias='opendata'):
    """Local opendata feed."""

    class Reader(alchemy.Reader):
        """Extending the SQLAlchemy reader."""

        def __init__(
            self,
            sources: typing.Mapping[dsl.Source, parsmod.Source],
            features: typing.Mapping[dsl.Feature, parsmod.Feature],
            origins: typing.Iterable[provider.Origin],
            **kwargs,
        ):
            self._connection: interfaces.Connectable = sqlalchemy.create_engine('sqlite://')
            self._loaded: set[dsl.Queryable] = set()
            self._origins: dict[dsl.Queryable, provider.Origin] = {o.source: o for o in origins}
            super().__init__(sources, features, self._connection, **kwargs)

        def __call__(self, query: dsl.Query) -> layout.ColumnMajor:
            tables = _Tables.extract(query)
            for origin in (self._origins[t] for t in tables if t not in self._loaded and not self._loaded.add(t)):
                origin().to_sql(origin.name, self._connection, index=False)
            return super().__call__(query)

    def __init__(self, *origins: provider.Origin, **readerkw):
        if not origins:
            origins = ORIGINS
        self._sources: typing.Mapping[dsl.Source, sql.Selectable] = types.MappingProxyType(
            {o.source: sqlalchemy.table(o.name) for o in origins}
        )
        super().__init__(origins=frozenset(origins), **readerkw)

    @property
    def sources(self) -> typing.Mapping[dsl.Source, sql.Selectable]:
        return self._sources
