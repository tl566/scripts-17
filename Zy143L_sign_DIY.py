# 解密Zy143L的wskey转换脚本
# 删除boom方法
# 调用ddo的获取sign的云接口
# 参考皮卡丘的相关代码，加入通知服务，wskey过期自动通知

# 此版本是我认为市面上相对安全的版本，可以放心使用。建议自用，勿传播。
import hashlib
import base64
import http.client
import json
import os
import sys
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests模块, 请执行命令：pip3 install requests\n")
    sys.exit(1)
os.environ['no_proxy'] = '*'
requests.packages.urllib3.disable_warnings()

# Env环境设置 通知服务
# export BARK=''                   # bark服务,苹果商店自行搜索;
# export SCKEY=''                  # Server酱的SCKEY;
# export TG_BOT_TOKEN=''           # tg机器人的TG_BOT_TOKEN;
# export TG_USER_ID=''             # tg机器人的TG_USER_ID;
# export TG_API_HOST=''            # tg 代理api
# export TG_PROXY_IP=''            # tg机器人的TG_PROXY_IP;
# export TG_PROXY_PORT=''          # tg机器人的TG_PROXY_PORT;
# export DD_BOT_ACCESS_TOKEN=''    # 钉钉机器人的DD_BOT_ACCESS_TOKEN;
# export DD_BOT_SECRET=''          # 钉钉机器人的DD_BOT_SECRET;
# export QQ_SKEY=''                # qq机器人的QQ_SKEY;
# export QQ_MODE=''                # qq机器人的QQ_MODE;
# export QYWX_AM=''                # 企业微信；http://note.youdao.com/s/HMiudGkb
# export PUSH_PLUS_TOKEN=''        # 微信推送Plus+ ；

# 获取通知模块
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
###################


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


def get_wskey():
    if "JD_WSCK" in os.environ:
        wskey_list = os.environ['JD_WSCK'].split('&')
        if len(wskey_list) > 0:
            return wskey_list
        else:
            print("JD_WSCK变量未启用")
            sys.exit(1)
    else:
        print("未添加JD_WSCK变量")
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


def check_ck(ck):
    url = 'https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder'
    headers = {'Cookie': ck, 'Referer': 'https://home.m.jd.com/myJd/home.action',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1', }
    res = requests.get(url=url, headers=headers, verify=False, timeout=30)
    if res.status_code == 200:
        code = int(json.loads(res.text)['retcode'])
        pin = ck.split(";")[1]
        if code == 0:
            print(pin, "状态正常\n")
            return True
        else:
            print(pin, "状态失效\n")
            return False
    else:
        return False


def getToken(wskey):
    headers = {'cookie': wskey, 'User-Agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1440x3007;os/11;network/wifi;',
               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'charset': 'UTF-8', 'accept-encoding': 'br,gzip,deflate'}
    params = {'functionId': 'genToken', 'clientVersion': '10.1.2',
              'client': 'android', 'uuid': uuid, 'st': st, 'sign': sign, 'sv': sv}
    url = 'https://api.m.jd.com/client.action'
    data = 'body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fplogin.m.jd.com%252Fcgi-bin%252Fm%252Fthirdapp_auth_page%253Ftoken%253DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%2526client_type%253Dandroid%2526appid%253D879%2526appup_type%253D1%22%7D&'
    res = requests.post(url=url, params=params,
                        headers=headers, data=data, verify=False)
    res_json = json.loads(res.text)
    print(res_json)
    tokenKey = res_json['tokenKey']
    return appjmp(wskey, tokenKey)


def appjmp(wskey, tokenKey):
    headers = {'User-Agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1440x3007;os/11;network/wifi;',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', }
    params = {'tokenKey': tokenKey, 'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg',
              'client_type': 'android', 'appid': 879, 'appup_type': 1, }
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    res = requests.get(url=url, headers=headers, params=params,
                       verify=False, allow_redirects=False)
    res_set = res.cookies.get_dict()
    pt_key = 'pt_key='+res_set['pt_key']
    pt_pin = 'pt_pin='+res_set['pt_pin']
    jd_ck = str(pt_key)+';'+str(pt_pin)+';'
    wskey = wskey.split(";")[0]
    if 'fake' in pt_key:
        print(wskey, "wskey状态失效\n")
        send(wskey+"的wskey状态失效\n请查看是否退出客户端或者修改过密码", message_info)
        return False, jd_ck
    else:
        print(wskey, "wskey状态正常\n")
        return True, jd_ck


def bytes2bin(bytes):  # 字节转二进制
    arr = []
    for v in [m for m in bytes]:
        arr.append(
            [(v & 128) >> 7, (v & 64) >> 6, (v & 32) >> 5, (v & 16) >> 4, (v & 8) >> 3, (v & 4) >> 2, (v & 2) >> 1,
             v & 1])
    return [i for j in arr for i in j]


def bin2bytes(arr):  # 二进制转字节
    length = len(arr) // 8
    arr1 = [0 for _ in range(length)]
    for j in range(length):
        arr1[j] = arr[j * 8] << 7 | arr[j * 8 + 1] << 6 | arr[j * 8 + 2] << 5 | arr[j * 8 + 3] << 4 | arr[
            j * 8 + 4] << 3 | arr[j * 8 + 5] << 2 | arr[j * 8 + 6] << 1 | arr[j * 8 + 7]
    return bytes(arr1)


def sub_10EA4(input):
    # 输入8个字节
    table = [[0, 0], [1, 4], [2, 61], [3, 15], [4, 56], [5, 40], [6, 6], [7, 59], [8, 62], [9, 58], [10, 17],
             [11, 2],
             [12, 12], [13, 8], [14, 32], [15, 60], [16, 13], [
                 17, 45], [18, 34], [19, 14], [20, 36], [21, 21],
             [22, 22], [23, 39], [24, 23], [25, 25], [26, 26], [
                 27, 20], [28, 1], [29, 33], [30, 46], [31, 55],
             [32, 35], [33, 24], [34, 57], [35, 19], [36, 53], [
                 37, 37], [38, 38], [39, 5], [40, 30], [41, 41],
             [42, 42], [43, 18], [44, 47], [45, 27], [46, 9], [
                 47, 44], [48, 51], [49, 7], [50, 49], [51, 63],
             [52, 28],
             [53, 43], [54, 54], [55, 52], [56, 31], [57, 10], [
                 58, 29], [59, 11], [60, 3], [61, 16], [62, 50],
             [63, 48]]
    arr = bytes2bin(input)
    arr1 = [0 for i in range(len(arr))]
    for i in range(len(table)):
        arr1[table[i][1]] = arr[table[i][0]]
    # print(arr1)
    # print(len(arr1))
    return bin2bytes(arr1)


def sub_10D70(input, remaining_byte_num):
    table0 = [[0, 6, 0, 1], [1, 4, 1, 0], [2, 5, 0, 1], [3, 0, 0, 1], [4, 2, 0, 1], [5, 3, 0, 1], [6, 1, 1, 0],
              [7, 7, 0, 1]]

    table1 = [[0, 5, 0, 1], [1, 9, 0, 1], [2, 0, 1, 0], [3, 7, 1, 0], [4, 10, 0, 1], [5, 6, 0, 1], [6, 13, 1, 0],
              [7, 1, 0, 1], [8, 4, 0, 1], [9, 11, 0, 1], [10, 14, 1, 0], [
                  11, 3, 1, 0], [12, 12, 0, 1], [13, 15, 1, 0],
              [14, 8, 0, 1], [15, 2, 0, 1]]

    table2 = [[0, 17, 0, 1], [1, 7, 0, 1], [2, 5, 0, 1], [3, 19, 1, 0], [4, 18, 0, 1], [5, 15, 1, 0], [6, 22, 0, 1],
              [7, 21, 0, 1], [8, 16, 0, 1], [9, 4, 0, 1], [10, 12, 0, 1], [
                  11, 2, 1, 0], [12, 10, 1, 0], [13, 13, 1, 0],
              [14, 20, 1, 0], [15, 8, 1, 0], [16, 9, 0, 1], [
                  17, 23, 0, 1], [18, 11, 1, 0], [19, 6, 0, 1],
              [20, 1, 0, 1],
              [21, 3, 1, 0], [22, 0, 1, 0], [23, 14, 0, 1]]

    table3 = [[0, 25, 1, 0], [1, 4, 0, 1], [2, 29, 0, 1], [3, 1, 0, 1], [4, 27, 1, 0], [5, 18, 1, 0], [6, 23, 1, 0],
              [7, 14, 1, 0], [8, 28, 1, 0], [9, 11, 0, 1], [10, 9, 1, 0], [
                  11, 13, 0, 1], [12, 24, 1, 0], [13, 0, 1, 0],
              [14, 5, 0, 1], [15, 2, 1, 0], [16, 26, 0, 1], [
                  17, 12, 0, 1], [18, 31, 1, 0], [19, 16, 1, 0],
              [20, 30, 0, 1],
              [21, 15, 0, 1], [22, 10, 0, 1], [23, 22, 1, 0], [
                  24, 7, 1, 0], [25, 21, 0, 1], [26, 6, 1, 0],
              [27, 3, 1, 0],
              [28, 8, 1, 0], [29, 20, 0, 1], [30, 19, 1, 0], [31, 17, 0, 1]]

    table4 = [[0, 11, 0, 1], [1, 12, 0, 1], [2, 28, 1, 0], [3, 30, 0, 1], [4, 13, 1, 0], [5, 24, 0, 1], [6, 22, 1, 0],
              [7, 25, 1, 0], [8, 23, 1, 0], [9, 3, 0, 1], [10, 16, 0, 1], [
                  11, 8, 1, 0], [12, 34, 0, 1], [13, 2, 0, 1],
              [14, 5, 0, 1], [15, 7, 1, 0], [16, 4, 0, 1], [
                  17, 14, 0, 1], [18, 39, 1, 0], [19, 33, 0, 1],
              [20, 15, 0, 1],
              [21, 0, 0, 1], [22, 31, 0, 1], [23, 9, 1, 0], [
                  24, 29, 0, 1], [25, 26, 1, 0], [26, 19, 0, 1],
              [27, 6, 1, 0],
              [28, 27, 1, 0], [29, 10, 1, 0], [30, 37, 0, 1], [
                  31, 38, 1, 0], [32, 20, 0, 1], [33, 21, 1, 0],
              [34, 1, 0, 1],
              [35, 36, 0, 1], [36, 32, 0, 1], [37, 17, 0, 1], [38, 18, 0, 1], [39, 35, 1, 0]]

    table5 = [[0, 11, 0, 1], [1, 45, 0, 1], [2, 15, 1, 0], [3, 22, 0, 1], [4, 10, 0, 1], [5, 7, 0, 1], [6, 3, 0, 1],
              [7, 42, 0, 1], [8, 17, 1, 0], [9, 21, 0, 1], [10, 4, 0, 1], [
                  11, 8, 1, 0], [12, 19, 1, 0], [13, 32, 0, 1],
              [14, 28, 1, 0], [15, 31, 1, 0], [16, 29, 0, 1], [
                  17, 14, 1, 0], [18, 39, 1, 0], [19, 27, 1, 0],
              [20, 2, 1, 0],
              [21, 24, 0, 1], [22, 26, 1, 0], [23, 9, 1, 0], [
                  24, 41, 0, 1], [25, 1, 1, 0], [26, 47, 0, 1],
              [27, 44, 0, 1],
              [28, 23, 1, 0], [29, 0, 1, 0], [30, 12, 1, 0], [
                  31, 18, 0, 1], [32, 33, 0, 1], [33, 36, 0, 1],
              [34, 40, 1, 0],
              [35, 34, 0, 1], [36, 25, 0, 1], [37, 16, 1, 0], [
                  38, 5, 1, 0], [39, 35, 0, 1], [40, 38, 0, 1],
              [41, 37, 1, 0],
              [42, 13, 0, 1], [43, 20, 1, 0], [44, 6, 0, 1], [45, 43, 0, 1], [46, 30, 0, 1], [47, 46, 1, 0]]

    table6 = [[0, 7, 1, 0], [1, 9, 0, 1], [2, 53, 1, 0], [3, 19, 1, 0], [4, 15, 1, 0], [5, 8, 0, 1], [6, 3, 0, 1],
              [7, 24, 1, 0],
              [8, 18, 0, 1], [9, 51, 0, 1], [10, 42, 1, 0], [
                  11, 39, 0, 1], [12, 20, 0, 1], [13, 12, 0, 1],
              [14, 28, 1, 0],
              [15, 27, 1, 0], [16, 23, 0, 1], [17, 49, 0, 1], [
                  18, 10, 1, 0], [19, 55, 1, 0], [20, 52, 1, 0],
              [21, 17, 0, 1],
              [22, 48, 0, 1], [23, 14, 1, 0], [24, 33, 0, 1], [
                  25, 25, 1, 0], [26, 4, 1, 0], [27, 11, 0, 1],
              [28, 47, 1, 0],
              [29, 0, 0, 1], [30, 21, 1, 0], [31, 44, 0, 1], [
                  32, 16, 0, 1], [33, 41, 0, 1], [34, 29, 0, 1],
              [35, 1, 0, 1],
              [36, 46, 0, 1], [37, 5, 0, 1], [38, 30, 0, 1], [
                  39, 45, 0, 1], [40, 31, 1, 0], [41, 43, 1, 0],
              [42, 36, 1, 0],
              [43, 26, 0, 1], [44, 34, 0, 1], [45, 2, 0, 1], [
                  46, 6, 0, 1], [47, 50, 1, 0], [48, 13, 1, 0],
              [49, 37, 1, 0],
              [50, 32, 0, 1], [51, 40, 0, 1], [52, 35, 0, 1], [53, 38, 0, 1], [54, 54, 0, 1], [55, 22, 0, 1]]

    tables = [table0, table1, table2, table3, table4, table5, table6]
    table = tables[remaining_byte_num - 1]
    arr = bytes2bin(input)
    bit_num = 8 * remaining_byte_num
    arr1 = [0] * bit_num
    for i in range(bit_num):
        if arr[i] == 0:
            arr1[table[i][1]] = table[i][2]
        else:
            arr1[table[i][1]] = table[i][3]
    return bin2bytes(arr1)


def JDencrypt_version0(plainTextDic, ran1):
    encrypt_version_0 = [100, 112, 121]
    # encrypt_version_1 = [110, 101, 122]
    # encrypt_version_2 = [120, 102, 111]
    plainTextDic['sv'] = encrypt_version_0[ran1]
    text_index = ['functionId', 'body', 'uuid',
                  'client', 'clientVersion', 'st', 'sv']
    join_text = ['%s=%s' % (text_index[i], plainTextDic[text_index[i]])
                 for i in range(len(text_index))]
    plainText = '&'.join(join_text)
    # print(plainText)
    plainTextByte = bytes(plainText, encoding='utf-8')

    # --------------------------encrypt_version_0加密------------------------------- #
    # 每次加密8个字节，8字节由sub_10EA4进行加密
    byte_val_final = b''
    byte_val_from_sub_10EA4 = b''
    eight_byte_num = len(plainText) // 8
    for i in range(eight_byte_num):
        byte_val_from_sub_10EA4 += sub_10EA4(plainTextByte[i * 8: (i + 1) * 8])
    # print(byte_val_from_sub_10EA4)

    # 加密剩余的字节
    plainTextRemaining = plainText[int(8 * eight_byte_num):]
    plainTextRemaining_length = len(plainTextRemaining)
    # print('剩余字节数量：%d，剩余字节字符串：%s' % (plainTextRemaining_length, plainTextRemaining))

    plainTextRemainingByte = bytes(plainTextRemaining, encoding='utf-8')
    byte_val_from_sub_10D70 = sub_10D70(
        plainTextRemainingByte, plainTextRemaining_length)
    # print('剩余字节加密前结果：%s，加密后结果：%s' % (plainTextRemainingByte, byte_val_from_sub_10D70))
    byte_val_final = byte_val_from_sub_10EA4 + byte_val_from_sub_10D70

    # print(byte_val_final)
    # base64和md5加密
    md5 = hashlib.md5()
    md5.update(base64.b64encode(byte_val_final))
    result = {
        'st': plainTextDic['st'],
        'sign': md5.hexdigest(),
        'sv': plainTextDic['sv']
    }
    # result = 'st=%s&sign=%s&sv=%s' % (
    #     plainTextDic['st'], md5.hexdigest(), plainTextDic['sv'])
    # print(result)
    return result


def randomParams():

    return


def get_sign():
    ran1 = 2  # sv随机数
    plainTextDic = {
        'functionId': 'genToken',
        'clientVersion': '10.1.2',
        'client': 'android',
        'uuid': 'a27c56da92d3c148',
        'body': '{"action":"to","to":"https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D100012043978"}',
        'st': 1631763902041
    }
    # print(JDencrypt_version0(plainTextDic=plainTextDic, ran1=ran1))
    # url = 'https://hellodns.coding.net/p/sign/d/jsign/git/raw/master/sign'
    # res = requests.get(url=url, verify=False, timeout=20)
    # sign_list = json.loads(res.text)
    sign_list = JDencrypt_version0(
        plainTextDic=plainTextDic, ran1=ran1)
    svv = plainTextDic['sv']
    stt = plainTextDic['st']
    suid = plainTextDic['uuid']
    jign = sign_list['sign']
    return suid, stt, svv, jign


def serch_ck(pin):
    pin2 = pin.replace('%', '%5C%25')
    conn = http.client.HTTPConnection("127.0.0.1", 5700)
    payload = ''
    headers = {'Authorization': 'Bearer '+token}
    url = '/api/envs?searchValue={0}'.format(pin2)
    conn.request("GET", url, payload, headers)
    res = json.loads(conn.getresponse().read())
    if len(res['data']) == 0:
        print(pin, "检索失败\n")
        return False, 1
    elif len(res['data']) > 1:
        print(pin, "Pin存在重复, 取第一条\n")
        key = res['data'][0]['value']
        eid = res['data'][0]['_id']
        return True, key, eid
    else:
        print(pin, "检索成功\n")
        key = res['data'][0]['value']
        eid = res['data'][0]['_id']
        return True, key, eid


def ql_update(eid, n_ck):
    url = 'http://127.0.0.1:5700/api/envs'
    data = {"name": "JD_COOKIE", "value": n_ck, "_id": eid}
    data = json.dumps(data)
    res = json.loads(s.put(url=url, data=data).text)
    if res['data']['status'] == 1:
        ql_enable(eid)


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


def ql_disable(eid):
    url = 'http://127.0.0.1:5700/api/envs/disable'
    data = '["{0}"]'.format(eid)
    res = json.loads(s.put(url=url, data=data).text)
    if res['code'] == 200:
        print("账号禁用成功")
        print("--------------------\n")
        return True
    else:
        print("账号禁用失败")
        print("--------------------\n")
        return False


def ql_insert(i_ck):
    data = [{"value": i_ck, "name": "JD_COOKIE"}]
    data = json.dumps(data)
    url = 'http://127.0.0.1:5700/api/envs'
    s.post(url=url, data=data)
    print("账号添加完成")
    print("--------------------\n")


if __name__ == '__main__':
    st, uuid, sv, sign = get_sign()
    print(st, uuid, sv, sign)
    token = ql_login()
    s = requests.session()
    s.headers.update({"authorization": "Bearer "+str(token)})
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    wslist = get_wskey()
    for ws in wslist:
        wspin = ws.split(";")[0]
        if "pin" in wspin:
            wspin = "pt_"+wspin
            return_serch = serch_ck(wspin)
            if return_serch[0]:
                jck = str(return_serch[1])
                if not check_ck(jck):
                    return_ws = getToken(ws)
                    print(return_ws)
                    if return_ws[0]:
                        nt_key = str(return_ws[1])
                        print("wskey转换成功\n")
                        eid = return_serch[2]
                        ql_update(eid, nt_key)
                    else:
                        print(ws, "wskey失效\n")
                        send(ws+"的wskey状态失效\n请查看是否退出了客户端或者修改过密码", message_info)
                        eid = return_serch[2]
                        print("禁用账号", wspin)
                        ql_disable(eid)
                else:
                    print(wspin, "账号有效")
                    print("--------------------\n")

            else:
                print("wskey未生成pt_key\n")
                return_ws = getToken(ws)
                if return_ws[0]:
                    nt_key = str(return_ws[1])
                    print("wskey转换成功\n")
                    ql_insert(nt_key)
        else:
            print("WSKEY格式错误\n--------------------\n")
    print("执行完成\n--------------------")
    sys.exit(0)
