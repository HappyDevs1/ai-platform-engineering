#!/bin/bash

# SSH into a pod on the remote GPU cluster
ssh root@"$1" -p "$2" -i ~/.ssh/id_ed25519
# Usage:
# sshintopod.sh <pod_ip> <pod_port>
