python gen_image_timestamp.py > curr_time.txt

SET /p images_tag=<curr_time.txt

REM SET images_tag=0.12-test44

REM pushd generate_data
REM call build.cmd
REM popd

REM pushd train_model
REM call build.cmd
REM popd

pushd deploy_model
call build.cmd
popd

python pipeline.py
