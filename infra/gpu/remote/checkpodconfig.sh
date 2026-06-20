#!/bin/bash

# Check GPU configuration
nvidia-smi

# Check CUDA tools installation
nvcc --version

# Check cuDNN installation
dpkg -l | grep cudnn