SET images_tag=0.12-test24

pushd generate_data
call build.cmd
popd

pushd train_model
call build.cmd
popd

python pipeline.py
