# -*- coding:utf8 -*-
import random
import requests
import thread

import proxy

BAIDUBAIKE_ERROR_URL = 'http://baike.baidu.com/error.html'
BAIDUBAIKE_ROOT_URL = 'https://baike.baidu.com/'

class HtmlDownloader(object):
    def __init__(self):
        self.proxies = self.load_proxies()
        self.currentProxy = None
        self.change_proxy()

    def change_proxy(self, invalid=0):
        if invalid == 1:
            print self.currentProxy + 'invalid'
            self.proxies.remove(self.currentProxy)
        if len(self.proxies) < 100:
            thread.start_new_thread(proxy.updateProxies())
        if len(self.proxies) < 20:
            self.proxies = self.load_proxies()
        if len(self.proxies) == 0:
            self.proxies = self.load_proxies()
        self.currentProxy = random.choice(self.proxies)
        print u'change proxy***********proxy is : ' + self.currentProxy

    def download(self, url):
        if url is None:
            return None
        count = 0
        while True:
            try:
                # s = requests.session()
                #   r = requests.get(url, timeout=2)
                r = requests.get(url, proxies={'http': 'http://' + self.currentProxy}, timeout=2)
                if r.url == BAIDUBAIKE_ERROR_URL or r.url == BAIDUBAIKE_ROOT_URL:
                    print 'r.url = ' + r.url
                    return None
                html_doc = r.text
                # s.cookies.clear()
                if r.status_code == 200:
                    break
                else:
                    count += 1
            except requests.RequestException as e:
                print e
                count += 1
            except Exception as e:
                print e
                count += 1
            if count == 5:
                self.change_proxy(invalid=1)
                count = 0
        return html_doc

    @staticmethod
    def load_proxies():
        # proxies = proxy.updateProxies()
        proxies = []
        f = open('proxies.txt', 'r')
        for line in f:
            proxies.append(line.strip())
        f.close()
        if len(proxies) == 0:
            print 'len(proxies) == 0'
            proxy.updateProxies()
        return proxies
