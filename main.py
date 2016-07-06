# -*- coding: utf-8 -*-

import logging
import sys
import time

import config
from log import init_log
from shike import ShikeClient
from wechat import post_template_message, WeChatApiClient

wechat = WeChatApiClient(config.appid, config.appsecret)
wechat.on_servererror = lambda resp, *args, **kwargs: logging.error(str(resp.text))
wechat.on_wechaterror = lambda resp, *args, **kwargs: logging.error(str(resp.text))


def load_user(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def send_wechat_msg(openid, template_id, url="", **kwargs):
    resp, code = post_template_message(wechat,
        openid, template_id, url, **kwargs)
    if code:
        logging.error("WeChatError: " + str(resp))
    else:
        logging.info("WeChatSendSuccess: " + str(resp))

def do_request(openid):
    apps = client.load_apps()
    availables = client.filter_apps(apps)
    # 先判断是否有正在处理的app
    processing = list(filter(lambda o: int(o["status"])==0, availables))
    if processing:
        # 正在处理的app查询是否已经可以打开
        app = processing[0]
        flg = client.get_app_status(app)
        if flg == "waitOpen":
            send_wechat_msg(openid, config.down_template, "",
                first=app["name"],
                remark="请及时打开！")
            time.sleep(config.down_break)
        else:
            time.sleep(config.req_break)
    elif availables:
        # 有应用可供下载
        availables = client.sort_app(availables)
        app = availables[0]
        logging.info("Got! " + app["name"])
        
        collected = client.collect_app(app)
        remark = "，任务已自动领取了哦！ " if collected else ""
        send_wechat_msg(openid, config.got_template, "",
            first=app["name"],
            keyword1=app["name"],
            keyword2=str(int(app["file_size_bytes"])/1024/1024) + "MB",
            keyword3=app["order_status_disp"],
            remark="一共" + str(len(availables)) + "个应用可供下载" + remark)
            
        if collected:
            time.sleep(config.success_break)
        else:
            time.sleep(config.req_break)
    else:
        time.sleep(config.req_break)

uid, id, idfa, openid = load_user(sys.argv[1])

init_log(uid)

client = ShikeClient(uid, id, idfa)
client.init()

while True:
    do_request(openid)