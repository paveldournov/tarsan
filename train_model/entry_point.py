import argparse
import os
from os import path



def train_model(imagesPath, modelPath):
    print("training model from data in {}".format(imagesPath))
    
    print("Images to train on:")
    for fn in os.listdir(imagesPath):
        print(fn)

    from train_score_model import train_target_score_model
    train_target_score_model(imagesPath, modelPath)


parser = argparse.ArgumentParser()
parser.add_argument('--imagesPath', type=str, help='path to images')
parser.add_argument('--modelPath', type=str, help='path to output model')

args = parser.parse_args()

print("ImagesPath={}".format(args.imagesPath))
print("modelPath={}".format(args.modelPath))

print("Creating output dir")
#output_dir_path = os.path.dirname(args.path)
output_dir_path = args.modelPath
os.makedirs(output_dir_path, exist_ok=True)

train_model(args.imagesPath, args.modelPath)

#process_op = comp.func_to_container_op(gen_target_images_entry_point, base_image="gcr.io/test-vms/tarsan-genimages:latest")
#process_op.component_spec.save("tarsan_gen_images.yaml")

