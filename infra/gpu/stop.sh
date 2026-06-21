#!/bin/bash

# Stop a pod on the remote GPU cluster
# Usage:
# stop.sh <pod_id>
runpodctl pod stop "$1"