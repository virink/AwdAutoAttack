#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import re,requests
import logging
from logging import handlers


from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

from config import RSA_PRIVATE_KEY, LOG_FILE, LOG_LEVEL, LOG_FMT,RSA_AGENT

RSA_KEY = RSA.importKey(RSA_PRIVATE_KEY)
cipher = Cipher_pkcs1_v1_5.new(RSA_KEY)
sentinel = Random.new().read(15 + SHA.digest_size)


class Logger(object):

    _debug = False

    def __init__(self, filename, level, fmt):
        fmt = '[*] [%(asctime)s] - %(levelname)s %(message)s'
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(level)
        # Console
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        # File
        th = logging.FileHandler(filename=filename, encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        self.logger.toggleDebug = self.toggleDebug

    def toggleDebug(self):
        if self._debug:
            self.logger.setLevel(LOG_LEVEL)
        else:
            self.logger.setLevel(logging.DEBUG)



log = Logger(
    LOG_FILE,
    level=LOG_LEVEL,
    fmt=LOG_FMT
)
logger = log.logger


def md5(text):
    m = hashlib.md5(text.encode())
    return m.hexdigest()


def b64e(c):
    if not isinstance(c, bytes):
        c = bytes(c, 'utf-8')
    return str(base64.b64encode(c), 'utf-8')


def b64d(c, b=0):
    if not isinstance(c, bytes):
        c = bytes(c, 'utf-8')
    ret = base64.b64decode(c)
    return ret if b else str(ret, 'utf-8')


def _rsa_encrypt(data):
    data_chunk = re.findall(r'.{117}', data)
    ret = b''
    for chunk in data_chunk:
        ret += cipher.encrypt(bytes(chunk, 'utf-8'))
    return b64e(ret)


def _rsa_decrypt(data):
    data = b64d(data, 1)
    # logger.debug("rsa_decrypt")
    # logger.debug("len : %d" % len(data))
    # logger.debug(data)
    ret = []
    for p in range(0, len(data), 128):
        # logger.debug("======= %d - %d ========" % (p, p+128))
        # logger.debug(data[p:p + 128])
        ret.append(str(cipher.decrypt(data[p:p + 128]), 'utf-8'))
        # ret.append(cipher.decrypt(data[p:p + 128], sentinel))
    # logger.debug("===============")
    # logger.debug(ret)
    return str(b''.join(ret), 'utf-8')

def _rsa_agent(data, url=""):
    res = requests.post(RSA_AGENT + url, data=data)
    logger.debug(res.text)
    return res.text

def rsa_encrypt(data):
    # logger.debug('rsa_decrypt')
    # logger.debug(data)
    ret = _rsa_agent(data ,"?encrypt=1")
    # logger.debug(ret)
    return ret

def rsa_decrypt(data):
    # logger.debug('rsa_decrypt')
    # logger.debug(data)
    ret = _rsa_agent(data)
    # logger.debug(ret)
    return ret
    # return _rsa_agent(str(ret, 'utf-8'))
