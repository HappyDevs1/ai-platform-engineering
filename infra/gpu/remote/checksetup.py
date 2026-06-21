import subprocess
import sys

podIp = sys.argv[1]
port = sys.argv[2]
local_script_path = "infra/gpu/remote/checkpodconfig.sh"

with open(local_script_path, 'r') as file:
    local_script_content = file.read().encode('utf-8')

result = subprocess.run(["bash", "infra/gpu/remote/sshintopod.sh", podIp, port], input=local_script_content)


if result.returncode == 0:
  print("Pod setup is correct.")
else:
  print(result.stderr)
  sys.exit(1)
