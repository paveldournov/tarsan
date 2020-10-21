import argparse
import os
from os import path

def deploy_model(modelPath):
    print("Getting the model from {}".format(modelPath))
    
    print("Model files")
    for fn in os.listdir(modelPath):
        print(fn)

    return "http://modelishre.com"


parser = argparse.ArgumentParser()
parser.add_argument('--modelPath', type=str, help='path to the model', required=True)
parser.add_argument('--endpointOutFile', type=str, help='path to output file with the endpoint URL in it', required=True)

args = parser.parse_args()

print("Creating output dir")
output_dir_path = args.endpointOutFile
os.makedirs(os.path.dirname(output_dir_path), exist_ok=True)

model_url = deploy_model(args.modelPath)

with open(args.endpointOutFile, "w") as f:
    f.write(model_url)

