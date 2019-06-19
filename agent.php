<?php

class RSA
{
    private static $PUBLIC_KEY = <<<EOF
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCEYOn06u1zVIW44sMXC/rTDgqB
3ercy1A2pteJ1LsAesPRgglIysPXaGpWrEgtY19tGTC+rnr15bmcIKFKopNji2A7
n6W7okhWnmclcUIlYVQUFwKgjfiPnaM09gpEZNDaRTiryKyI66XgXP0Wt2nsYD2Y
DNYL/Iz32zzQEz7irwIDAQAB
-----END PUBLIC KEY-----
EOF;

    private static $PRIVATE_KEY = <<<EOF
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCEYOn06u1zVIW44sMXC/rTDgqB3ercy1A2pteJ1LsAesPRgglI
ysPXaGpWrEgtY19tGTC+rnr15bmcIKFKopNji2A7n6W7okhWnmclcUIlYVQUFwKg
jfiPnaM09gpEZNDaRTiryKyI66XgXP0Wt2nsYD2YDNYL/Iz32zzQEz7irwIDAQAB
AoGBAIKSHPHIr0FsgyFj+c3HsTVvygliXIA/wfTGCB8ZRwIoFPGXc5Tq+tSDVy/6
ao7qT3uKtzu9WeclGjjXLoAxb3HtAOabLCFKVBU2Trbu+C3/wEvhDvBuJY34J8Kk
+LjZfTDKuzR4LO5+fb5tT9h0qYJw9Pg6rEbhJQyhEzWGNI/hAkEA8yI+WAitGcPi
SUAmtQIzK2PJkAqbAt23GbkH7N16BIhmO/dqShOV3E3SpHFarYXjJvNa61eHt/pI
rC6AChhe1wJBAItiQlSt8xAgqEgtwyBmlCeLu7rwsnnu5Ol/MJ72gwDTDcY3JPum
QNmUDlepHuSZ2QqPpFAvDzx0Z6sv9vSm1+kCQGkGw9OXe98DZP6rfYz3dE8r/egB
DNECIZQ0/51sVscafL8us3VoXHYcEAAFD1yh12v996pt1yy8KyRlud2ihWUCQGyj
ASAPFEuVqJPZVySBzyejeYaS5Ai1ciWrxLGhYSnbVfkQMfsR8amkBCm+3x097DSX
EHKOu0lbURHUKJ83C0ECQEWGQ6knDEWhTSsvlX3IUWdYgWRc6bbQhaYYkNQMt17F
0QqVqLc8RbsTnHPrS0DT7epuBmNh0TtzG4h93wYXuBs=
-----END RSA PRIVATE KEY-----
EOF;

    private static function getPrivateKey()
    {
        $ret = openssl_pkey_get_private(self::$PRIVATE_KEY);
        // print_r(openssl_error_string());
        return $ret;
    }
    private static function getPublicKey()
    {
        $ret = openssl_pkey_get_public(self::$PUBLIC_KEY);
        // print_r(openssl_error_string());
        return $ret;
    }
    public static function privateEncrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split($data, 117) as $chunk) {
            openssl_private_encrypt($chunk, $encryptData, self::getPrivateKey());
            $res .= $encryptData;
        }
        return $res ? base64_encode($res) : null;
    }
    public static function publicEncrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split($data, 117) as $chunk) {
            openssl_public_encrypt($chunk, $encryptData, self::getPublicKey());
            $res .= $encryptData;
        }
        return $res ? base64_encode($res) : null;
    }

    public static function privateDecrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split(base64_decode($data), 128) as $chunk) {
            openssl_private_decrypt($chunk, $decryptData, self::getPrivateKey());
            $res .= $decryptData;
        }
        return $res ? $res : null;
    }

    public static function publicDecrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split(base64_decode($data), 128) as $chunk) {
            openssl_public_decrypt($chunk, $decryptData, self::getPublicKey());
            $res .= $decryptData;
        }
        return $res;
    }
}


$test = new RSA();

$encrypt = isset($_GET['encrypt']);
$data = file_get_contents("php://input");
if ($encrypt == 1) {
    $ret = $test->privateEncrypt($data);
} else {
    $ret = $test->privateDecrypt($data);
}
print_r($ret);
