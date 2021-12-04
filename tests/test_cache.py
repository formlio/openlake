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
Caching unit tests.
"""
import pathlib
from unittest import mock

import pandas

from openlake import cache


def test_dataframe(tmp_path: pathlib.Path, frame: pandas.DataFrame):
    """Test the dataframe caching."""
    loader = mock.MagicMock()
    loader.return_value = frame
    assert cache.dataframe('foobar', loader, tmp_path).equals(frame)
    loader.assert_called()
    loader.reset_mock()
    assert cache.dataframe('foobar', loader, tmp_path).equals(frame)
    loader.assert_not_called()
