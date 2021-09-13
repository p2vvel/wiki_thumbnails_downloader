from unittest import TestCase

from wiki.main import ArticleException, WikiArticle

from .links import *

import requests


def get_links(amount=10):
    '''returns some links to wiki articles'''
    return (seasons_links[:amount] + drivers_links[:amount] +
            races_links[:amount] + circuits_links[:amount] +
            constructors_links[:amount])


class AllTests(TestCase):
    def test_seasons(self):
        '''Checks if names are correctly scrapped from wikipedia links by checking if there is an article with such name'''
        for k in get_links():
            try:
                article = WikiArticle(k)
                #i had to change user agent, because wiki servers were blocking me (returning 403 - "Forbidden")
                response = requests.get("http://en.wikipedia.org/wiki/%s" %
                                        article.title)
                self.assertEqual(response.status_code,
                                 200,
                                 msg="ERROR at: %s" % article.url)
            except ArticleException as e:
                pass

    def test_articles_no_thumbnail(self):
        '''checking if article without thumbnail will raise an exception'''
        articles = [
            'https://en.wikipedia.org/wiki/1952_Formula_One_season',
            "https://pl.wikipedia.org/wiki/Shrek",
            "https://pl.wikipedia.org/wiki/My_Beautiful_Dark_Twisted_Fantasy"
        ]

        for k in articles:
            self.assertRaises(ArticleException, WikiArticle, k)

    def test_api_scrapping(self):
        '''tests if api urls are correct'''
        for k in get_links(2):
            try:
                article = WikiArticle(k)
                response = requests.get(article.api_url)
                self.assertEqual(response.status_code, 200)
            except ArticleException as e:
                pass  #no need to check articles without thumbnail

    def test_thumbnails_urls(self):
        '''tests if urls for thumbnails are scrapped correctly'''
        for k in get_links(2):
            try:
                article = WikiArticle(k)
                response = requests.get(
                    article.get_thumbnail_url(),
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
                    })
                self.assertEqual(response.status_code,
                                 200,
                                 msg="ERROR: %s " % article)
            except ArticleException as e:
                pass  #no need to check articles without thumbnail
    
    def test_original_thumbnails_urls(self):
        '''tests if urls for fullsize thumbnails are scrapped correctly'''
        for k in get_links(2):
            try:
                article = WikiArticle(k)
                response = requests.get(
                    article.get_original_thumbnail_url(),
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
                    })
                self.assertEqual(response.status_code,
                                 200,
                                 msg="ERROR: %s, %s " % (article, article.get_original_thumbnail_url()))
            except ArticleException as e:
                pass  #no need to check articles without thumbnail
