import requests

wiki_link="https://en.wikipedia.org/wiki/Sebastian_Vettel"

def wiki_link_to_name(url):
    '''Returns article name from wiki article'''
    temp = "wikipedia.org/wiki/"    #poczatek kazdego linku na wiki
    url = url[url.index(temp) + len(temp):]   #usuwam poczatek
    if "#" in url:
        return url[:url.index("#")]
    elif "?" in url:
        return url[:url.index("?")]
    else:
        return url




if __name__ == "__main__":
    page = requests.get(wiki_link)
    print(page.status_code)