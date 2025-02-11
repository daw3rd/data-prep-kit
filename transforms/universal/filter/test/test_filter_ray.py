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

import os

from data_processing.runtime.ray import RayTransformLauncher
from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from filter_transform import (
    FilterRayTransformConfiguration,
    filter_columns_to_drop_cli_param,
    filter_criteria_cli_param,
    filter_logical_operator_cli_param,
    filter_logical_operator_default,
)


class TestRayFilterTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        fixtures = []
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data"))

        fixtures.append(
            (
                RayTransformLauncher(FilterRayTransformConfiguration()),
                {
                    filter_criteria_cli_param: [
                        "docq_total_words > 100 AND docq_total_words < 200",
                        "ibmkenlm_docq_perplex_score < 230",
                    ],
                    filter_logical_operator_cli_param: filter_logical_operator_default,
                    filter_columns_to_drop_cli_param: ["extra", "cluster"],
                },
                os.path.join(basedir, "input"),
                os.path.join(basedir, "expected", "test-and"),
            )
        )

        fixtures.append(
            (
                RayTransformLauncher(FilterRayTransformConfiguration()),
                {
                    filter_criteria_cli_param: [
                        "docq_total_words > 100 AND docq_total_words < 200",
                        "ibmkenlm_docq_perplex_score < 230",
                    ],
                    filter_logical_operator_cli_param: "OR",
                    filter_columns_to_drop_cli_param: ["extra", "cluster"],
                },
                os.path.join(basedir, "input"),
                os.path.join(basedir, "expected", "test-or"),
            )
        )

        fixtures.append(
            (
                RayTransformLauncher(FilterRayTransformConfiguration()),
                {
                    filter_criteria_cli_param: [],
                    filter_logical_operator_cli_param: filter_logical_operator_default,
                    filter_columns_to_drop_cli_param: [],
                },
                os.path.join(basedir, "input"),
                os.path.join(basedir, "expected", "test-default"),
            )
        )

        fixtures.append(
            (
                RayTransformLauncher(FilterRayTransformConfiguration()),
                {
                    filter_criteria_cli_param: [
                        "date_acquired BETWEEN '2023-07-04' AND '2023-07-08'",
                        "title LIKE 'https://%'",
                    ],
                    filter_logical_operator_cli_param: filter_logical_operator_default,
                    filter_columns_to_drop_cli_param: [],
                },
                os.path.join(basedir, "input"),
                os.path.join(basedir, "expected", "test-datetime-like"),
            )
        )

        fixtures.append(
            (
                RayTransformLauncher(FilterRayTransformConfiguration()),
                {
                    filter_criteria_cli_param: [
                        "document IN ('CC-MAIN-20190221132217-20190221154217-00305.warc.gz', 'CC-MAIN-20200528232803-20200529022803-00154.warc.gz', 'CC-MAIN-20190617103006-20190617125006-00025.warc.gz')",
                    ],
                    filter_logical_operator_cli_param: filter_logical_operator_default,
                    filter_columns_to_drop_cli_param: [],
                },
                os.path.join(basedir, "input"),
                os.path.join(basedir, "expected", "test-in"),
            )
        )

        return fixtures
