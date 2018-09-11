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
import logging
from flask import Blueprint
from flask_restplus import Api, Swagger
from werkzeug import cached_property

logger = logging.getLogger(__name__)


class CustomSwagger(Swagger):
    """Override RESTplus Swagger class to add custom properties."""

    def as_dict(self):
        """Add custom properties to top-level Swagger specs."""
        specs = super().as_dict()
        specs['consumes'] = ['text/csv', 'application/json', 'text/plain']
        return specs


class CustomApi(Api):
    @cached_property
    def __schema__(self):
        """
        The Swagger specifications/schema for this API

        Override this to refer to our fixed Swagger class.

        :returns dict: the schema as a serializable dict
        """
        if not self._schema:
            try:
                self._schema = CustomSwagger(self).as_dict()
            except Exception as e:
                # Log the source exception for debugging purpose
                # and return an error message
                print(e.message)
                msg = 'Unable to render schema'
                logger.exception(msg)  # This will provide a full traceback
                return {'error': msg}
        return self._schema


blueprint = Blueprint('acumos', __name__, url_prefix='/v2')


custom_api = CustomApi(
    blueprint,
    version=2,
    title='RDS Predictor',
    default_label='RDS Predictor',
    validate=True,
    description='The RDS (R Data) Predictor provides a mechanism for scoring models in RDS format'
)
