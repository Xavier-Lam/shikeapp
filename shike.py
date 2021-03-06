# -*- coding: utf-8 -*-

import logging
import re
import time

try:
    import lxml.html
    from lxml.cssselect import CSSSelector
except ImportError:
    class lxml(object):
        html = None
import requests

import config

def getnow():
    return str(int(time.time()*1000))

class ShikeClient(object):
    baseaddr = "http://i.appshike.com"
    ver = config.ver
    ua = config.ua
    binding = config.binding

    def __init__(self, uid, id, idfa):
        self.uid = uid
        self.id = id
        self.idfa = idfa

    def init(self):
        """初始化"""
        # 认证
        self.s = requests.Session()
        resp = self.s.get(self.baseaddr + "/itry/xb_verify", params=dict(
            param=self.id,
            idfa=self.idfa,
            ver=self.ver,
            binding=self.binding
        ))
        # 找到参数r
        if not lxml.html:
            match = re.search(r"btn_bjffffff[^>]+r=(.*)'.+>", resp.text)
        else:
            html = lxml.html.fromstring(resp.text)
            sel = CSSSelector(".btn_bjffffff")
            ele = sel(html)[0]
            match = re.search(r"r=(.*)'", ele.attrib["onclick"])
        if not match:
            self.logger.critical("Init failed!")
            raise Exception("Init failed!")
        token = match.group(1)
        # 转到appList首页
        lasturl = self.baseaddr + "/itry/desktop?r=" + token
        
        resp = self.s.get(lasturl, headers={"User-Agent": self.ua})
        match = re.search(r"taskToken:\s*'(.+?)'", resp.text)
        if not match:
            self.logger.critical("Init failed!")
            raise Exception("Init failed!")
        self.token = match.group(1)

    def load_apps(self):
        """加载app列表"""
        # 获取应用列表
        url = self.baseaddr + "/shike/getAppV1/" + self.token
        rv = []
        try:
            resp = self.s.post(url, data={"r": getnow()}, 
                headers={
                    "User-Agent": self.ua, 
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "http://i.appshike.com",
                    "Referer": self.baseaddr + "/shike/appList"
                })
            if resp.status_code != requests.codes.ok:
                self.logger.error("ServerError: " + resp.text)
            try:
                rv = resp.json()
                self.logger.debug("Success: " + resp.text)
            except:
                self.logger.warning("UnexceptResponse: " + resp.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.warning("ConnectionError: " + str(e))
        except Exception as e:
            self.logger.error("UnexceptError: " + str(e))
        return rv

    def filter_apps(self, data):
        """过滤app"""
        filter_fields = ["name", "file_size_bytes", "order_status_disp", "status", "search_word",
            "appid", "order_id", "down_price", "bundle_id", "process_name"]
        availables = filter(lambda x: (int(x["order_status_disp"]) > 0 and x.get("type_name") and str(x.get("type_name")).strip()) or int(x["status"]) == 0, data)
        availables = map(lambda x: {key: x[key] for key in x if key in filter_fields}, availables)
        availables = list(availables)
        return availables

    def sort_app(self, data, *args):
        """排序app"""
        return data

    def collect_app(self, app):
        """领取任务"""
        bundle_id = app["bundle_id"]
        try:
            self.s.post(self.baseaddr + "/api/write_click_log", data=dict(
                user_id="log_" + bundle_id + "_464_500"
            ))
            resp = self.s.post(self.baseaddr + "/shike/user_click_recordV1", data={
                "pass": bundle_id,
                "type": "app"
            })
            if resp.text != "0":
                self.logger.warning("任务领取失败: " + resp.text)
                return False

            # 任务领取成功 下一步
            detail_url = self.baseaddr + "/shike/appDetailsV1/%s?ds=r0"%bundle_id
            app["detail_url"] = detail_url
            resp = self.s.get(detail_url, headers={"User-Agent": self.ua})
            if not re.search(r'id="copy_key"', resp.text):
                self.logger.warning("进入详情页失败: " + resp.text)
                return False
            
            # 进入详情页成功
            resp = self.s.get(self.baseaddr + "/shike/copy_keywordV1", params={
                "pass": bundle_id,
                "t": getnow()
            })
            if resp.text == "0":
                self.logger.info("领取任务成功! " + str(app.get("name")))
                return True
            else:
                self.logger.warning("复制关键词失败: " + resp.text)
                return False
        except Exception as e:
            self.logger.warning("任务领取失败: " + str(e))
            return False

    def get_app_status(self, app):
        """获取app状态"""
        try:
            resp = self.s.post(self.baseaddr + "/shike/getAppStatusV1/%s"%app["bundle_id"],
                headers={"User-Agent": self.ua})
            data = resp.json()
            self.logger.debug("获取应用状态: " + resp.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.warning("ConnectionError: " + str(e))
        except Exception as e:
            self.logger.error("获取应用状态失败: " + resp.text)
        else:
            flg = data.get("flg")
            if not flg:
                self.logger.warning("获取应用状态失败: " + resp.text)
            return flg
        return ""
        
    @property
    def logger(self):
        return logging.getLogger("shike." + self.uid)