import time
import datetime
import os
import sys
import random
import requests
import re
import json
from urllib.parse import quote, unquote
import threading
requests.packages.urllib3.disable_warnings()


def println(s):
    print("[{0}]: {1}".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


def check_ck(ck):
    url = 'https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder'
    headers = {'Cookie': ck, 'Referer': 'https://home.m.jd.com/myJd/home.action',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1', }
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=30)
        if res.status_code == 200:
            code = int(json.loads(res.text)['retcode'])
            resp = json.loads(res.text)
            nickname = resp['data']['userInfo']['baseInfo']['nickname']
            if code == 0:
                println(f"账号{nickname}的状态正常\n")
                return True
            else:
                println(f"账号{nickname}状态已经失效\n")
                return False
        else:
            return False
    except Exception:
        print(nickname, "状态失效\n")
        return False


if __name__ == '__main__':
    cookies = os.environ['JD_COOKIE']
    cookies = cookies.split('&')
    cookies = [i for i in cookies if i != '']
    if len(cookies) > 0:
        println(f'总共{len(cookies)}个账号\n')
        print('\n--------------正在检测京东账号的可用性----------------\n')
        for ck in cookies:
            check_ck(ck)
    else:
        print('\n--------------没号你测个毛啊----------------\n')
