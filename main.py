import subprocess

out_bytes = subprocess.check_output('npm install -g @pnp/cli-microsoft365', shell=True)

print(out_bytes)
