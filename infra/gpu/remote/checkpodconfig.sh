#!/bin/bash

# Check GPU configuration
echo "Checking GPU configuration..."
gpu_info=$(nvidia-smi)
echo "$gpu_info"

# Check CUDA tools installation
echo "Checking CUDA tools installation..."
cuda_version=$(nvcc --version)
echo "CUDA version: $cuda_version"

# Check cuDNN installation
echo "Checking cuDNN installation..."
cudnn_version=$(dpkg -l | grep cudnn)
echo "cuDNN version: $cudnn_version"
