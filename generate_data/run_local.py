import kfp
import kfp.components as comp
from kfp.components._components import _resolve_command_line_and_paths

my_op = kfp.components.load_component_from_file('tarsan_gen_images.yaml') 

print("**** LOADED COMPONENT:")
print(my_op.component_spec)

sample_count = 20

cmd_args = {
   "samples_count": sample_count,
}

cmd = _resolve_command_line_and_paths(
         component_spec = my_op.component_spec,
         arguments = cmd_args,
      )

print("\nIMAGE:\n")
print(my_op.component_spec.implementation.container.image)

print("\nCOMMAND\n")
print(cmd.command)

print("\nARGS\n")
print(cmd.args)

import docker
docker_client = docker.from_env()

print("\nCOMMAND:")
args = cmd.command[0:] + cmd.args
print(args)

container_res = docker_client.containers.run(
         image = my_op.component_spec.implementation.container.image,
         #entrypoint = cmd.command,
         command = args,
      )

print("RUN OUTPUT")
print(container_res.decode("utf-8"))
