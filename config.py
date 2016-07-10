# -*- coding: utf-8 -*-

# 请求配置
req_break = 15
success_break = 450
down_break = 300

# 接口参数配置
ver = "1.19"
binding = "64_1"
ua = r"Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1"

# 微信参数配置
appid = "wxc908fb07bc49c284"
appsecret = "121ed8930e99a520e3ff7db796f17031"
got_template = "1__R1cYGbMhB-ucp5cZsRm3pDP92BoTSusTPct7O6pM"
down_template = "PPhNn2FK9kz1bY689FVyCxFdl4BMVSXMVYYX6gsPOpo"

# 程序配置
log_prefix = "logs/"
broker = "sqla+sqlite:///celerydb.data"
backend = "db+sqlite:///celerydb_results.data"
database_str = "sqlite:///data.data"

# 监控配置
monitor_break = 300
alert_num1 = 5
alert_num2 = 150
alert_openid = "oFfv-s7eYZ8n7Z6buxKiMhql7ehE"
alert_template = "tFeAoZZfqm_ova3GBBMIwmsujynWCprddxivFFAyry4"