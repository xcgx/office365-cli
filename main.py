import subprocess

out_bytes = subprocess.check_output('ls -l', shell=True)

print(out_bytes)
