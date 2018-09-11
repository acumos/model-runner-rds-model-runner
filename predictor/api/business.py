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
from acumoscommon.config_util import get_config_value, get_model_cache_dir, verify_ssl,\
    get_properties_path
from acumoscommon.responses import bad_request, request_entity_too_large, error_response
from flask import request, Response

from predictor.rds.wrapper import RDSWrapper, RDSException
from acumoscommon.services.model_manager_service import ModelManagerException, CachedModelManagerService
import logging
import os

logger = logging.getLogger(__name__)


def perform_scoring():
    max_content_size = int(get_config_value('max_content_size', section='APP_SETTINGS'))
    content_length = request.content_length
    if content_length is not None and content_length > max_content_size:
        request_entity_too_large()

    section = 'SERVICES'
    model_manager_endpoint = get_config_value('modelmanager_service', section=section)

    model_key = request.headers.get("ACUMOS-ModelKey")
    model_version = request.headers.get("ACUMOS-ModelVersion")

    model_manager_service = CachedModelManagerService(model_manager_endpoint,
                                                      get_model_cache_dir(), binary=True, verify_ssl=verify_ssl())
    if request.data is None or request.is_json:
        bad_request("No input csv found on the request")
    else:
        dataset_contents = request.data.decode()

    try:
        model = model_manager_service.download_model(model_key, model_version)
    except ModelManagerException as ex:
        error_response(ex.status_code, ex.body)

    try:
        wrapper_program = os.path.join(os.path.join(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'properties'), 'predictor.R')

        rds_wrapper = RDSWrapper()
        results = rds_wrapper.run_prediction(wrapper_program, model, dataset_contents)
        return Response(results, mimetype='text/csv')
    except RDSException as ex:
        bad_request(str(ex))
