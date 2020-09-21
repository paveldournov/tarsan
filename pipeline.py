import kfp
from kfp.components import load_component_from_file

gen_images_op = load_component_from_file("generate_data\component.yaml")
train_model_op = load_component_from_file("train_model\component.yaml")

def train_target_image_reco_pipeline(
    train_count: int = 100, 
    test_count: int = 10
):
    gen_images_task = gen_images_op(train_count, test_count)
    train_model_task = train_model_op(gen_images_task.outputs["TrainingDataLocation".lower()])


kfp.compiler.compiler.Compiler().compile(
    pipeline_func=train_target_image_reco_pipeline,
    package_path="train_targe_image_reco_pipeline.yaml",
)
