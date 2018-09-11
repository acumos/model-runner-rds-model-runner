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
from predictor.api.namespaces import predictor_namespace as api
from predictor.api.parser import sync_request_params, async_request_params
from predictor.api.parser import status_success_response_body, async_success_response_body
from predictor.api.parser import error_response_body, error_response_body_500
from flask_restplus import Resource, abort


def placeholder():
    abort(501, 'Method not yet implemented')


@api.route('/syncPredictions')
class SyncScoringCollection(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request', error_response_body)
    @api.response(413, 'Request Entity Too Large')
    @api.response(500, 'Internal Server Error', error_response_body_500)
    @api.header('Content-Type', 'The content type of the response body', required=True)
    @api.expect(sync_request_params, validate=False)
    def post(self):
        """
        Score the specified model against the specified dataset payload to get a prediction
        """
        placeholder()


@api.route('/asyncPredictions')
class AsyncScoringCollection(Resource):
    @api.response(202, 'Accepted', async_success_response_body)
    @api.response(400, 'Bad Request', error_response_body)
    @api.response(413, 'Request Entity Too Large')
    @api.response(500, 'Internal Server Error', error_response_body_500)
    @api.header('ATT-MessageId', 'This is the correlation id to associate the callback response to.', required=False)
    @api.header('Content-Type', 'application/json', required=True)
    @api.expect(async_request_params, validate=True)
    def post(self):
        """
        Perform asynchronous prediction

        Asynchronously score the specified model against the specified read dataset key and write back to the specified
        write dataset key
        """
        placeholder()


@api.route('/statuses/<string:statusKey>')
class StatusScoringCollection(Resource):
    @api.response(200, 'Ok', status_success_response_body)
    @api.response(400, 'Bad Request', error_response_body)
    @api.response(413, 'Request Entity Too Large')
    @api.response(500, 'Internal Server Error', error_response_body_500)
    def get(self, statusKey):
        """
        Get the status of the predictions
        """
        placeholder()
