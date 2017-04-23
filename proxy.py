# -*- coding:utf-8 -*-  
import urllib2
import urllib
import random
import requests
from bs4 import BeautifulSoup
import re
import time

CHECK_TIMTOUT = 0.1
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'


def proxyByUrllib2():
    # iplist = ['183.185.0.47:9797','124.238.236.109:80','115.85.233.94:80']
    iplist = ['190.203.164.217:8080', '60.249.19.50:8080', '220.248.126.58:8080', '218.92.145.40:8080',
              '112.249.41.57:8888']

    url = 'http://www.whatismyip.com.tw'
    for ip in iplist:
        proxy_support = urllib2.ProxyHandler({'http': ip})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        try:
            res = urllib2.urlopen(url)
            html = res.read().decode('utf-8')
            # print(html)
            print ip
        except urllib2.HTTPError as e:
            print e.code
            print e.reason
            continue


def proxyByRequests():
    proxies = {'https': '183.185.0.47:9797', 'https': '124.238.236.109:80', 'https': '115.85.233.94:80'}
    url = 'http://www.whatismyip.com.tw'
    r = requests.get(url, proxies=proxies)
    print r.text


# 如果爬取的页面IP:port 是<tr><td>...</td></tr>这种形式
def formatTable(html_doc, ipPos=1, portPos=2):
    print u'解析table，位置是' + str(ipPos) + ' ' + str(portPos)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf8')
    proxies = []
    trs = soup.findAll('tr')
    # print(u'formatTable： 抓到'+len(trs)+u'行trs')
    for i in range(1, len(trs)):
        tds = trs[i].findAll("td")
        if (len(tds) >= 2):
            ip_port = tds[ipPos].get_text().strip() + ':' + tds[portPos].get_text().strip()
            proxies.append(ip_port)
    print('formatTable end')
    print u'测试formatTable 得到的proxise ' + proxies[0]
    print u'获取ip数目：' + str(len(proxies))
    return proxies


# 如果爬取的页面IP:port 是<ul><li>...</li></ul>这种形式
def formatUlLi(html_doc, ipPos=1, portPos=2):
    print u'解析formatUlLi，位置是' + str(ipPos) + ' ' + str(portPos)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf8')
    proxies = []
    uls = soup.findAll('ul', class_='l2')
    print(u'formatUlLi： 抓到' + len(uls) + u'行ul class=l2')
    for i in range(1, len(uls)):
        lis = uls[i].findAll("li")
        ip_port = lis[ipPos].get_text() + ':' + lis[portPos].get_text()
        proxies.append(ip_port)
    print('formatUlLi end')
    return proxies


# 如果爬取的页面IP:port直接在文本中
def formatText(html_doc, ipPos=None, portPos=None):
    print u'解析text类型'
    proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}', html_doc)
    print('formatText end')
    print u'测试poxise ' + proxies[0]
    print u'获取ip数目： ' + str(len(proxies))
    return proxies


# 用urllib2解析url
def getHtmlDoc(url, User_Agent, cookie=None):
    # ipList = ['61.188.24.137:808','61.188.24.137:808','171.38.142.148:8123','218.92.145.40:8080','177.114.80.45:8080']
    # checkProxies('http://quote.stockstar.com/stock',ipList)
    # proxy_support = urllib2.ProxyHandler({'http':random.choice(ipList)})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)

    header = {'User-Agent': User_Agent}
    if cookie is not None:
        header['Cookie'] = cookie
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    html_doc = res.read()
    if res.getcode() != 200:
        print 'html_doc 响应状态不是200'
    print('getHtmlDoc end')
    return html_doc


# 用Requests解析url，简洁
def htmlDocByRequests(url, headers):
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print 'htmlDocByRequests : r.status_code = %d' % r.status_code
        return None
    print 'htmlDocByRequests end'
    return r.text


# 验证IP的有效性
def checkProxies(proxies):
    url = "http://quote.stockstar.com/"
    # print u'共解析到%d个proxies'%len(proxies)
    valid_proxies = []
    for i in range(len(proxies)):
        proxy = proxies[i]
        if (i + 1) % 100 == 0:
            print u'\t已查' + str(i + 1) + u'个'
        if (i + 1) % 1000 == 0:
            time.sleep(2)  # 防止被用来验证proxy有效性的网址禁了
        # print str(i) + u'cheking : ' + proxy
        try:
            r = requests.get(url, proxies={'http': 'http://' + proxy}, timeout=CHECK_TIMTOUT)
            # print r.status_code
            if r.status_code == 200:
                valid_proxies.append(proxy)
        except Exception as e:
            # if(r.status_code != 200):
            # print r.status_code + ':' + url + u'无效'
            print e

    f = open('proxies.txt', 'a')
    for i in range(len(valid_proxies)):
        proxy = valid_proxies[i]
        f.write(proxy.encode('utf-8') + '\n')
        print str(i + 1) + u': ' + proxy
    f.close()

    print u'checkProxy结束，可以使用共有： ' + str(len(valid_proxies))
    return valid_proxies


# 将代理以及需要的参数存在文件中
def saveProxyWebsite(url, User_Agent, formatFuc, ipPos=None, portPos=None):
    '''
	format: 解析网对应页用到的函数
	ipPos: ip在table或者ul中的位置，函数formatFuc中的参数
	portPos: port在table或者换ul中的位置，函数formatFuc中的参数
	'''

    f = open('proxyWebsite.txt', 'a')
    words = url.encode('utf-8') + '\t' + User_Agent.encode('utf-8') + '\t' + formatFuc.encode('utf-8')
    if ipPos is None and portPos is None:
        words = words + '\n'
    else:
        words = words + '\t' + str(ipPos).encode('utf-8') + '\t' + str(portPos).encode('utf-8') + '\n'
    f.write(words)
    f.close()


def getProxy(url, User_Agent, formatFuc, ipPos=None, portPos=None):
    valid_proxies = []
    proxies = []
    try:
        print u'从 ' + url + u' 爬取proxies...'
        html_doc = htmlDocByRequests(url, {'User-Agent': User_Agent})
        if html_doc is None:
            print 'html_doc is None'
            return None
        if formatFuc == 'formatTable':
            proxies = formatTable(html_doc, ipPos, portPos)
        elif formatFuc == 'formatUlLi':
            proxies = formatUlLi(html_doc, ipPos, portPos)
        elif formatFuc == 'formatText':
            proxies = formatText(html_doc, ipPos, portPos)
        else:
            print u'没有这种模式'
        print  u'验证从 ' + url + u' 爬取到的proxies'
        valid_proxies = checkProxies(proxies)
    except Exception as e:
        print "getProxies Exception"
        if len(proxies) == 0:
            print url + u" 中没有爬取到proxies..."
    print u'从 ' + url + u' 爬取proxies结束\n'
    return valid_proxies


# 解析每一行文件，解析后获取有效的proxy
def getProxies(line):
    parts = line.strip('\n').split('\t')
    url, User_Agent, formatFuc, ipPos, portPos = str(parts[0].decode('utf-8')), str(parts[1].decode('utf-8')), str(
        parts[2].decode('utf-8')), None, None
    # print u'param is:'
    # print type(url)
    # print '\turl=%s\n\tUser_Agent=%s\n\tformatFuc=%s'%(url,User_Agent,formatFuc)
    if len(parts) == 5:
        ipPos = int(parts[3].decode('utf-8'))
        portPos = int(parts[4].decode('utf-8'))
    # print '\tipPos=%d\n\tportPos=%d'%(ipPos,portPos)

    return getProxy(url, User_Agent, formatFuc, ipPos, portPos)


# 从代理文件proxyWebsite.txt中读取代理IP的网址，User_Agent等等，并对每一行进行解析
def updateProxies():
    f1 = open('proxies.txt', 'w')
    f1.close()  # 主要是清空文件，会在checkProxy时候重新存入里面
    f = open('proxyWebsite.txt', 'r')

    count = 0  # 总数量
    valid_proxies = []
    for line in f:
        valid_proxies = getProxies(line)
        if valid_proxies != None:
            count = count + len(valid_proxies)
    print('-------------------------------------------------')
    print u'本次共爬取%d个有效代理' % count
    f.close()
    return valid_proxies


if __name__ == '__main__':
    updateProxies()

    '''
	#   保存能获取到的proxy网址
	User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	saveProxyWebsite('http://www.youdaili.net/Daili/http/36723.html',User_Agent,'formatText')
	saveProxyWebsite('http://ip.qqroom.cn/detail/2284.html',User_Agent,'formatText')
	saveProxyWebsite('http://www.httpsdaili.com/' ,User_Agent,'formatTable',0,1)
	saveProxyWebsite('http://www.kuaidaili.com/',User_Agent,'formatTable',0,1)
	saveProxyWebsite('http://www.ip3366.net/',User_Agent,'formatTable',0,1)
	saveProxyWebsite('http://ip.qqroom.cn/detail/2284.html',User_Agent,'formatText')
	saveProxyWebsite('http://www.xicidaili.com/nn/1','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0','formatTable',1,2)
	'''

    '''
	url = 'http://www.xicidaili.com/nn/1'
	User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
	html_doc = getHtmlDoc(url,User_Agent)
	proxies = formatTable(html_doc)	

	url = 'http://ip.qqroom.cn/detail/2284.html'
	User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	html_doc = getHtmlDoc(url,User_Agent)
	proxies = formatText(html_doc)
	'''

    # 出现302错误跟cookie可能有关
    # url = 'http://www.data5u.com/'
    # User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    # cookie = 'ASPSESSIONIDQARRTAQD=LNEAPJJBACOKJIAMMJJBFOKD; Hm_lvt_2c6f6b890eb59b44e4e4c2ac2a18d1f2=1492388862; Hm_lpvt_2c6f6b890eb59b44e4e4c2ac2a18d1f2=1492388862; UM_distinctid=15b794ed97a102-0c0aa8ec6012c1-4d015463-100200-15b794ed97b12b; CNZZDATA1000412828=2054788486-1492383567-null%7C1492383567'
    # html_doc = getHtmlDoc(url,User_Agent)
    # proxies = formatUlLi(html_doc,1,2)

    '''
	# 有页码
	url = 'http://www.ip3366.net/'
	User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	html_doc = getHtmlDoc(url,User_Agent)
	proxies = formatTable(html_doc,0,1)	
	'''

    '''
	# 有页码
	url = 'http://www.kuaidaili.com/'
	User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	html_doc = getHtmlDoc(url,User_Agent)
	proxies = formatTable(html_doc,0,1)	
	'''

    '''
	url = 'http://www.httpsdaili.com/' 
	User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	html_doc = getHtmlDoc(url,User_Agent)
	proxies = formatTable(html_doc,0,1)
	'''

    '''
	#是链接形式
	url = 'http://www.youdaili.net/Daili/http/36723.html'
	url = 'http://ip.qqroom.cn/detail/2284.html'
	User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	# html_doc = getHtmlDoc(url,User_Agent)
	html_doc = htmlDocByRequests(url,{'User_Agent':User_Agent})	
	proxies = formatText(html_doc)
	valid_proxies = checkProxies(proxies)
	'''
