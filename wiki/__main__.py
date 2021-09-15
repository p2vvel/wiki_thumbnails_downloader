import requests
from requests.models import Response



class ArticleException(Exception):
    pass


class WikiArticle:
    def __init__(self, url, thumbsize=None):
        try:
            self.thumbsize = thumbsize or 500
            self.url = url
            self.title = self.get_title()
            self.api_url = self.get_api_url()
            self.api_json = self.get_api_json()
            self.thumbnail_data = self.get_thumbnail_data()
        except Exception as e:
            raise e

    def __str__(self):
        return "<Article: %s>" % self.url

    def get_title(self):
        '''Returns article name from wiki article url'''
        temp = "wikipedia.org/wiki/"  #poczatek kazdego linku na wiki
        title = self.url[self.url.index(temp) + len(temp):]  #usuwam poczatek
        if "#" in title:
            return title[:title.index("#")]
        elif "?" in title:
            return title[:title.index("?")]
        else:
            return title

    def get_api_url(self):
        return "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles=%s&pithumbsize=%s" % (
            self.title, self.thumbsize)

    def get_api_json(self):
        response = requests.get(self.api_url)
        return response.json()

    def get_thumbnail_data(self):
        try:
            page_id = [k for k in self.api_json["query"]["pages"].keys()][0]
            thumbnail = self.api_json["query"]["pages"][page_id]["thumbnail"]
            # print("JEST?", "thumbnail" in self.api_json["query"]["pages"][page_id])
            return thumbnail
        except KeyError:
            raise ArticleException("Article without thumbnail!")

    def get_thumbnail_url(self):
        return self.thumbnail_data["source"]

    def get_original_thumbnail_url(self):
        url = self.thumbnail_data["source"]
        if "/thumb/" in url:
            url = url.replace("/thumb/", "/")  #removes "thumb/" part from url
            url = url[:url.rindex("/")]
            return url
        else:
            #if theres no /thumb/ part in thumbnail url, you were given fullsize thumbnail url, no need to change anything
            return url


if __name__ == "__main__":
    import sys
    args = sys.argv

    import argparse

    parser = argparse.ArgumentParser(prog="Wiki Thumbnails Downloader")
    parser.add_argument("show", nargs="?", help="shows link to article thumbnail")
    parser.add_argument("save", help="shows link to article thumbnail")
    parser.print_help()
    # article = WikiArticle(args[1])
    # print(article.get_thumbnail_url())