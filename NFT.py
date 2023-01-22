#!/usr/bin/python
# -*- coding: utf-8 -*-

import qrcode
import qrcode_terminal
import json
import time
import requests
from urllib.parse import urlencode
from hashlib import md5
from typing import Union
from requests_toolbelt.multipart.encoder import MultipartEncoder
import imghdr
import os
import sys

# 声明
# =================================================================================================
os.system('title 哔哩哔哩自定义数字头像 — Powered By Koilo')
print("作者：Koilo   转发请标明出处")
print()
print("本程序仅供学习交流，请勿用于违规用途")
print()

# 获取当前文件所在目录
path = os.path.dirname(os.path.realpath(sys.argv[0]))
new_path = "/".join(path.split("\\"))



print("输入“1”为二维码登录\n输入“2”为链接登录\n输入“3”为密匙登录\n输入“4”获取 ACCESS_KEY\n输入“5”查看参考的相关仓库")
print()
choose_type = input("请输入数字序号：")
print()
if choose_type == "1" or choose_type == "2" or choose_type == "3":
    # 获取头像位置
    images = input("请拖入头像到输入框：")
    print()
if choose_type == "1" or choose_type == "2" or choose_type == "4":
    # 登录模块
    # =================================================================================================

    # 为请求参数进行 api 签名
    def tvsign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
        params.update({'appkey': appkey})
        params = dict(sorted(params.items()))  # 重排序参数 key
        query = urlencode(params)  # 序列化参数
        sign = md5((query + appsec).encode()).hexdigest()  # 计算 api 签名
        params.update({'sign': sign})
        return params


    # 获取二维码数据
    loginInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code', params=tvsign({
        'local_id': '0',
        'ts': int(time.time())
    })).json()

    if choose_type == "1":
        # 生成二维码
        creat_qrcode = qrcode.make(loginInfo['data']['url'])

        # 保存二维码
        with open('{}/qrcode.jpg'.format(new_path), 'wb') as f:
            creat_qrcode.save(f)
        print("已在本目录下生成登录二维码,用手机打开B站扫码登录")
        print()

    elif choose_type == "2":
        # 输出链接
        print("请在浏览器输入链接登录：" + loginInfo['data']['url'])
        print()
    elif choose_type == "4":
        print("请扫描二维码登录：")
        qrcode_terminal.draw(loginInfo['data']['url'])
        print("或打开此链接登录：" + loginInfo['data']['url'])
        print()
        print("或扫描本目录下的 qrcode_login.jpg 登录")
        # 生成二维码
        creat_qrcode = qrcode.make(loginInfo['data']['url'])
        # 保存二维码
        with open('{}/qrcode_login.jpg'.format(new_path), 'wb') as f:
            creat_qrcode.save(f)
        print()

    # 校验
    while True:
        pollInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/poll',
        params=tvsign({
            'auth_code': loginInfo['data']['auth_code'],
            'local_id': '0',
            'ts': int(time.time())
            })).json()

        if pollInfo['code'] == 0:
            loginData = pollInfo['data']
            print("登录成功！")
            print()
            UID = loginData['mid']
            ACCESS_KEY = loginData['access_token']
            break

        elif pollInfo['code'] == -3:
            print('API校验密匙错误！')
            print()
            raise

        elif pollInfo['code'] == -400:
            print('请求错误！')
            print()
            raise

        elif pollInfo['code'] == 86038:
            print('二维码已失效！')
            print()
            raise

        elif pollInfo['code'] == 86039:
            time.sleep(5)

        else:
            print('未知错误！')
            print()
            raise
    if choose_type == "4":
        saveInfo = {
            'update_time': int(time.time() + 0.5),
            'token_info': loginData['token_info'],
            'cookie_info': loginData['cookie_info']
        }
        with open('info.txt', 'w+') as f:
            f.write(json.dumps(saveInfo, ensure_ascii=False, separators=(',', ':')))
            f.close()
            print("文件已保存在本目录下的 info.txt 中")
            print("其中 mid 为 UID ，access_token 为 ACCESS_KEY")
            print()
            input("按回车键退出此程序")
            sys.exit()
    else:
        pass
elif choose_type == "3":
    UID = input(">>> UID：")
    print()
    ACCESS_KEY = input(">>> ACCESS_KEY：")
    print()
elif choose_type == "5":
    print("aristorechina(https://github.com/aristorechina/NFT_auto)")
    print("XiaoMiku01(https://github.com/XiaoMiku01/custom_bilibili_nft)")
    print("cibimo(https://github.com/cibimo/bilibiliLogin)")
    print()
    input("按回车键退出程序")
    sys.exit()
else:
    input("输入序号不正确，按回车键退出")
    sys.exit()

# 头像所在目录
if os.path.exists(images.format(new_path)):
    FACE_PATH = images.format(new_path)
else:
    pass

# 选择需要的卡片种类
card_type = str(input(
    "请选择您想使用的卡片种类后在下方输入对应ID后回车\n可选择ID：\n1：段艺璇-语音类型的数字藏品\n4：胶囊计划\n5：天官赐福\n7，8，9，12：音-福系列数字藏品\n14：三体\n\n请输入您想使用的卡片ID："))
print()


# 更改头像模块
# =================================================================================================
class Crypto:
    APPKEY = '4409e2ce8ffd12b8'
    APPSECRET = '59b43e04ad6965f34319062b478f83dd'

    @staticmethod
    def md5(data: Union[str, bytes]) -> str:
        '''generates md5 hex dump of `str` or `bytes`'''
        if type(data) == str:
            return md5(data.encode()).hexdigest()
        return md5(data).hexdigest()

    @staticmethod
    def sign(data: Union[str, dict]) -> str:
        '''salted sign funtion for `dict`(converts to qs then parse) & `str`'''
        if isinstance(data, dict):
            _str = urlencode(data)
        elif type(data) != str:
            raise TypeError
        return Crypto.md5(_str + Crypto.APPSECRET)


class SingableDict(dict):
    @property
    def sorted(self):
        '''returns a alphabetically sorted version of `self`'''
        return dict(sorted(self.items()))

    @property
    def signed(self):
        '''returns our sorted self with calculated `sign` as a new key-value pair at the end'''
        _sorted = self.sorted
        return {**_sorted, 'sign': Crypto.sign(_sorted)}


def get_image_type(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return imghdr.what(None, data)


def upload_image(file_path):
    url = "https://api.bilibili.com/x/upload/app/image?access_key=" + ACCESS_KEY

    payload = {'bucket': 'medialist', 'dir': 'nft'}

    with open(file_path, 'rb') as f:
        type = f'image/{imghdr.what(f)}'
        print(type)
        files = [
            (
                'file',
                (file_path, f, type),
            )
        ]
        response = requests.request("POST", url, data=payload, files=files)
        print(response.text)
        return response.json()['data']['location']


# 获取卡片信息
def get_one_card_id():
    url = "https://api.bilibili.com/x/vas/nftcard/cardlist"
    params = SingableDict(
        {
            "access_key": ACCESS_KEY,
            "act_id": card_type,
            "appkey": "4409e2ce8ffd12b8",
            "disable_rcmd": "0",
            "ruid": UID,
            "statistics": "{\"appId\":1,\"platform\":3,\"version\":\"7.9.0\",\"abtest\":\"\"}",
            "ts": int(time.time()),
        }
    ).signed
    response = requests.request("GET", url, params=params)
    data = response.json()

    # 遍历数据，得出可用结果输出供用户选择

    print("请在下列卡片中选择一个(卡片名称:对应卡片ID)")
    for round in data['data']['round_list']:
        for card in round['card_list']:
            if card['card_id_list']:
                print(card['card_name'], ":", card['card_id_list'][0]['card_id'])
    if data['data']['pre_list']:
        for pre in data['data']['pre_list']:
            if pre['card_id_list']:
                print(pre['card_name'], ":", pre['card_id_list'][0]['card_id'])
    choose_card_id = input("请输入ID后回车(如果没有回车会自动退出):\n")
    return choose_card_id


def set_face(card_id):
    api = "https://api.bilibili.com/x/member/app/face/digitalKit/update"
    params = SingableDict(
        {
            "access_key": ACCESS_KEY,
            "appkey": "4409e2ce8ffd12b8",
            "build": "7090300",
            "c_locale": "zh_CN",
            "channel": "xiaomi",
            "disable_rcmd": "0",
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": "{\"appId\":1,\"platform\":3,\"version\":\"7.9.0\",\"abtest\":\"\"}",
            "ts": int(time.time()),
        }
    ).signed
    m = MultipartEncoder(
        fields={
            'digital_kit_id': str(card_id),
            'face': ('face', open(FACE_PATH, 'rb'), 'application/octet-stream'),
        }
    )
    headers = {
        "Content-Type": m.content_type,
    }
    response = requests.request("POST", api, data=m, headers=headers, params=params)
    if response.json()['code'] != 0:
        print(response.json())
        return
    print()
    print('设置头像成功, 请等待审核')
    print()


def main():
    card_id = get_one_card_id()
    if not card_id:
        return
    set_face(card_id)


if __name__ == '__main__':
    main()
    input("按下回车键结束")
