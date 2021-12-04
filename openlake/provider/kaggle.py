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
import os
import typing

import kaggle
from forml import conf
from forml.io import dsl
from openschema import kaggle as schema

from openlake import fetcher, parser, provider


class File(fetcher.Mixin[typing.IO], metaclass=abc.ABCMeta):
    """Kaggle file provider."""

    COMPETITION: str = abc.abstractmethod
    FILE_NAME: str = abc.abstractmethod

    def fetch(
        self, columns: typing.Optional[typing.Iterable[dsl.Feature]], predicate: typing.Optional[dsl.Feature]
    ) -> typing.IO:
        kaggle.api.competition_download_file(self.COMPETITION, self.FILE_NAME, conf.tmpdir, force=True, quiet=True)
        return open(os.path.join(conf.tmpdir, self.FILE_NAME), encoding='utf8')


class Titanic(File, parser.CSV, provider.Origin):
    """Titanic trainset."""

    COMPETITION = 'titanic'
    FILE_NAME = 'train.csv'

    @property
    def source(self) -> dsl.Queryable:
        return schema.Titanic
