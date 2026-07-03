import subprocess
import sys

vllm_result = subprocess.run(["bash", "infra/gpu/vllm/vllm_setup.sh"])

if vllm_result.returncode == 0:
  print("VLLM installation succeded")
else:
  sys.exit(1)

model_deploy_result = subprocess.run(["bash", "infra/gpu/vllm/deploy_model.sh"])

if model_deploy_result.returncode == 0:
  print("Model deployed successfully at full precision")
else:
  sys.exit(1)