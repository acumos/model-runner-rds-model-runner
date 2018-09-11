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
import json
import os
from unittest.mock import patch
from predictor.rds.wrapper import RDSWrapper
from flask import Flask
os.environ['model_cache_dir'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'model_cache_dir_test')
from microservice_flask import initialize_app

app = Flask(__name__)

initialize_app(app)


# This is a mocked function that writes the results of scoring to a file
def mock_popen_write_result(command, working_dir):

    with open(os.path.join(working_dir, RDSWrapper.OUTPUT_FILE_NAME), "w") as file:
        file.write("""\"x\"
                    29.5853765907586
                    9.88258499966691
                    """)
    return "test"


@patch.object(RDSWrapper, '_run_command', side_effect=mock_popen_write_result)
def test_get_syncPredictions(run_prediction):

    body = '''
        qsec, wt, am
        22.2,  2.6, 1
        10.12, 3.1, 0
        '''

    request_headers = {
        'content-type': 'text/csv',
        'accept': 'text/csv',
        'ACUMOS-ModelVersion': '1_0',
        'ACUMOS-ModelKey': 'rdsmodel'
    }

    with app.test_client() as c:
        response = c.post('/v2/syncPredictions', data=body, headers=request_headers)
    assert response.status_code == 200
    assert len(response.get_data()) > 5


def test_get_status():
    with app.test_client() as c:
        response = c.get('/v2/statuses/' + 'dummyStatusKey')
    assert response.status_code == 501
    assert json.loads(response.get_data())['message'] == 'Method not yet implemented'


def test_get_asyncPredictions():

    body = {
        'readDatasetKey': 'm092XX_1530026027076_855258959068650452',
        'writeDatasetKey': 'm092XX_1530026122667_683407214566211287'
    }

    request_headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'ACUMOS-ModelVersion': '1_0',
        'ACUMOS-ModelKey': 'rds',
        'ACUMOS-MessageId': 'rh1832_callback_id1',
        'ACUMOS-ReturnURL': 'http://localhost:8123/v2/callback'
    }

    with app.test_client() as c:
        response = c.post('/v2/asyncPredictions', data=json.dumps(body), headers=request_headers)
    assert response.status_code == 501
    assert json.loads(response.get_data())['message'] == 'Method not yet implemented'
