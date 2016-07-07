# -*- coding: utf-8 -*-

import json
import sys

import requests

__python_version__ = sys.version[0]

class WeChatApiClient(object):
    """一个微信apiclient"""
    __baseaddr__ = "https://api.weixin.qq.com"
    __prefix__ = "/cgi-bin"

    __accesstoken = None
    appid = None
    appsecret = None
    
    on_wechaterror = None
    on_wechatgranted = None
    on_servererror = None

    def __init__(self, appid, appsecret, token=None):
        self.appid = appid
        self.appsecret = appsecret
        self.__accesstoken = token

    def get(self, url, **kwargs):
        kwargs["method"] = "get"
        kwargs = self._handlekwargs(url, kwargs)
        resp = self.requests(**kwargs)
        return self._onresponse(resp)
        
    def get_raw(self, url, **kwargs):
        kwargs["method"] = "get"
        kwargs = self._handlekwargs(url, kwargs)
        return self.requests(**kwargs)
        
    def post(self, url, **kwargs):
        kwargs["method"] = "post"
        kwargs = self._handlekwargs(url, kwargs)
        resp = self.requests(**kwargs)
        return self._onresponse(resp)
        
    def grant(self):
        params = dict(
            grant_type="client_credential",
            appid=self.appid,
            secret=self.appsecret
        )
        resp = self.requests("get", "/token", 
            params=params)
        try:
            json = resp.json()
            code = json.get("errcode")
            if code:
                if self.on_wechaterror:
                    self.on_wechaterror(resp, code)
            else:
                self.__accesstoken = json["access_token"]
                expires_in = json.get("expires_in") or 7200
                # 更新外部token
                if self.on_wechatgranted:
                    self.on_wechatgranted(resp, self.__accesstoken, expires_in)
                self._update_accesstoken(self.__accesstoken, expires_in)
        except Exception as e:
            if self.on_servererror:
                self.on_servererror(resp, code, e)
        return self.__accesstoken

    def requests(self, method, url, *args, **kwargs):
        url = self.__baseaddr__.rstrip("/") + self.__prefix__ + url
        if "json" in kwargs:
            # 解决中文被转码问题
            headers = kwargs.get("headers") or {}
            headers["Content-Type"] = "application/json; charset=UTF-8"
            headers["Encoding"] = "utf-8"
            kwargs["headers"] = headers
            kwargs["data"] = json.dumps(kwargs["json"], ensure_ascii=False)
            if __python_version__ == "3":
                kwargs["data"] = kwargs["data"].encode("utf-8")
            del kwargs["json"]
        try:
            rv = getattr(requests, method)(url, *args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            # 连接错误 生成一个空响应
            rv = requests.Response()
        return rv

    @property
    def accesstoken(self):
        token = self.__accesstoken
        if token:
            return token
        else:
            return self.grant()

    def _onresponse(self, resp):
        """处理一般返回"""
        try:
            json = resp.json()
            code = int(json.get("errcode")) or 0
            rv = (json, code)
            if code:
                # 处理异常
                if self.on_wechaterror:
                    self.wechat_error(resp, code)
                resp = self._handleerror(json, code)
                if resp:
                    json = resp.json()
                    code = int(json.get("errcode")) or 0
                    if code:
                        if self.on_wechaterror:
                            self.wechat_error(resp, code)
                    else:
                        # 成功处理
                        rv = (json, code)
            return rv
        except Exception as e:
            if self.on_servererror:
                self.on_servererror(resp, code, e)
            return {}, -2

    def _handleerror(self, resp_json, code):
        """在返回异常后再次请求"""
        if code in [40001, 40014, 42001, 42007]:
            # accesstoken 失效
            self.grant()
            self.__lastrequest["params"]["access_token"] = self.accesstoken
            return self.requests(**self.__lastrequest)
        else:
            pass
            
    def _handlekwargs(self, url, kwargs):
        kwargs["url"] = url
        params = kwargs.get("params") or {}
        params["access_token"] = self.accesstoken
        kwargs["params"] = params
        self.__lastrequest = kwargs
        return kwargs
        
    def _update_accesstoken(self, value, expires_in=None):
        """更新accesstoken"""
        return value

def post_template_message(client, touser, template_id, url="", **kwargs):
    content = dict()
    for key, value in kwargs.items():
        content[key] = dict(
            value=str(value),
            color="#333333"
        )
    data = dict(
        touser=touser,
        template_id=template_id,
        url=url,
        data=content
    )
    return client.post("/message/template/send", json=data)