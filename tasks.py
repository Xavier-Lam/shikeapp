# -*- coding: utf-8 -*-

import logging

from celery import Celery

import config
from log import init_log
from model import Session, User
from shike import ShikeClient
from wechat import post_template_message, WeChatApiClient

app = Celery("tasks", broker=config.broker, backend=config.backend)

@app.task(bind=True)
def run(self, client):
    logger.info("Task starts: " + client.uid)
    delay = config.req_break
    try:
        apps = client.load_apps()
        availables = client.filter_apps(apps)
        # 先判断是否有正在处理的app
        processing = list(filter(lambda o: int(o["status"])==0, availables))
        if processing:
            # 正在处理的app查询是否已经可以打开
            app = processing[0]
            flg = client.get_app_status(app)
            if flg == "waitOpen":
                send_wechat_msg(user.openid, config.down_template, "",
                    first=app["name"],
                    remark="请及时打开！")
                delay = config.down_break
        elif availables:
            # 有应用可供下载
            availables = client.sort_app(availables)
            app = availables[0]
            logger.info("Got! " + app["name"])
            
            collected = client.collect_app(app)
            remark = "，任务已自动领取了哦！ " if collected else ""
            send_wechat_msg(user.openid, config.got_template, "",
                first=app["name"],
                keyword1=app["name"],
                keyword2=str(int(app["file_size_bytes"])/1024/1024) + "MB",
                keyword3=app["order_status_disp"],
                remark="一共" + str(len(availables)) + "个应用可供下载" + remark)
                
            if collected:
                delay = config.success_break
        logger.info("Task complete: " + client.uid)
        run.apply_async((client,), countdown=delay)
    except Exception as e:
        logger.error("An error occured: " + str(e))
        self.retry(exe=e, countdown=delay)

def send_wechat_msg(openid, template_id, url="", **kwargs):
    """发送微信消息"""
    resp, code = post_template_message(wechat,
        openid, template_id, url, **kwargs)
    if code:
        logger.error("WeChatError: " + str(resp))
    else:
        logger.info("WeChatSendSuccess: " + str(resp))
  
# 初始化微信ApiClient  
wechat = WeChatApiClient(config.appid, config.appsecret)
wechat.on_servererror = lambda resp, *args, **kwargs: logger.error(str(resp.text))
wechat.on_wechaterror = lambda resp, *args, **kwargs: logger.error(str(resp.text))

# 初始化日志
init_log()
logger = logging.getLogger("shike")

session = Session()