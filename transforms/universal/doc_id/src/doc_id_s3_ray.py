# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import sys

from data_processing.runtime.ray import RayTransformLauncher
from data_processing.utils import ParamsUtils
from doc_id_transform import DocIDRayTransformConfiguration


# create launcher


launcher = RayTransformLauncher(DocIDRayTransformConfiguration())
# create parameters
s3_cred = {
    "access_key": "localminioaccesskey",
    "secret_key": "localminiosecretkey",
    "url": "http://localhost:9000",
}
s3_conf = {
    "input_folder": "test/doc_id/input",
    "output_folder": "test/doc_id/output",
}
worker_options = {"num_cpus": 0.8}
code_location = {"github": "github", "commit_hash": "12345", "path": "path"}
params = {
    # where to run
    "run_locally": True,
    # Data access. Only required parameters are specified
    "data_s3_cred": ParamsUtils.convert_to_ast(s3_cred),
    "data_s3_config": ParamsUtils.convert_to_ast(s3_conf),
    # orchestrator
    "runtime_worker_options": ParamsUtils.convert_to_ast(worker_options),
    "runtime_num_workers": 5,
    "runtime_pipeline_id": "pipeline_id",
    "runtime_job_id": "job_id",
    "runtime_creation_delay": 0,
    "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
    # doc id
    "doc_id_doc_column": "contents",
    "doc_id_hash_column": "hash_column",
    "doc_id_int_column": "int_id_column",
}
sys.argv = ParamsUtils.dict_to_req(d=params)

# launch
launcher.launch()
