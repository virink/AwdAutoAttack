#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging

LOG_FILE = './logs/attack.log'
LOG_LEVEL = logging.INFO
LOG_FMT = '[*] [%(asctime)s] - %(levelname)s %(message)s'

RSA_AGENT = "http://127.0.0.1:8085/agent.php"

RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCEYOn06u1zVIW44sMXC/rTDgqB3ercy1A2pteJ1LsAesPRgglI
ysPXaGpWrEgtY19tGTC+rnr15bmcIKFKopNji2A7n6W7okhWnmclcUIlYVQUFwKg
jfiPnaM09gpEZNDaRTiryKyI66XgXP0Wt2nsYD2YDNYL/Iz32zzQEz7irwIDAQAB
AoGBAIKSHPHIr0FsgyFj+c3HsTVvygliXIA/wfTGCB8ZRwIoFPGXc5Tq+tSDVy/6
ao7qT3uKtzu9WeclGjjXLoAxb3HtAOabLCFKVBU2Trbu+C3/wEvhDvBuJY34J8Kk
+LjZfTDKuzR4LO5+fb5tT9h0qYJw9Pg6rEbhJQyhEzWGNI/hAkEA8yI+WAitGcPi
SUAmtQIzK2PJkAqbAt23GbkH7N16BIhmO/dqShOV3E3SpHFarYXjJvNa61eHt/pI
rC6AChhe1wJBAItiQlSt8xAgqEgtwyBmlCeLu7rwsnnu5Ol/MJ72gwDTDcY3JPum
QNmUDlepHuSZ2QqPpFAvDzx0Z6sv9vSm1+kCQGkGw9OXe98DZP6rfYz3dE8r/egB
DNECIZQ0/51sVscafL8us3VoXHYcEAAFD1yh12v996pt1yy8KyRlud2ihWUCQGyj
ASAPFEuVqJPZVySBzyejeYaS5Ai1ciWrxLGhYSnbVfkQMfsR8amkBCm+3x097DSX
EHKOu0lbURHUKJ83C0ECQEWGQ6knDEWhTSsvlX3IUWdYgWRc6bbQhaYYkNQMt17F
0QqVqLc8RbsTnHPrS0DT7epuBmNh0TtzG4h93wYXuBs=
-----END RSA PRIVATE KEY-----""".strip()

FLAG_PATTERN = re.compile(r'((flag)?({(.*?)}))', re.I | re.M)
