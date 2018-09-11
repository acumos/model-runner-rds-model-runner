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
from flask_restplus import reqparse, fields
from predictor.api.namespaces import predictor_namespace as api

sync_request_params = reqparse.RequestParser()

sync_request_params.add_argument('rawCSV',
                                 type=str,
                                 location='form',
                                 required=True,
                                 help='Raw CSV to score model against')

sync_request_params.add_argument('Content-Type',
                                 type=str,
                                 location='headers',
                                 required=True,
                                 help='Set the appropriate content type based on input dataset that\
                                 is passed in the body.  For example, for csv set the content type text/csv')

sync_request_params.add_argument('ATT-ModelKey',
                                 type=str,
                                 location='headers',
                                 required=True,
                                 help='Key of the model uploaded')

sync_request_params.add_argument('ATT-ModelVersion',
                                 type=str,
                                 location='headers',
                                 required=False,
                                 help='Version of the uploaded model.   If not provided, the latest\
                                 version of the model will be used.')

sync_request_params.add_argument('ATT-DatasetKey',
                                 type=str,
                                 location='headers',
                                 required=False,
                                 help='The key to the dataset that contains metadata associated with the input dataset')

async_request_params = reqparse.RequestParser()

async_request_params.add_argument('Content-Type',
                                  type=str,
                                  location='headers',
                                  required=True,
                                  help='Set the appropriate content type based on input dataset that is passed in the\
                                  body.  For example, for csv set the content type text/csv')

async_request_params.add_argument('ATT-ModelKey',
                                  type=str,
                                  location='headers',
                                  required=True,
                                  help='Key of the model uploaded')

async_request_params.add_argument('ATT-ModelVersion',
                                  type=str,
                                  location='headers',
                                  required=False,
                                  help='Version of the uploaded model.   If not provided, the latest version of \
                                  the model will be used.')

async_request_params.add_argument('ATT-MessageId',
                                  type=str,
                                  location='headers',
                                  required=False,
                                  help='Pass in a unique id to correlate the callback response.  This id will be echoed\
                                   back in the header of the callback/webhooks notification through the callback url')

async_request_params.add_argument('ATT-CallbackURL',
                                  type=str,
                                  location='headers',
                                  required=False,
                                  help='This is the callback url to which the service will send a callback/webhooks \
                                  notification when the scoring has been completed')

async_request_params.add_argument('readDatasetKey',
                                  type=str,
                                  location='json',
                                  required=True,
                                  help='Dataset key from which the input dataset will be pulled for scoring')

async_request_params.add_argument('writeDatasetKey',
                                  type=str,
                                  location='json',
                                  required=True,
                                  help='Dataset key to which the predictions results will be written back')


async_success_response_body = api.model('Async Prediction Response', {
    'statusUrl': fields.String(description='The is the url for polling the status of the async prediction request.',
                               required=True,
                               example="https://<FQDN>/v2/statuses/232423423"),
    'statusKey': fields.String(description='The is the unique identifier for the status of the requested job.',
                               required=True,
                               example="232423423"),
})


status_success_response_body = api.model('Status Response', {
    'status': fields.String(description='This is the status of the async prediction request.',
                            required=True,
                            example="Success-Job Completed"),
    'messageId': fields.String(description='This is ATT-MessageId passed by the client in the async request header',
                               required=False,
                               example="156144651"),
})


error_response_body = api.model('Error Response - General', {
    'errorId': fields.String(description='Identifier for the error.',
                             required=True,
                             example="RDS-0003"),
    'message': fields.String(description='Brief description about the error.',
                             required=True,
                             example="Invalid Value for parameter(s), %1, %2"),
    'variable': fields.List(fields.String, description='Values for the parameters in the error message field.',
                            required=False,
                            example="['modelKey', 'modelVersion']"),
    'errorUrl': fields.String(description='Url to a web page where there is detailed information \
    about the cause and resolution for the given error.',
                              required=False,
                              example="https://acumos.org/error/rds-0001"),
})


error_response_body_500 = api.model('Error Response - 500', {
    'errorId': fields.String(description='Identifier for the error.',
                             required=True,
                             example="RDS-0001"),
    'message': fields.String(description='Brief description about the error.',
                             required=True,
                             example="Please provide the reference id ( %1 ) to the support team"),
    'variable': fields.List(fields.String,
                            description='The unique error reference id to be provided to the support team.',
                            required=False,
                            example="['24234234234234']"),
    'errorUrl': fields.String(description='Url to a web page where there is detailed information \
    about the cause and resolution for the given error.',
                              required=False,
                              example="https://acumos.org/error/rds-0001"),
})
