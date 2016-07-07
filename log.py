# -*- coding: utf-8 -*-

import logging

import config

__all__ = ["init_log", "logger"]

def init_log():
    logger = logging.getLogger("shike")
    
    formatter = logging.Formatter("[%(levelname)s] %(name)-12s %(asctime)s %(message)s", 
        "%m-%d %H:%M:%S")
    # 关键异常处理器
    ch = logging.FileHandler(config.log_prefix + "errlog.txt", "a")
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # 控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # 调试异常处理器
    ch = logging.FileHandler(config.log_prefix + "debuglog.txt", "w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# def init_log(uid):
#     """日志配置"""
#     # # 按用户文件处理器
#     # ch = logging.FileHandler(config.log_prefix + "log" + str(uid) + ".txt", "w")
#     # ch.setLevel(logging.INFO)
#     # ch.setFormatter(formatter)
#     # logger.addHandler(ch)