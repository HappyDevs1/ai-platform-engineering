#!/bin/bash

# Start a pod on the remote GPU cluster
# Usage:
# start.sh <pod_id>
runpodctl pod start "$1"