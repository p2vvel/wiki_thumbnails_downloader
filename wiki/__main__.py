import requests
from requests.models import Response



#TODO: write more tests
#TODO: improve exceptions messages


class ArticleException(Exception):
    pass


class WikiArticle:
    def title_from_link(image_url):
        '''Converts wikipedia image link to title for example: 
            "https://upload.wikimedia.org/wikipedia/commons/4/44/Sebastian_Vettel_2015_Malaysia_podium_1.jpg"
            -> 
            "Sebastian_Vettel_2015_Malaysia_podium_1.jpg"
        '''
        title = image_url[image_url.rindex("/") + 1:]
        return title

    def __init__(self, url, thumbsize, user_agent=""):
        self.thumbsize = thumbsize
        self.url = url
        self.localisation = url[url.index("://") +
                                3:url.index(".")]  #'pl', 'en', 'com' etc.
        self.header = {
            "User-Agent": user_agent
        } if user_agent else {
            "User-Agent":
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
        }
        try:
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
        return "https://%s.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles=%s&pithumbsize=%s" % (
            self.localisation, self.title, self.thumbsize)

    def get_api_json(self):
        response = requests.get(self.api_url, headers=self.header)
        if response.status_code != 200:
            raise ArticleException("Unable to fetch API data!")
        return response.json()

    def get_thumbnail_data(self):
        try:
            page_id = [k for k in self.api_json["query"]["pages"].keys()][0]

            if int(page_id) == -1:
                raise ArticleException("No article with such url!")
            thumbnail = self.api_json["query"]["pages"][page_id]["thumbnail"]
            return thumbnail
        except KeyError:
            raise ArticleException(
                "Article without thumbnail or API didnt returned any thumbnail data!"
            )
        except Exception as e:
            raise e

    def get_thumbnail_url(self):
        return self.thumbnail_data["source"]

    def get_original_thumbnail_url(self):
        url = self.thumbnail_data["source"]
        #if theres no /thumb/ part in thumbnail url, you were given fullsize thumbnail url, no need to change anything
        if "/thumb/" in url:
            url = url.replace("/thumb/", "/")  #removes "thumb/" part from url
            url = url[:url.rindex("/")]
        return url

    def save_thumbnail(self, filename=""):
        #saves thumbnail as file, locally
        image_url = self.get_thumbnail_url()
        if filename == "":
            filename = WikiArticle.title_from_link(image_url)
        else:
            extension = image_url[image_url.rindex(
                "."):]  #file extension is at the end of the url
            filename = filename + extension  #adding extension even if user has added one - for safety

        response = requests.get(image_url, headers=self.header)
        with open(filename, "wb") as file:
            file.write(response.content)

    def save_original_thumbnail(self, filename=""):
        #saves fullsize thumbnail as file, locally
        image_url = self.get_original_thumbnail_url()
        if filename == "":
            filename = WikiArticle.title_from_link(image_url)
        else:
            extension = image_url[image_url.rindex(
                "."):]  #file extension is at the end of the url
            filename = filename + extension  #adding extension even if user has added one - for safety

        response = requests.get(image_url, headers=self.header)
        with open(filename, "wb") as file:
            file.write(response.content)


def show_article(url, size, type, user_agent, **kwargs):
    article = WikiArticle(url, size, user_agent)
    if type == "thumbnail":
        print(article.get_thumbnail_url())
    elif type == "original":
        print(article.get_original_thumbnail_url())


def save_article(url, size, type, filename, user_agent, **kwargs):
    article = WikiArticle(url, size, user_agent)
    if type == "thumbnail":
        article.save_thumbnail(filename)
    else:
        article.save_original_thumbnail(filename)


def main():
    import sys
    args = sys.argv

    import argparse

    parser = argparse.ArgumentParser(prog="Wiki Thumbnails Downloader")
    subparsers = parser.add_subparsers()

    show_subparser = subparsers.add_parser("show", help="show thumbnail url")
    show_subparser.add_argument("--url",
                                type=str,
                                help="wiki article url",
                                required=True)
    show_subparser.add_argument(
        "--size",
        type=int,
        help="max thumbnail size(might be smaller) [default=500px]",
        default=500)
    show_subparser.add_argument(
        "--type",
        choices=["original", "thumbnail"],
        default="thumbnail",
        help="choose between thumbnail or original image")
    show_subparser.add_argument(
        "--user_agent",
        default="",
        help="user agent used in program, might be necessary if default doesnt work")
    show_subparser.set_defaults(func=show_article)


    save_subparser = subparsers.add_parser("save", help="save thumbnail")
    save_subparser.add_argument("--url",
                                type=str,
                                help="wiki article url",
                                required=True)
    save_subparser.add_argument(
        "--size",
        type=int,
        help="max thumbnail size(might be smaller) [default=500px]",
        default=500)
    save_subparser.add_argument(
        "--type",
        choices=["original", "thumbnail"],
        default="thumbnail",
        help="choose between thumbnail or original image")
    save_subparser.add_argument(
        "--user_agent",
        default="",
        help="user agent used in program, might be necessary if default doesnt work")
    save_subparser.add_argument("--filename",
                                type=str,
                                default="",
                                help="image filename")
    save_subparser.set_defaults(func=save_article)

    args = parser.parse_args()
    args.func(**args.__dict__)


if __name__ == "__main__":
    main()
    # article = WikiArticle("https://pl.wikipedia.org/wiki/Sebastian_Vettel", 500)
    # show_article("https://pl.wikipedia.org/wiki/Sebastian_Vettel", 500, "original", "")