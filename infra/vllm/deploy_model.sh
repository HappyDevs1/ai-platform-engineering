#!/bin/bash

# Deploy the Qwen2.5-3B-Instruct model using vLLM
vllm serve Qwen/Qwen2.5-3B-Instruct --host 0.0.0.0 --port 8000