import argparse
import os
from os import path
#import kfp
#import kfp.components as comp
#from kfp.components._components import _resolve_command_line_and_paths

def gen_target_images_entry_point(samples_count, samples_path):
    from gen_targets import generate_dataset
    generate_dataset(samples_count, samples_path)


parser = argparse.ArgumentParser()
parser.add_argument('--samples', metavar='num_samples', type=int, help='number of samples')
parser.add_argument('--path', metavar="samples_path", type=str, help='output path')

args = parser.parse_args()

print("Samples={}".format(args.samples))
print("Path={}".format(args.path))

print("Creating output dir")
#output_dir_path = os.path.dirname(args.path)
output_dir_path = args.path
os.makedirs(output_dir_path, exist_ok=True)

#ff2 = open(args.path, "w")
#ff2.write("gs://dpa23/imagedata")
#ff2.close()

#print("Output exists:{}".format(path.exists(args.path)))
#print("Output is a file:{}".format(path.isfile(args.path)))

gen_target_images_entry_point(args.samples, output_dir_path)

#process_op = comp.func_to_container_op(gen_target_images_entry_point, base_image="gcr.io/test-vms/tarsan-genimages:latest")
#process_op.component_spec.save("tarsan_gen_images.yaml")

