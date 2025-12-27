"""
scyd 运营中台登录
"""

import requests
import yaml
import os


# 获取当前脚本所在文件夹路径
curPath = os.path.dirname(os.path.realpath(__file__))
# 获取yaml文件路径
yamlPath = os.path.join(curPath, "test_data.yaml")

with open(yamlPath,"r",encoding='utf-8') as f:
    result = yaml.load(f.read(),Loader=yaml.FullLoader)



class Login(object):
    def __init__(self,envir):
        self.envir = envir

    # 运营中台登录
    def send_msg(self):
        url = result['login'][self.envir]['url'] + "/ydmanage/v1/sms/send"
        json = {
            "mobile": result['login'][self.envir]['mobile']
        }
        res_data = requests.post(url, json=json).json()
        verifyCode = res_data['data']['verifyCode']
        return verifyCode

    def center_login(self):
        url = result['login'][self.envir]['url'] + "/ydmanage/v1/login"
        print(url)

        json = {
            "workNo": result['login'][self.envir]['work_no'],
            "password": result['login'][self.envir]['password'],
            "verificationCode": self.send_msg()
        }
        print(json)

        res_data = requests.post(url,json=json).json()
        access_token = res_data['data']['token']

        print(res_data)
        print(access_token)
        return access_token


if __name__ == '__main__':
    # pass
    test1 = Login('dev')
    test1.center_login()
