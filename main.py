import subprocess

out_bytes = subprocess.check_output('m365 login  --authType password --userName info@dakfpv.com.au --password Jeremy_2009', shell=True)

print(out_bytes)
