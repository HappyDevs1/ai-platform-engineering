#!/bin/bash

# Create a pod on the remote GPU cluster
# Usage:
# create.sh <template_id> <gpu_id>
runpodctl pod create --template-id "$1" --gpu-id "$2"