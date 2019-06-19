<?php
class Rsa
{
    private static $PRIVATE_KEY = '-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCy/QLPIu6m9Le5a1Jm8lYeHgiJbDEux/1BZuGwbDlXG68ph/Cs
aAHr7QNEoB0+mmo7Caimred973ikcKZArahSQzKUIcEj3LXFT56lxo/Ur7/lJvAD
OQgZcfTOAxgeXyaflX0pEcosXTzJ7+9BBoG/zY1k7r9Fnz9EpcNoHd4BdQIDAQAB
AoGAVTldbg1e/wYEuPfd+4Cl+p8oR27JmFHHR63aBmvxfYWECM1ejmjTiWeIJ9Pp
ONbDgCrgL8UcNX2hvwKYVrGZNA1l+s7jzp/gmnoXaNV2bPHS5lxLhVZZvNyHZRKi
9eIxeZo/mMXNGXO25kqdUvvKUFZL6gAT6FvQvHZFordTnP0CQQDrHZgEq9aXmgc5
otWmia8g1vGPYWffxT/7IYzr9J+et3AppGutk0H13U0DFIO/bh7cHPSHltLOO3UH
Umwe6CfnAkEAwuMctVt7Mo7D6b/mseCisnmKz7JcsGKQTOS3GhuwZEcm/XI/2GGu
F0Sg74xnieTwkpF5MHbESFjGj9RdjlXwQwJACpciqdMzr1B40tfK192Lzebgqpyw
mRvBbgZs2pQCPJv2qWmGkCL57aEyPtlFtfG34iJLwW/BvxhehR3pUNsUMQJAG8Mu
u8ckbbdYwVvNCVnu023tEFlgSuA/njSWwOlg32gjbcdwwOppWnc0VeuydDpg6wA+
O2Ev5P6Aisy95yDm8QJBAJmVZIXbA8/ERVD4coaCGsbX+UC6055SKFJLNVGIGyz2
EbCiGTHdeDN46oNHYytie2VuU/WEb14mlTl9pF45JF4=
-----END RSA PRIVATE KEY-----';

    private static function getPrivateKey()
    {
        return openssl_pkey_get_private(self::$PRIVATE_KEY);
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
        return ($res) ? $res : null;
    }
}

$rsa = new Rsa();