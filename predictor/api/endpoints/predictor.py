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
from predictor.api.parser import sync_request_params
from predictor.api.parser import status_success_response_body, async_success_response_body
from predictor.api.parser import error_response_body, error_response_body_500, async_read_write_fields
from flask_restplus import Resource, abort
from predictor.api.business import perform_scoring


def placeholder():
    abort(501, 'Method not yet implemented')


@api.route('/syncPredictions')
class SyncScoringCollection(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request', error_response_body)
    @api.response(413, 'Request Entity Too Large')
    @api.response(500, 'Internal Server Error', error_response_body_500)
    @api.header('ACUMOS-DatasetKey', 'The key to the dataset that contains metadata \
    associated with the input dataset', required=False)
    @api.header('ACUMOS-ModelVersion', 'Version of the uploaded model.   \
    If not provided, the latest version of the model will be used.', required=False)
    @api.header('ACUMOS-ModelKey', 'Key of the model uploaded', required=True)
    @api.header('Content-Type', 'Set the appropriate content type based on input dataset that\
    is passed in the body.  For example, for csv set the content type text/csv', required=True)
    @api.expect(sync_request_params, validate=False, headers={"ACUMOS-TEST": "TEST"})
    def post(self):
        """
        Perform synchronous scoring/prediction with the specified \
        model against the dataset provided in-band in the payload.
        """
        return perform_scoring()


@api.route('/asyncPredictions')
class AsyncScoringCollection(Resource):
    @api.response(202, 'Accepted', async_success_response_body)
    @api.response(400, 'Bad Request', error_response_body)
    @api.response(413, 'Request Entity Too Large')
    @api.response(500, 'Internal Server Error', error_response_body_500)
    @api.header('ACUMOS-MessageId', 'VPass in a unique id to correlate the callback response.  \
    This id will be echoed back in the header of the callback/webhooks notification through \
    the callback url', required=False)
    @api.header('ACUMOS-CallbackURL', 'This is the callback url to which the service will send a\
     callback/webhooks notification when the scoring has been completed', required=False)
    @api.header('ACUMOS-ModelVersion', 'Version of the uploaded model.   \
    If not provided, the latest version of the model will be used.', required=False)
    @api.header('ACUMOS-ModelKey', 'Key of the model uploaded', required=True)
    @api.header('Content-Type', 'The content type should be application/json', required=True)
    @api.expect(async_read_write_fields, validate=True)
    def post(self):
        """
        Perform asynchronous prediction against the specified model and the specified read dataset key in the payload \
        and write back the prediction in the specified write back dataset key
        """
        placeholder()


@api.route('/statuses/<string:statusKey>')
class StatusScoringCollection(Resource):
    @api.response(200, 'Ok', status_success_response_body)
    @api.response(400, 'Bad Request', error_response_body)
    @api.response(413, 'Request Entity Too Large')
    @api.response(500, 'Internal Server Error', error_response_body_500)
    @api.header('ACUMOS-MessageId', 'This is ACUMOS-MessageId passed by the \
    client in the async request header', required=True)
    def get(self, statusKey):
        """
        Get the status of the predictions
        """
        placeholder()
