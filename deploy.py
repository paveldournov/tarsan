import kfp

with open('curr_time.txt', 'r') as file:
    curr_timestamp = file.read().replace('\n', '')

client = kfp.Client(host='http://localhost:8080')

file_name = 'train_targe_image_reco_pipeline.yaml'
tarsan_pipelineid='6304e111-9c28-4436-8be6-007318be64e2'
version_id = file_name+'-'+curr_timestamp
new_job_name='tarsan'+'-'+curr_timestamp

#client._upload_api.upload_pipeline_version(file_name, name=version_id, pipelineid=tarsan_pipelineid)

client.run_pipeline(experiment_id='0b3e85c6-62aa-4781-bfd5-ef7f05ca3114', job_name=version_id, pipeline_id=tarsan_pipelineid, version_id=version_id)
