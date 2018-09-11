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
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)


class RDSException(Exception):
    pass


class RDSWrapper():
    MODEL_FILE_NAME = 'RDS.rds'
    INPUT_FILE_NAME = 'input.csv'
    OUTPUT_FILE_NAME = 'output.csv'
    BASE_COMMAND = 'Rscript'

    def _run_command(self, command, working_dir):
        cwd = working_dir
        logger.debug('cwd: %s', cwd)
        logger.debug('command: %s', command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        stdout, stderr = process.communicate()
        stdout = stdout.decode()
        logger.debug(f'stdout: {stdout}')
        if process.returncode != 0:
            raise RDSException(stderr.decode())
        return stdout

    def run_prediction(self, wrapper_program_path, model_contents, dataset_contents):
        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, RDSWrapper.MODEL_FILE_NAME)
            with open(model_path, 'wb') as model_file:
                model_file.write(model_contents)

            input_path = os.path.join(tmpdir, RDSWrapper.INPUT_FILE_NAME)
            with open(input_path, 'w') as dataset_file:
                dataset_file.write(dataset_contents)

            output_path = os.path.join(tmpdir, RDSWrapper.OUTPUT_FILE_NAME)

            command = [RDSWrapper.BASE_COMMAND, wrapper_program_path, model_path, input_path, output_path]
            self._run_command(command, tmpdir)

            with open(output_path) as results:
                return results.read()
