import os
import platform
import subprocess
import datetime
import numpy as np
import pandas as pd



def run():
    if test_m365() == 'true':
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始运行')
        print('运行状态OK')
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 运行结束')




def test_npm():
    try:
        npm_ver = subprocess.check_output('npm -v', shell=True)
    except Exception as e:
        npm_ver = '0'

    if eval(npm_ver[0:1]) >= 6:
        print('当前npm版本为' + npm_ver + '将继续运行')
        return 'true'
    else:
        print('npm未安装或版本过低，尝试自动安装...')
        sys_ver = platform.uname()
        if 'Debian' in sys_ver or 'Ubuntu' in sys_ver:
            os.system('sudo apt-get update')
            os.system('sudo apt-get upgrade')
            os.system('sudo apt install npm')
            os.system('sudo npm install npm -g')
            os.system('sudo npm cache clean')
            os.system('npm install -g n')
            os.system('sudo n stable')
        elif 'Centos' in sys_ver or 'Redhat' in sys_ver or 'Fedora' in str(sys_ver):
            os.system('sudo yum -y upgrade')
            os.system('sudo yum install npm')
            os.system('sudo npm install npm -g')
            os.system('sudo npm cache clean')
            os.system('npm install -g n')
            os.system('sudo n stable')
        else:
            print('系统为Windows或其他系统，请手动安装nodejs与npm')
            return 'false'
    try:
        npm_ver = subprocess.check_output('npm -v', shell=True)
    except Exception as e:
        npm_ver = '0'

    if eval(npm_ver[0:1]) >= 6:
        print('当前npm版本为' + npm_ver + '将继续运行')
        return 'true'
    else:
        print('npm自动安装/更新失败，请手动安装')


def test_m365():
    if test_npm() == 'true':
        try:
            m365_ver = subprocess.check_output('m365 version', shell=True)
        except Exception as e:
            m365_ver = '0'
        if m365_ver is '0':
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始安装m365')
            os.system('npm install -g @pnp/cli-microsoft365')
        elif m365_ver[1:2] is 'v':
            print('m365环境正常')
            return 'true'
        else:
            print('未知错误，请尝试手动安装m365')
            return 'false'
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' m365安装跳过')
        return 'false'
    try:
        m365_ver = subprocess.check_output('m365 version', shell=True)
    except Exception as e:
        m365_ver = '0'
    if m365_ver[1:2] is 'v':
        print('m365环境正常')
        return 'true'
    else:
        print('未知错误，请尝试手动安装m365')
        return 'false'




run()
