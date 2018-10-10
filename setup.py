#!/usr/bin/env python3
# ===============LICENSE_START=======================================================
# Acumos Apache-2.0
# ===================================================================================
# Copyright (C) 2018 AT&T Intellectual Property. All rights reserved.
# ===================================================================================
# This Acumos software file is distributed by AT&T
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================
from os.path import dirname, abspath, join as path_join
from setuptools import setup, find_packages


SETUP_DIR = abspath(dirname(__file__))

with open(path_join(SETUP_DIR, 'predictor', '_version.py')) as file:
    globals_dict = dict()
    exec(file.read(), globals_dict)
    __version__ = globals_dict['__version__']

with open("README.md") as fd:
    long_description = fd.read()

setup(
    author='Pavel Kazakov, Karthic Raghavan, Ryan Hull',
    author_email='pk9069@att.com, kr577p@att.com, rh183@att.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
    ],
    description='RDS model runner is for scoring/predictions for portable RDS model formats',
    install_requires=['Flask>=1.0.2',
                      'flask-restplus>=0.10.1',
                      'gunicorn>=19.9.0',
                      'flask-cors>=3.0.3',
                      'requests==2.18.4'],
    keywords='acumos machine learning model rds runner predictor server ml ai',
    license='Apache License 2.0',
    long_description=long_description,
    name='rds-model-runner',
    packages=find_packages(),
    python_requires='>=3.5',
    url='https://gerrit.acumos.org/r/gitweb?p=model-runner%2Frds-model-runner.git',
    version=__version__,
)
