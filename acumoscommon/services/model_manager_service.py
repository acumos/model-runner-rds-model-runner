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
from logging import getLogger
from tempfile import NamedTemporaryFile

import requests
import os


logger = getLogger(__name__)

API_VERSION = 'v2'
MODELS_RESOURCE = 'models'
CONTENTS_RESOURCE = 'contents'


class ModelManagerException(Exception):
    def __init__(self, body, status_code, message=None):
        self.body = body
        self.status_code = status_code

        if message is None:
            message = 'ModelManagerException: Status code: {}. Response Body: {}'.format(
                status_code, body)
        super(ModelManagerException, self).__init__(message)


class ModelManagerService:

    def __init__(self, endpoint, binary=False, verify_ssl=True):
        self._endpoint = endpoint
        self.headers = {}
        self.binary = binary
        self.verify_ssl = verify_ssl


    def download_model(self, model_key, version_id=None):
        endpoint = self._endpoint + '/' + API_VERSION + '/' + MODELS_RESOURCE + '/' + \
            model_key + '/' + CONTENTS_RESOURCE

        logger.debug('Sending request endpoint {}'.format(endpoint))
        if version_id is not None:
            params = {
                'versionId': version_id
            }
            response = requests.get(endpoint, params=params, headers=self.headers,
                                    verify=self.verify_ssl)
        else:
            response = requests.get(endpoint, headers=self.headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise ModelManagerException(response.text, response.status_code)

        if self.binary:
            return response.content
        else:
            return response.text


class CachedModelManagerService(ModelManagerService):

    def __init__(self, endpoint, model_cache_dir,  binary=False, verify_ssl=True):
        ModelManagerService.__init__(self, endpoint, binary=binary,
                                     verify_ssl=verify_ssl)
        self.model_cache_dir = model_cache_dir

    def download_model(self, model_key, version_id):
        model = self._get_cached_model(model_key, version_id)
        if model:
            return model
        model = ModelManagerService.download_model(self, model_key, version_id)
        self._save_cached_model(model_key, version_id, model)
        return model

    def _get_cached_model(self, model_key, version_id):
        model_file_path = os.path.join(self.model_cache_dir, version_id, model_key)
        logger.debug("Checking path %s for cached model", model_file_path)
        if not os.path.exists(model_file_path):
            return None
        read_flag = 'rb' if self.binary else 'r'
        with open(model_file_path, read_flag) as model_file:
            return model_file.read()

    def _save_cached_model(self, model_key, version_id, model):
        """
        Saves the model to the model cache directory

        Some implementation notes: To avoid corrupt files in cases where two processes are writing to the same file, the
        model is first saved as a temporary file and then moved to the final destination as POSIX guarantees a rename to
        be atomic.
        """

        model_file_dir = os.path.join(self.model_cache_dir, version_id)
        try:
            os.makedirs(model_file_dir)
        except OSError:
            if not os.path.isdir(model_file_dir):
                raise ModelManagerException('Error creating model cache directory {}'.format(model_file_dir))
        tmp_file = NamedTemporaryFile(dir=self.model_cache_dir, delete=False)
        write_flag = 'wb' if self.binary else 'w'
        with open(tmp_file.name, write_flag) as f:
            f.write(model)
        os.rename(tmp_file.name, os.path.join(model_file_dir, model_key))
