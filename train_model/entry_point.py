import argparse
import os
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('--imagesPath', type=str, help='path to images')
parser.add_argument('--tblogs', type=str, help='GCS path to tensorboard logs')
parser.add_argument('--epochs', type=int, help='Number of epochs')
parser.add_argument('--batchsize', type=int, help='Batch size')
parser.add_argument('--modelPath', type=str, help='Path to output model')

args = parser.parse_args()

print("Creating output dir")
output_dir_path = args.modelPath
os.makedirs(output_dir_path, exist_ok=True)

from train_score_model import train_target_score_model
train_target_score_model(args.imagesPath, args.modelPath, args.tblogs, args.epochs, args.batchsize )

