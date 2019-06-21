<?php

error_reporting(0);

define("WEBROOT", $_SERVER['DOCUMENT_ROOT']);
define("LOGDIR", "_logs");

class FlowLog
{
    public function __construct($ips = [], $forward = false)
    {
        $this->done = 0;
        $this->flow = array();
        $this->log_path = WEBROOT . '/' . LOGDIR . '/';
        mkdir($this->log_path, 0777, 1);
        $this->Flow();
    }

    private function Flow()
    {
        foreach ($_SERVER as $key => $value) {
            if (stripos("HTTP_", $key)) {
                $this->flow['header'][ucwords(strtolower($key))] = $_SERVER["HTTP_" . $key];
            }
        }
        $this->flow['method'] = $_SERVER['REQUEST_METHOD'];
        $this->flow['protocol'] = $_SERVER['SERVER_PROTOCOL'];
        $this->flow['time'] = date('Y-m-d H:i:s', $_SERVER['REQUEST_TIME']);
        isset($_SERVER['CONTENT_TYPE']) && $this->flow['ctype'] = @$_SERVER['CONTENT_TYPE'];
        $this->flow['ip'] = array(
            'REMOTE_ADDR' => @$_SERVER['REMOTE_ADDR'],
            'CLIENT-IP' => @$_SERVER['HTTP_CLIENT_IP'],
            'X-FORWARDED-FOR' => @$_SERVER['HTTP_X_FORWARDED_FOR'],
        );

        /* GetData */
        $this->flow['uri'] = $_SERVER['REQUEST_URI'];
        $this->flow['get'] = print_r(parse_url($_SERVER['REQUEST_URI']), 1);

        /* PostData */
        if (strtolower($_SERVER['CONTENT_TYPE']) != 'multipart/form-data') {
            $this->flow['post'] = file_get_contents('php://input');
        } elseif (isset($_POST) or strtolower($this->flow['method']) == 'post') {
            $this->flow['post'] = print_r($_POST, 1);
        }

        /* File */
        // 还没想好怎么判断大量干扰数据的 webshell
        if (isset($_FILES)) {
            // print_r($_FILES);
            $shelldir = $this->log_path . "/_webshell/";
            @file_exists($shelldir) || @mkdir($shelldir, 0777, 1);
            foreach ($_FILES as $key => $fObj) {
                $tmp = $fObj['tmp_name'];
                $temp = file_get_contents($tmp);
                // 后缀及内容判断，保存并清空可疑內容
                if (preg_match("/pht?p?[3457]?(ml)?/gmi", pathinfo($fObj['file_name'])['extension']) || (ini_get('short_open_tag') && stripos("<?", $temp)) !== flase || stripos("<?=", $temp) !== flase || stripos("<?php", $temp) !== flase || stripos("lauguage=php", $temp) !== flase || stripos("lauguage='php", $temp) !== flase || stripos('lauguage="php', $temp) !== flase) {
                    // 保存小文件到日志
                    $fObj['file_size'] < 10240 && $this->flow['file'][$key]['data'] = $temp;
                    file_put_contents($shelldir . "/" . $fObj['name'] . "_" . md5_file($tmp), $temp);
                    file_put_contents($tmp, "<?php header('404 Not Found', 404);");
                }
                unset($temp);
            }
        }
        // Scan
        foreach ($this->flow as $key => $value) {
            $this->Scan(print_r($value, 1));
        }
    }

    private function Scan($input, $force = 0)
    {
        $pattern = "select|insert|update|delete|and|union|load_file|outfile|dumpfile|sub|hex";
        // ZmxhZw > flag
        $pattern .= "|flag|galf|falg|fgla|gafl|glaf|ZmxhZw";
        $pattern .= "|file_put_contents|fwrite|eval|assert|file:\/\/|fopen|readfile|show_source";
        $pattern .= "|passthru|exec|system|chroot|scandir|chgrp|chown|shell_exec|proc_open|proc_get_status|popen|ini_alter|ini_restore|`|\$\$";
        $pattern .= "|dl|openlog|syslog|readlink|symlink|popepassthru|stream_socket_server|pcntl_exec";
        $pattern .= "|exit|die|php:|include|require";
        // 从 POST or GET 数据搜索大佬的WebShell 密码或者相关特征查杀写马
        $pattern .= "|l3m0n|zhixian";
        if (preg_match_all("/$pattern/i", $input, $matches, PREG_PATTERN_ORDER) && $matches[0][0]) {
            $this->Save($matches[0]);
            return 1;
        }
        return 0;
    }

    private function Save($keyword)
    {
        $data = $this->flow;
        file_put_contents($this->log_path . date("d-h") . ".log", "=====================================\r\n" . "Keyword : " . implode(", ", $keyword) . "\r\n" . print_r($data, true) . "\r\n", FILE_APPEND);
        return 1;
    }
}

header("X-Waf-Defense: AWD");

new FlowLog();
