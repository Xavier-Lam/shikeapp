# -*- coding: utf-8 -*-

import logging

import config

__all__ = ["init_log", "logger"]

class SubFileHandler(logging.Handler):
    def __init__(self, filename_pattern, mode="a", name_map=None, 
        encoding=None, delay=0):
        logging.Handler.__init__(self)
        self.handlers = {}

        if name_map:
            self.name_map = name_map
        self.filename_pattern = filename_pattern
        self.mode = mode
        self.encoding = encoding
        self.delay = delay

    def emit(self, record):
        name = record.name
        handler = self.handlers.get(name)
        if not handler:
            filename = self.filename_pattern\
                .format(name=self.name_map(name) if self.name_map else name)
            handler = logging.FileHandler(filename, self.mode, 
                self.encoding, self.delay)
            handler.setLevel(self.level)
            handler.setFormatter(self.formatter)
            self.handlers[name] = handler
        handler.emit(record)

def init_log():
    formatter = logging.Formatter("[%(levelname)s] %(name)-12s %(asctime)s %(message)s", 
        "%m-%d %H:%M:%S")

    # 一般日志
    logger = logging.getLogger("shike.main")
    ch = logging.FileHandler(config.log_prefix + "shike.txt", "a")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger = logging.getLogger("shike")
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
    # 子日志
    ch = SubFileHandler(config.log_prefix + "userlog_{name}.txt", "a", lambda x: x[6:])
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # 统计日志
    stat_logger = logging.getLogger("stat")
    ch = logging.FileHandler("stat.txt", "a")
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    stat_logger.addHandler(ch)

# def init_log(uid):
#     """日志配置"""
#     # # 按用户文件处理器
#     # ch = logging.FileHandler(config.log_prefix + "log" + str(uid) + ".txt", "w")
#     # ch.setLevel(logging.INFO)
#     # ch.setFormatter(formatter)
#     # logger.addHandler(ch)