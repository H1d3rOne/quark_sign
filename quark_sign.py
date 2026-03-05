# -*- coding: utf-8 -*-

import os
import re
import sys
import time
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_env():
    if "COOKIE_QUARK" in os.environ:
        cookie_list = re.split('\n|&&', os.environ.get('COOKIE_QUARK'))
    else:
        print('❌未添加COOKIE_QUARK变量')
        send_to_wxwork('夸克自动签到,❌未添加COOKIE_QUARK变量')
        sys.exit(0)

    return cookie_list

def create_session():
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
  
def send_to_wxwork(content):
    webhook = os.environ.get('WEBHOOK_URL', '')
    if not webhook:
        print('❌未添加WEBHOOK_URL变量')
        return
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    hook_data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    try:
        session = create_session()
        response = session.post(webhook, json=hook_data, headers=headers, timeout=10)
        response.raise_for_status()
        print('✅ 企业微信通知发送成功')
    except Exception as e:
        print(f'❌ 企业微信通知发送失败: {str(e)}')

class Quark:
    '''
    Quark类封装了签到、领取签到奖励的方法
    '''
    def __init__(self, user_data):
        '''
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        '''
        self.param = user_data

    def convert_bytes(self, b):
        '''
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回 MB GB TB
        '''
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024
            i += 1
        return f"{b:.2f} {units[i]}"

    def get_growth_info(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        try:
            session = create_session()
            response = session.get(url=url, params=querystring, timeout=10)
            response.raise_for_status()
            json_response = response.json()
            if json_response.get("data"):
                return json_response["data"], None
            else:
                error_msg = f"获取成长信息失败: {json_response.get('message', '未知错误')}"
                print(f'❌ {error_msg}')
                return False, error_msg
        except Exception as e:
            error_msg = f'获取成长信息异常: {str(e)}'
            print(f'❌ {error_msg}')
            return False, error_msg

    def get_growth_sign(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        data = {"sign_cyclic": True}
        try:
            session = create_session()
            response = session.post(url=url, json=data, params=querystring, timeout=10)
            response.raise_for_status()
            json_response = response.json()
            if json_response.get("data"):
                return True, json_response["data"]["sign_daily_reward"], None
            else:
                error_msg = f"签到失败: {json_response.get('message', '未知错误')}"
                print(f'❌ {error_msg}')
                return False, 0, error_msg
        except Exception as e:
            error_msg = f'签到异常: {str(e)}'
            print(f'❌ {error_msg}')
            return False, 0, error_msg

    def queryBalance(self):
        '''
        查询抽奖余额
        '''
        url = "https://coral2.quark.cn/currency/v1/queryBalance"
        querystring = {
            "moduleCode": "1f3563d38896438db994f118d4ff53cb",
            "kps": self.param.get('kps'),
        }
        response = requests.get(url=url, params=querystring).json()
        if response.get("data"):
            return response["data"]["balance"]
        else:
            return response["msg"]

    def do_sign(self):
        '''
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        '''
        log = ""
        errors = []
        growth_info, error = self.get_growth_info()
        if error:
            errors.append(error)
        
        if growth_info:
            log += (
                f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
                f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
                f"签到累计容量："
            )
            if "sign_reward" in growth_info['cap_composition']:
                log += f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
            else:
                log += "0 MB\n"
            if growth_info["cap_sign"]["sign_daily"]:
                log += (
                    f"✅ 签到日志: 今日已签到+{self.convert_bytes(growth_info['cap_sign']['sign_daily_reward'])}，"
                    f"连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})\n"
                )
            else:
                sign, sign_return, error = self.get_growth_sign()
                if error:
                    errors.append(error)
                if sign:
                    log += (
                        f"✅ 执行签到: 今日签到+{self.convert_bytes(sign_return)}，"
                        f"连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})\n"
                    )

        return log, errors


def main():
    '''
    主函数
    :return: 返回一个字符串，包含签到结果
    '''
    msg = ""
    all_errors = []
    global cookie_quark
    cookie_quark = get_env()

    print("✅ 检测到共", len(cookie_quark), "个夸克账号\n")

    i = 0
    while i < len(cookie_quark):
        user_data = {}
        for a in cookie_quark[i].replace(" ", "").split(';'):
            if not a == '':
                item = a.split('=', 1)
                user_data[item[0]] = item[1]
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        log, errors = Quark(user_data).do_sign()
        msg += log + "\n"
        if errors:
            all_errors.extend(errors)

        i += 1

    try:
        final_message = f'夸克自动签到：\n{msg}({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})'
        
        if all_errors:
            error_msg = "\n⚠️ 异常提醒：\n" + "\n".join([f"• {err}" for err in all_errors])
            final_message += error_msg
        
        print(final_message)
        send_to_wxwork(final_message)
    except Exception as err:
        print('%s\n❌ 错误，请查看运行日志！' % err)

    return msg[:-1]

if __name__ == "__main__":
    print("----------夸克网盘开始签到----------")
    main()
    print("----------夸克网盘签到完毕----------")
