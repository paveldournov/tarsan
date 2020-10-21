import argparse
import os
from os import path
import json
#import kfp
#import kfp.components as comp
#from kfp.components._components import _resolve_command_line_and_paths

def gen_target_images_entry_point(samples_count, samples_path, test_count, test_path):
    from gen_targets import generate_dataset
    generate_dataset(samples_count, samples_path)
    generate_dataset(test_count, test_path)


parser = argparse.ArgumentParser()
parser.add_argument('--train_samples', type=int, help='number of samples for training')
parser.add_argument('--test_samples',  type=int, help='number of samples for testing')
parser.add_argument('--train_path', type=str, help='output path for training samples')
parser.add_argument('--test_path', type=str, help='output path for testing samples')

args = parser.parse_args()

print(args)

print("Creating output dirs")

os.makedirs(args.train_path, exist_ok=True)
os.makedirs(args.test_path, exist_ok=True)

gen_target_images_entry_point(args.train_samples, args.train_path, args.test_samples, args.test_path)

viz_metadata = {
    'outputs' : [
    # Markdown that is hardcoded inline
    {
      'storage': 'inline',
      'source': '# Inline Markdown\n[A link](https://www.kubeflow.org/)',
      'type': 'markdown',
    }]
  }

with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(viz_metadata, f)

