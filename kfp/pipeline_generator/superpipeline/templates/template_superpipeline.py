# NOTE: This file is auto generated by Pipeline Generator.

import os

import kfp.compiler as compiler
import kfp.components as comp
import kfp.dsl as dsl
from workflow_support.compile_utils import (
    DEFAULT_KFP_COMPONENT_SPEC_PATH,
    ONE_HOUR_SEC,
    ONE_WEEK_SEC,
    ComponentUtils,
)


# path to kfp component specifications files
component_spec_path = os.getenv("KFP_COMPONENT_SPEC_PATH", DEFAULT_KFP_COMPONENT_SPEC_PATH)
# For every sub workflow we need a separate components, that knows about this subworkflow.
{%- for component in sub_workflows_components %}
run_{{ component.name }}_op = comp.load_component_from_file(component_spec_path + "executeSubWorkflowComponent.yaml")
{%- endfor %}


{%- for component in sub_workflows_components %}
{{ component.name }}_image = "{{ component.image }}"
{%- endfor %}

# Pipeline to invoke execution on remote resource
@dsl.pipeline(
    name="{{ superpipeline_name }}",
    description="{{ superpipeline_description }}",
)
def super_pipeline(
    {%- for p1_parameter in p1_parameters %}
    p1_orch_{{ p1_parameter.name }}_name: str = "{{ p1_parameter.pipeline_name }}",
    {%- endfor %}
    p2_pipeline_runtime_pipeline_id: str = "pipeline_id",
    p2_pipeline_ray_head_options: str = '{"cpu": 1, "memory": 4, "image_pull_secret": ""}',
    p2_pipeline_ray_worker_options: str = '{"replicas": 2, "max_replicas": 2, "min_replicas": 2, "cpu": 2, "memory": 4, "image_pull_secret": ""}',
    p2_pipeline_server_url: str = "http://kuberay-apiserver-service.kuberay.svc.cluster.local:8888",
    p2_pipeline_additional_params: str = '{"wait_interval": 2, "wait_cluster_ready_tmout": 400, "wait_cluster_up_tmout": 300, "wait_job_ready_tmout": 400, "wait_print_tmout": 30, "http_retries": 5, "delete_cluster_delay_minutes": 0}',
    p2_pipeline_runtime_code_location: str = '{"github": "github", "commit_hash": "12345", "path": "path"}',
    {%- for p2_parameter in add_p2_parameters %}
    p2_pipeline_{{ p2_parameter.name }}: {{ p2_parameter.type }}{% if p2_parameter.value is defined %}{% if p2_parameter.type == "str" %} = "{{ p2_parameter.value }}"{% else %} = {{ p2_parameter.value }}{% endif %}{% endif %},
    {%- endfor %}

    {{ sub_workflows_parameters }}
):

    # get all arguments
    args = locals()
    orch_host = "http://ml-pipeline:8888"

    def _set_component(op: dsl.BaseOp, displaied_name: str, prev_op: dsl.BaseOp = None):
        # set the sub component UI name
        op.set_display_name(displaied_name)

        # Add pod labels
        op.add_pod_label("app", "ml-pipeline").add_pod_label("component", "data-science-pipelines")
        # No cashing
        op.execution_options.caching_strategy.max_cache_staleness = "P0D"
        # image pull policy
        op.set_image_pull_policy("Always")
        # Set the timeout for each task to one week (in seconds)
        op.set_timeout(ONE_WEEK_SEC)
        if prev_op is not None:
            op.after(prev_op)

{{ sub_workflows_operations }}


    # Configure the pipeline level to one week (in seconds)
    dsl.get_pipeline_conf().set_timeout(ONE_WEEK_SEC)


if __name__ == "__main__":
    # Compiling the pipeline
    compiler.Compiler().compile(super_pipeline, __file__.replace(".py", ".yaml"))
