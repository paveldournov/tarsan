import argparse
import os
from os import path
import glob
from google.cloud import storage


def copy_local_directory_to_gcs(local_path, bucket, gcs_path):
    for local_file in glob.glob(local_path + '/**'):
        if not os.path.isfile(local_file):
            continue
        remote_path = os.path.join(gcs_path, local_file[1 + len(local_path) :])
        blob = bucket.blob(remote_path)
        blob.upload_from_filename(local_file)

def deploy_model(modelPath, remoteGCSBucket):
    print("Getting the model from {}".format(modelPath))
    remote_path = 'tarsanmodel2'
    storage_client = storage.Client()
    bucket = storage_client.bucket(remoteGCSBucket)
    
    copy_local_directory_to_gcs(modelPath, bucket, remote_path)

    """
    print("Model files")
    for fn in os.listdir(modelPath):
        full_fn = os.path.join(modelPath, fn)
        print("Copying {}".format(full_fn))
        blob = bucket.blob(os.path.join(remote_path, fn))
        blob.upload_from_filename(full_fn)
    """

    return "gs://{}/{}".format(remoteGCSBucket, remote_path)


parser = argparse.ArgumentParser()
parser.add_argument('--modelPath', type=str, help='path to the model', required=True)
parser.add_argument('--DestGCSBucket', type=str, help='gcs bucket to copy the model to', required=True)
parser.add_argument('--endpointOutFile', type=str, help='path to output file with the endpoint URL in it', required=True)
parser.add_argument('--DestGCSPath', type=str, help='path to output file with the full gcs path of the model', required=True)

args = parser.parse_args()

print("Creating output dirs to return output variables")
os.makedirs(os.path.dirname(args.endpointOutFile), exist_ok=True)
os.makedirs(os.path.dirname(args.DestGCSPath), exist_ok=True)

model_url = deploy_model(args.modelPath, args.DestGCSBucket)

with open(args.endpointOutFile, "w") as f:
    f.write(model_url)

with open(args.DestGCSPath, "w") as f:
    f.write(model_url)
