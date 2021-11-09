# ---------------------------------------------------------------------------------
#
#                       自用脚本，可以借鉴，可以自用，请勿传播
#                           新手学习为主，多为借鉴，想法居多
#                                  实用性较强
#                               更多用法，自己揣摩
#
#
#                                   by Onz3V
#
# ---------------------------------------------------------------------------------
'''
cron: 0 */1 * * * checkCK.py
new Env('cookie过期检测');
'''
import time
import datetime
import os
import http.client
import sys
import random
import requests
import re
import json
from urllib.parse import quote, unquote
import threading
requests.packages.urllib3.disable_warnings()

expiredCount = 0
message_info = ''''''


def message(str_msg):
    global message_info
    print(str_msg)
    message_info = "{}\n{}".format(message_info, str_msg)
    sys.stdout.flush()


def getsendNotify(a=0):
    if a == 0:
        a += 1
    try:
        url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
        response = requests.get(url)
        if 'main' in response.text:
            with open('sendNotify.py', "w+", encoding="utf-8") as f:
                f.write(response.text)
        else:
            if a < 5:
                a += 1
                return getsendNotify(a)
            else:
                pass
    except:
        if a < 5:
            a += 1
            return getsendNotify(a)
        else:
            pass


cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
if os.path.exists(cur_path + "/sendNotify.py"):
    from sendNotify import send
else:
    getsendNotify()
    from sendNotify import send


def println(s):
    print("[{0}]: {1}".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


def ql_login():
    path = '/ql/config/auth.json'
    if os.path.isfile(path):
        with open(path, "r")as file:
            auth = file.read()
            file.close()
        auth = json.loads(auth)
        username = auth["username"]
        password = auth["password"]
        token = auth["token"]
        if token == '':
            url = "http://127.0.0.1:5700/api/login"
            payload = {"username": username, "password": password}
            headers = {'Content-Type': 'application/json'}
            res = requests.post(url=url, headers=headers,
                                data=payload, verify=False)
            token = json.loads(res.text)['token']
            return token
        else:
            return token
    else:
        print("没有发现auth文件, 你这是青龙吗???")
        sys.exit(0)


def get_ck():
    if "JD_COOKIE" in os.environ:
        ck_list = os.environ['JD_COOKIE'].split('&')
        if len(ck_list) > 0:
            return ck_list
        else:
            print("JD_COOKIE变量未启用")
            sys.exit(1)
    else:
        print("未添加JD_COOKIE变量")
        sys.exit(0)


def ql_enable(eid):
    url = 'http://127.0.0.1:5700/api/envs/enable'
    data = '["{0}"]'.format(eid)
    res = json.loads(s.put(url=url, data=data).text)
    if res['code'] == 200:
        print("账号启用成功")
        print("--------------------\n")
        return True
    else:
        print("账号启用失败")
        print("--------------------\n")
        return False


def ql_disable(ck):
    eid = get_id(ck)
    url = 'http://127.0.0.1:5700/api/envs/disable'
    data = '["{0}"]'.format(eid)
    res = json.loads(s.put(url=url, data=data).text)
    if res['code'] == 200:
        println("账号禁用成功")
        # print("--------------------\n")
        return True
    else:
        println("账号禁用失败")
        # print("--------------------\n")
        return False


def get_id(ck):
    conn = http.client.HTTPConnection('127.0.0.1', 5700)
    payload = ''
    url = '/api/envs'
    headers = {'Authorization': 'Bearer '+token}
    conn.request('GET', url, payload, headers)
    res = json.loads(conn.getresponse().read())
    res = res['data']
    index = -1
    for i in range(len(res)):
        if(ck == res[i]['value']):
            index = i
            return res[i]['_id']
    if(index == -1):
        print('没有找到id，应该是没有开启')
        return False


def check_ck(ck):
    url = 'https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder'
    headers = {'Cookie': ck, 'Referer': 'https://home.m.jd.com/myJd/home.action',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1', }
    res = requests.get(url=url, headers=headers, verify=False, timeout=30)
    pin = r.findall(ck)
    pin = unquote(pin[0])
    if res.status_code == 200:
        code = int(json.loads(res.text)['retcode'])
        if code == 0:
            resp = json.loads(res.text)
            global nickname
            nickname = resp['data']['userInfo']['baseInfo']['nickname']
            println(f"账号《{nickname}》的状态正常")
            println('但是我们还想检验一下')
            re_check_ck(ck)
        else:
            println(f"账号《{nickname}》状态已经失效")
            send(f"账号《《{nickname}》状态已经失效", message_info)
            ql_disable(ck)
    else:
        println("接口炸掉了,直接请求加强检查接口")
        re_check_ck(ck)


def re_check_ck(ck):
    url = 'https://plogin.m.jd.com/cgi-bin/ml/islogin'
    headers = {'Cookie': ck, 'Referer': 'https://h5.m.jd.com/',
               'User-Agent': 'jdapp;iPhone;10.1.2;15.0;network/wifi;Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1', }
    res = requests.get(url=url, headers=headers, verify=False, timeout=30)
    pin = r.findall(ck)
    pin = unquote(pin[0])
    if res.status_code == 200:
        code = json.loads(res.text)['islogin']
        if code == "1":
            println(f"账号《{nickname}》的状态确实正常\n")
        else:
            println(f"账号《{nickname}》状态已经失效")
            send(f"账号{nickname}状态已经失效", message_info)
            ql_disable(ck)
    else:
        println("请求超时，接口炸掉了,一会再试吧")


if __name__ == '__main__':
    r = re.compile(r'pt_pin=(.*?);')
    token = ql_login()
    s = requests.session()
    s.headers.update({'authorization': 'Bearer '+str(token)})
    s.headers.update({'Content-Type': 'application/json;charset=UTF-8'})
    # cookies = os.environ['JD_COOKIE'].split('&')
    # cookies = [i for i in cookies if i != '']
    cookies = get_ck()
    if len(cookies) > 0:
        println(f'总共{len(cookies)}个账号\n')
        print('\n--------------正在检测京东账号的可用性----------------\n')
        for ck in cookies:
            check_ck(ck)
    else:
        print('\n--------------没号你测个毛啊----------------\n')
