#!/bin/bash

# Check the SSH info for a pod on the remote GPU cluster
# Usage:
# checkpodssh.sh <pod_id>
runpodctl pod ssh info "$1"