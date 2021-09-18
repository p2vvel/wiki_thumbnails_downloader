from unittest import TestCase

from wiki.__main__ import ArticleException, WikiArticle

from links import *

import requests

import os


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
                article = WikiArticle(k, 500)
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
            "https://pl.wikipedia.org/wiki/The_Eminem_Show",
            "https://pl.wikipedia.org/wiki/My_Beautiful_Dark_Twisted_Fantasy"
        ]

        for k in articles:
            self.assertRaises(ArticleException, WikiArticle, k, 500)

    def test_api_scrapping(self):
        '''tests if api urls are correct'''
        for k in get_links(2):
            try:
                article = WikiArticle(k, 500)
                response = requests.get(article.api_url)
                self.assertEqual(response.status_code, 200)
            except ArticleException as e:
                pass  #no need to check articles without thumbnail

    def test_thumbnails_urls(self):
        '''tests if urls for thumbnails are scrapped correctly'''
        for k in get_links(2):
            try:
                article = WikiArticle(k, 500)
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
                article = WikiArticle(k, 500)
                response = requests.get(
                    article.get_original_thumbnail_url(),
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
                    })
                self.assertEqual(
                    response.status_code,
                    200,
                    msg="ERROR: %s, %s " %
                    (article, article.get_original_thumbnail_url()))
            except ArticleException as e:
                pass  #no need to check articles without thumbnail

    def test_saving_thumbnails_no_filename(self):
        '''tests if saving thumbnails works properly'''
        articles = [
            'https://en.wikipedia.org/wiki/1951_Formula_One_season',
            "https://pl.wikipedia.org/wiki/Shrek",
            "https://pl.wikipedia.org/wiki/Kanye_West"
        ]

        for url in articles:
            article = WikiArticle(url, 500)
            article.save_thumbnail()
            file_data = open(WikiArticle.title_from_link(article.get_thumbnail_url()), "rb").read()  #wczytuje plik
            img_data = requests.get(article.get_thumbnail_url(), headers=article.header).content
            self.assertEqual(file_data, img_data)
            os.remove(WikiArticle.title_from_link(article.get_thumbnail_url()))

    def test_saving_thumbnails_filename(self):
        '''tests if saving thumbnails works properly'''
        articles = [
            'https://en.wikipedia.org/wiki/1951_Formula_One_season',
            "https://pl.wikipedia.org/wiki/Shrek",
            "https://pl.wikipedia.org/wiki/Kanye_West"
        ]

        names = ["formula", "shrek.jpg", "ye.ezy"]

        for url, name in zip(articles, names):
            article = WikiArticle(url, 500)
            article.save_thumbnail(name)
            extension = article.get_thumbnail_url()
            extension = extension[extension.rindex("."):]
            file_data = open(name + extension, "rb").read()  #wczytuje plik
            img_data = requests.get(article.get_thumbnail_url(), headers=article.header).content
            self.assertEqual(file_data, img_data)
            os.remove(name + extension)


    def test_links_to_title(self):
        '''tests if turning links to images filenames works properly'''
        links = [
            "https://upload.wikimedia.org/wikipedia/commons/4/44/Sebastian_Vettel_2015_Malaysia_podium_1.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Alfa-Romeo-159-%281951%29.jpg/500px-Alfa-Romeo-159-%281951%29.jpg",
            'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Eminem_-_Concert_for_Valor_in_Washington%2C_D.C._Nov._11%2C_2014_%282%29_%28Cropped%29.jpg/416px-Eminem_-_Concert_for_Valor_in_Washington%2C_D.C._Nov._11%2C_2014_%282%29_%28Cropped%29.jpg',
        ]

        filenames = [
            "Sebastian_Vettel_2015_Malaysia_podium_1.jpg",
            "500px-Alfa-Romeo-159-%281951%29.jpg",
            "416px-Eminem_-_Concert_for_Valor_in_Washington%2C_D.C._Nov._11%2C_2014_%282%29_%28Cropped%29.jpg"
        ]

        for l, f in zip(links, filenames):
            self.assertEqual(WikiArticle.title_from_link(l), f)

    def test_localisation(self):
        '''tests if country subdomain is correctly fetched from wiki url'''
        articles = [
            'https://en.wikipedia.org/wiki/1951_Formula_One_season',
            "https://pl.wikipedia.org/wiki/Shrek",
            "https://szl.wikipedia.org/wiki/Lipy_(Prudnik)"
        ]
        subdomains = ["en", "pl", "szl"]

        for l, s in zip(articles, subdomains):
            try:
                article = WikiArticle(l, 500)
                self.assertEqual(s, article.localisation)
            except:
                self.assertEqual(s, article.localisation)