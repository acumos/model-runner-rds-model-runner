#
# ===============LICENSE_START=======================================================
# Acumos
# ===================================================================================
# Copyright (C) 2018 AT&T Intellectual Property. All rights reserved.
# ===================================================================================
# This Acumos software file is distributed by AT&T
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================
from setuptools import setup


setup(
    author='Pavel Kazakov, Karthic Raghavan, Ryan Hull',
    author_email='pk9069@att.com, kr577p@att.com, rh183@att.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
    ],
    description=""""RDS Predictor provides the capability to run predictions on RDS / R
    models and runs predictions either synchronously or asynchronously.""",
    install_requires=['Flask>=1.0.2',
                      'flask-restplus>=0.11.0',
                      'gunicorn>=19.9.0',
                      'flask-cors>=3.0.6'],
    keywords='acumos machine learning model runner server predictor rds r ml ai',
    license='Apache License 2.0',
    name='rds-model-runner',
    python_requires='>=3.4',
    url='git clone https://gerrit.acumos.org/r/model-runner/rds-model-runner.git',
    version=1.0,
    )
