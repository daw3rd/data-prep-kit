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

from data_processing.runtime import TransformRuntimeConfiguration
from data_processing.runtime.ray import DefaultTableTransformRuntimeRay
from data_processing.transform import TransformConfiguration


class RayTransformRuntimeConfiguration(TransformRuntimeConfiguration):
    def __init__(
        self,
        transform_config: TransformConfiguration,
        runtime_class: type[DefaultTableTransformRuntimeRay] = DefaultTableTransformRuntimeRay,
    ):
        """
        Initialization
        :param transform_config - base configuration class
        :param runtime_class: implementation of the transform runtime
        :param remove_from_metadata - list of parameters to remove from metadata
        """
        super().__init__(transform_config=transform_config)
        self.runtime_class = runtime_class

    def create_transform_runtime(self) -> DefaultTableTransformRuntimeRay:
        """
        Create transform runtime with the parameters captured during apply_input_params()
        :return: transform runtime object
        """
        return self.runtime_class(self.transform_config.get_transform_params())
