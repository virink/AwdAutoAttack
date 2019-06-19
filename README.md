# AutoAttack Framework

## 用法

1. 本地搭建 PHP 及环境
   - PHP
   - openssl - rsa
   - 放入 agent.php
   - 修改 config.py 的配置
2. 安装 python 相关依赖
3. 添加 Bin 文件数据
4. 修改并运行 main.py

## TODO

**auto.py**

- 导入 main.py 的函数
- 自动化运行
  - 定时任务
  - while and sleep ?

## 说明

**mix.py**

- NormalRequest 正常流量请求
- MixRequest    混淆流量请求

**config.py**

- LOG_FILE            日志路径
- LOG_LEVEL           logging.INFO
- LOG_FMT             '[*] [%(asctime)s] - %(levelname)s %(message)s'
- RSA_AGENT           "http://127.0.0.1:8085/agent.php"
- RSA_PRIVATE_KEY     RSA 私钥
- FLAG_PATTERN        flag 匹配正则模型

**common.py**

- 日志
- RSA 加密解密函数
  - 辣鸡 Py 毁我青春
  - 用来 PHP Agent 加解密
- 其他通用函数

**exps/*.py**

一些 payload

**shells/*.php**

shell 模板及生成脚本

**logs**

日志

**tests**

测试环境
