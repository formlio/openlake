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
Kaggle datasets providers.
"""
import abc
import collections
import functools
import logging
import os
import pathlib
import typing

import forml
from forml import setup
from forml.io import dsl
from openschema import kaggle as schema

from openlake import fetcher, parser, provider

try:
    import kaggle
except Exception as err:  # pylint: disable=broad-except
    kaggle = provider.Unavailable('kaggle', err)


LOGGER = logging.getLogger(__name__)


class Partition(provider.Partition, collections.namedtuple('Partition', 'columns, filename')):
    """Kaggle data partition representation."""

    columns: tuple[dsl.Column]
    filename: str

    def __new__(cls, columns: typing.Sequence[dsl.Column], filename: str):
        return super().__new__(cls, tuple(columns), filename)

    @functools.cached_property
    def key(self) -> str:
        return pathlib.Path(self.filename).with_suffix('').name


class File(fetcher.Mixin[Partition, typing.IO], metaclass=abc.ABCMeta):
    """Kaggle file provider."""

    COMPETITION: str = abc.abstractmethod
    PARTITIONS: tuple[Partition] = abc.abstractmethod

    def partitions(
        self, columns: typing.Collection[dsl.Column], predicate: typing.Optional[dsl.Predicate]
    ) -> typing.Iterable[Partition]:
        columns = set(columns)
        for partition in self.PARTITIONS:
            if columns.issubset(partition.columns):
                return tuple([partition])
        raise forml.MissingError('No partition satisfy the column requirement')

    def fetch(self, partition: typing.Optional[Partition]) -> typing.IO:
        LOGGER.info('Fetching %s from %s', partition.filename, self.COMPETITION)
        kaggle.api.competition_download_file(self.COMPETITION, partition.filename, setup.tmpdir, force=True, quiet=True)
        return open(os.path.join(setup.tmpdir, partition.filename), 'rb')


class Titanic(File, parser.CSV, provider.Origin):
    """Titanic dataset."""

    COMPETITION = 'titanic'
    PARTITIONS = (
        Partition(
            (
                schema.Titanic.PassengerId,
                schema.Titanic.Pclass,
                schema.Titanic.Name,
                schema.Titanic.Sex,
                schema.Titanic.Age,
                schema.Titanic.SibSp,
                schema.Titanic.Parch,
                schema.Titanic.Ticket,
                schema.Titanic.Fare,
                schema.Titanic.Cabin,
                schema.Titanic.Embarked,
            ),
            'test.csv',
        ),  # Testset partition
        Partition(schema.Titanic.features, 'train.csv'),  # Trainset partition
    )

    @property
    def source(self) -> dsl.Source:
        return schema.Titanic


class Avazu(File, parser.CSV, provider.Origin):
    """Avazu dataset."""

    COMPETITION = 'avazu-ctr-prediction'
    PARTITIONS = (
        Partition(
            (
                schema.Avazu.id,
                schema.Avazu.hour,
                schema.Avazu.C1,
                schema.Avazu.banner_pos,
                schema.Avazu.site_id,
                schema.Avazu.site_domain,
                schema.Avazu.site_category,
                schema.Avazu.app_id,
                schema.Avazu.app_domain,
                schema.Avazu.app_category,
                schema.Avazu.device_id,
                schema.Avazu.device_ip,
                schema.Avazu.device_model,
                schema.Avazu.device_type,
                schema.Avazu.device_conn_type,
                schema.Avazu.C14,
                schema.Avazu.C15,
                schema.Avazu.C16,
                schema.Avazu.C17,
                schema.Avazu.C18,
                schema.Avazu.C19,
                schema.Avazu.C20,
                schema.Avazu.C21,
            ),
            'test.gz',
        ),  # Testset partition
        Partition(schema.Avazu.features, 'train.gz'),  # Trainset partition
    )
    CSV_PARAMS = {
        'compression': 'gzip',
        'parse_dates': ['hour'],
        'date_format': '%y%m%d%H',
    }

    @property
    def source(self) -> dsl.Source:
        return schema.Avazu
