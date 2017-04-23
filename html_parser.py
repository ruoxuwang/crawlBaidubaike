# -*- coding:utf-8 -*-
import re
import urllib2
import urlparse
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parse(self, page_url, html_content):
        if page_url is None or html_content is None:
            return
        soup = BeautifulSoup(html_content, 'html.parser')

        if soup is None:
            print 'soup is none'
            return None, None

        new_data = self._get_new_data(page_url, soup)
        if new_data is None:
            print 'new data is none'
            return None, None

        new_urls = self._get_new_urls(page_url, soup)

        return new_urls, new_data

    @staticmethod
    def _get_new_urls(page_url, soup):
        links = soup.find_all('a', href=re.compile(r'/item/'))
        new_urls = set()
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    @staticmethod
    def _get_new_data(page_url, soup):
        res_data = {'url': page_url}

        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title")
        if title_node is None:
            print 'title_node is none'
            print soup.contents
            return None

        res_data['title'] = title_node.find('h1').get_text()
        if title_node.find('h2') is not None:
            res_data['title'] += title_node.find('h2').get_text()

        if soup.find('div', class_="lemma-summary") is not None:
            res_data['summary'] = soup.find('div', class_="lemma-summary").get_text()

        return res_data

