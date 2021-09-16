import requests
import json
import time
import os


def gettimestamp():
    return str(int(time.time() * 1000))


def getitem(searchValue):
    url = "http://127.0.0.1:5700/api/envs?searchValue=%s&t=%s" % (
        searchValue, gettimestamp())
    r = s.get(url)
    print('r:{r}')
    item = json.loads(r.text)["data"]
    print('item:{item}')
    return item


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
            # pin = ck.split(";")[1]
            if code == 0:
                print(nickname, "状态正常\n")
                return True
            else:
                print(nickname, "状态失效\n")
                return False
        else:
            return False
    except Exception:
        print(nickname, "状态失效\n")
        return False


if __name__ == '__main__':
    s = requests.session()
    # cookies = getitem("JD_COOKIE")
    cookies = os.environ['JD_COOKIE']
    cookies = cookies.split('&')
    print(cookies)
    for i in cookies:
        check_ck(cookies[i])
