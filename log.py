# -*- coding: utf-8 -*-

import logging

import config

def init_log(uid):
    """日志配置"""
    log_format = '[%(levelname)s] %(name)-12s %(asctime)s %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt='%m-%d %H:%M:%S',
    )
    logger = logging.getLogger("")
    formatter = logging.Formatter(log_format)
    ch = logging.FileHandler(config.log_prefix + "log" + str(uid) + ".txt", "w")
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)