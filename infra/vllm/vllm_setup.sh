#!/bin/bash

# Install vLLM from source
git clone https://github.com/vllm-project/vllm.git
cd vllm

# Build and install vLLM with maximum parallel jobs to prevent RAM crashes
export MAX_JOBS=6
pip install -e .