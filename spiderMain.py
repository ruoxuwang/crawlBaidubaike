# -*- coding:utf-8 -*-
from urllib import unquote
import html_downloader
import html_outputer
import html_parser
import url_manager
import time
# import urllib
import urllib2

BAIDUBAIKE_URL_BASE = 'http://baike.baidu.com/item/'
CRAWL_COUNT = 10000
EACH_CRAWL = 20


class SpiderMain(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.urls = url_manager.UrlManager()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                count += 1
                if count % EACH_CRAWL == 0:
                    # time.sleep(0.2)
                    self.downloader.change_proxy()
                url = self.urls.get_new_url()
                print '%s crawl %d : %s' % (time.ctime(), count, url)
                html_content = self.downloader.download(url)
                urls, data = self.parser.parse(url, html_content)

                if html_content is None:    # url error
                    print 'url error'
                    continue
                invalid_user = 0
                while urls is None and data is None and invalid_user < 5:  # invalid user
                    print 'invalid user'
                    self.downloader.change_proxy(invalid=1)
                    html_content = self.downloader.download(url)
                    urls, data = self.parser.parse(url, html_content)
                if invalid_user == 5:   # maybe url error
                    print 'maybe url error'
                    self.urls.save_invalid_url(url)
                    continue
                self.urls.add_new_urls(urls)
                self.outputer.output_txt(data)

            except Exception as e:
                print("crawl failed")
                print e
                # self.urls.save_urls()
            except KeyboardInterrupt as e:
                print("KeyboardInterrupt")
                # print e
                self.urls.save_urls()
            except BaseException as e:
                print("BaseException")
                # print e
                self.urls.save_urls()
                exit()
        self.outputer.output_html()

    def crawlByEntityName(self):
        file_path = 'D:\Entity linkage\cndbpedia\cndbpediaDumpEntityName.txt'
        f = open(file_path, 'r')
        for line in f:
            url = BAIDUBAIKE_URL_BASE + line.decode('utf-8')
            # crawUrl(url)
            html_content = self.downloader.download(url)
            urls, data = self.parser.parse(url, html_content)
            self.outputer.output_txt(data)
        f.close()


if __name__ == '__main__':
    root_url = "http://baike.baidu.com/item/hello"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
