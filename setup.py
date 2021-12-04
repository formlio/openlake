# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# 'License'); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Setuptools script for Opendata package.
"""

import setuptools

setuptools.setup(
    name='opendata',
    description='Public dataset feed',
    long_description=open('README.md', encoding='utf8').read(),  # pylint: disable=consider-using-with
    long_description_content_type='text/markdown',
    url='https://github.com/formlio/opendata',
    maintainer='ForML Development Team',
    maintainer_email='forml-dev@googlegroups.com',
    license='Apache License 2.0',
    packages=setuptools.find_packages(include=['opendata*']),
    setup_requires=['setuptools', 'wheel', 'pytest-runner'],
    tests_require=['pytest-runner', 'pytest-pylint', 'pytest-flake8'],
    install_requires=['forml>=0.3.*', 'openschema', 'pandas', 'pyarrow'],
    extras_require={
        'doc': {'sphinx', 'sphinxcontrib-napoleon', 'sphinx_rtd_theme', 'sphinx-autoapi'},
        'kaggle': {'kaggle'},
        'sklearn': {'scikit-learn'},
    },
    python_requires='>=3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: System :: Distributed Computing',
    ],
    zip_safe=False,
)
