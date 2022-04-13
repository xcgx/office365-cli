import subprocess

out_bytes = subprocess.check_output('apt install npm', shell=True)

print(out_bytes)
