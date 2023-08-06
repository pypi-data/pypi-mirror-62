#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/2/29

POC-S自实现的DSNLog功能

api: http://www.xxxx.cn:88/api/?token={api_key}&type={web|dns}&filter=

param:
    - api_key: 你搭建dnslog时候要求你输入的api_key
    - type 可选值有web和dns
    - filter 过滤出请求的随机子域名
return:
    {"status": "success", "data": {}}
"""

import random
import requests
import time
from string import ascii_lowercase
import sys, json
sys.path.append('../')
from lib.core.data import logger, paths
paths.CONFIG_PATH = "../toolkit.conf"
from lib.utils.config import ConfigFileParser

API_KEY = ConfigFileParser()._get_option("dnslog", "api_key")
DNS_DOMAIN = ConfigFileParser()._get_option("dnslog", "dns_domain")
DNS_IP = ConfigFileParser()._get_option("dnslog", "dns_ip")
API_PORT = ConfigFileParser()._get_option("dnslog", "api_port")


class Dnslog:
    def __init__(self, custom="vuln"):
        self.dns_domain = DNS_DOMAIN
        self.dns_ip = DNS_IP
        self.api_key = API_KEY
        self.api_port = API_PORT
        self.random = ''.join([random.choice(ascii_lowercase) for _ in range(10)])
        self.custom_domain = '%s.%s.%s' % (self.random, custom, self.dns_domain)

    def getDomain(self, custom='poc'):
        """获取随机域名
        """
        return self.custom_domain

    def getCommand(self, type="dns"):
        if type == "dns":
            return "nslookup %s %s" % (self.custom_domain, self.dns_ip)
        elif type == "web":
            return "wget http://%s:88/weblog/%s" % (self.dns_domain, self.random)

    def getDnsRecord(self, delay=2):
        time.sleep(delay)
        api_base = 'http://{0}:{1}/api/?token={2}&type=dns&filter={3}'.format(self.dns_domain,
                                                                              self.api_port,
                                                                              self.api_key,
                                                                              self.custom_domain)
        return requests.get(api_base).content

    def getHttpRecord(self, delay=2):
        time.sleep(delay)
        api_base = 'http://{0}:{1}/api/?token={2}&type=web&filter={3}'.format(self.dns_domain,
                                                                              self.api_port,
                                                                              self.api_key,
                                                                              self.custom_domain)
        return requests.get(api_base).content

    def verifyDNS(self, delay=2):
        try:
            res = json.loads(self.getDnsRecord(delay))
            if res["data"]: return True
        except:
            return False
        return False

    def verifyHTTP(self, delay=2):
        try:
            res = json.loads(self.getHttpRecord(delay))
            if res["data"]: return True
        except:
            return False
        return False


if __name__ == "__main__":
    import subprocess

    c = Dnslog("test")
    domain = c.getDomain()
    command = c.getCommand("dns")
    print(command)
    web_command = c.getCommand("web")
    print(web_command)
    # subprocess.call(command, shell=True)
    # res = c.verifyDNS(3)
    # print(res)
