python gen_image_timestamp.py > curr_time.txt

SET /p images_tag=<curr_time.txt

pushd generate_data
call build.cmd
popd

pushd train_model
call build.cmd
popd

pushd deploy_model
call build.cmd
popd

python pipeline.py
