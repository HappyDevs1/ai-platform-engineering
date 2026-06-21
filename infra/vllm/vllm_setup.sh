#!/bin/bash

git clone https://github.com/vllm-project/vllm.git
cd vllm

export MAX_JOBS=6
pip install -e .