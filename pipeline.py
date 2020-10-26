import kfp
from kfp.components import load_component_from_file
import kfp.gcp as gcp

gen_images_op = load_component_from_file("generate_data\component.yaml")
train_model_op = load_component_from_file("train_model\component.yaml")
deploy_model_op = load_component_from_file("deploy_model\component.yaml")

def train_target_image_reco_pipeline(
    train_count: int = 100, 
    test_count: int = 10,
    epochs: int = 30,
    batch_size: int = 30,
    dest_gcs_bucket: 'GCSBucket' = 'dpa23',
    tb_logs: 'GCSPath' = 'gs://dpa23/tarsantblogs'
):
    gen_images_task = gen_images_op(train_count, test_count)
    
    train_model_task = train_model_op(
        gen_images_task.outputs["TrainingDataLocation".lower()],
        tb_logs,
        epochs,
        batch_size
    ).apply(gcp.use_gcp_secret('user-gcp-sa'))
    
    deploy_model_task = deploy_model_op(
        train_model_task.outputs["Model".lower()],
        dest_gcs_bucket
    ).apply(gcp.use_gcp_secret('user-gcp-sa'))

kfp.compiler.compiler.Compiler().compile(
    pipeline_func=train_target_image_reco_pipeline,
    package_path="train_targe_image_reco_pipeline.yaml",
)
