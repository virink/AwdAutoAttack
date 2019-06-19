#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exps.backdoor import *
from exps.agent import *
from exps.webshell import *

import base64


def b64e(c):
    if isinstance(c, str):
        c = bytes(c, 'utf-8')
    return str(base64.b64encode(c), 'utf-8')


def exp_eval_b64e(data):
    return "eval(base64_decode('%s));" % b64e(data)


def exp_upload_rce():
    pass
