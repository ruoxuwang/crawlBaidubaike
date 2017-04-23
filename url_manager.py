# -*- coding:utf-8 -*-

class UrlManager(object):
    def __init__(self):
        self.new_url_list = set()
        self.old_url_list = set()
        self.load_urls()

    def add_new_url(self, url):
        # pass
        if url is None:
            return
        if url not in self.new_url_list and url not in self.old_url_list:
            self.new_url_list.add(url)

    def has_new_url(self):
        return len(self.new_url_list) != 0

    def get_new_url(self):
        url = self.new_url_list.pop()
        self.old_url_list.add(url)
        return url

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    @staticmethod
    def _save_url(file_name, url_list):
        f = open(file_name, 'w')
        for url in url_list:
            f.write(url.encode('utf-8') + '\n')
        f.close()

    def save_urls(self):
        self._save_url('new_url_list.txt', self.new_url_list)
        self._save_url('old_url_list.txt', self.old_url_list)

    def _load_urls(self, file_name):
        f = open(file_name, 'r')
        for line in f:
            url = line.decode('utf-8').strip()
            if len(url) < 3:
                print u'没有'
                break
            self.new_url_list.add(url)
        f.close()

    def load_urls(self):
        self._load_urls('new_url_list.txt')
        self._load_urls('old_url_list.txt')

    def save_invalid_url(self, url):
        f = open('invalid_url_list.txt', 'a')
        f.write(url.encode('utf-8') + '\n')
        f.close()