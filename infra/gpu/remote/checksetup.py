import subprocess
import sys

podIp = sys.argv[1]
port = sys.argv[2]


podSsh =subprocess.run(["bash", "infra/gpu/remote/sshintopod.sh", podIp, port])

configCheck = subprocess.run(["bash", "infra/gpu/remote/checkpodconfig.sh"])