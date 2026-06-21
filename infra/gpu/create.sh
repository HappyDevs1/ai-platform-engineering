#!/bin/bash

runpodctl pod create --template-id "$1" --gpu-id "$2"