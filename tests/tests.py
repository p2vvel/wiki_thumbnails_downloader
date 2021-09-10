from unittest import TestCase


from wiki.main import wiki_link_to_name


from links import *

import requests



class test_name_scraper(TestCase):
    '''Checks if names are correctly scrapped from wikipedia links by checking if there is an article with such name'''
    def test_seasons(self):
        for k in seasons_links:
            repsonse = requests.get("http://en.wikipedia.org/wiki/%s" % wiki_link_to_name(k))
            self.assertEqual(repsonse.status_code, 200)
    
    def test_constructors(self):
        for k in constructors_links[:20]:
            repsonse = requests.get("http://en.wikipedia.org/wiki/%s" % wiki_link_to_name(k))
            self.assertEqual(repsonse.status_code, 200)

    def test_drivers(self):
        for k in drivers_links[:20]:
            repsonse = requests.get("http://en.wikipedia.org/wiki/%s" % wiki_link_to_name(k))
            self.assertEqual(repsonse.status_code, 200)

    def test_races(self):
        for k in races_links[:20]:
            repsonse = requests.get("http://en.wikipedia.org/wiki/%s" % wiki_link_to_name(k))
            self.assertEqual(repsonse.status_code, 200)
    
    def test_circuits(self):
        for k in circuits_links[:20]:
            repsonse = requests.get("http://en.wikipedia.org/wiki/%s" % wiki_link_to_name(k))
            self.assertEqual(repsonse.status_code, 200)