# wiki_thumbnails_downloader
Simple script for downloading thumbnails from wiki articles

usage: Wiki Thumbnails Downloader [-h] {show,save} ...

positional arguments:
    show       show thumbnail url
        optional arguments:
          -h, --help            show this help message and exit
          --url URL             wiki article url
          --size SIZE           max thumbnail size(might be smaller) [default=500px]
          --type {original,thumbnail}
                                choose between thumbnail or original image
          --user_agent USER_AGENT
                                user agent used in program, might be necessary if default doesnt work


    save       save thumbnail
        optional arguments:
          -h, --help            show this help message and exit
          --url URL             wiki article url
          --size SIZE           max thumbnail size(might be smaller) [default=500px]
          --type {original,thumbnail}
                                choose between thumbnail or original image
          --user_agent USER_AGENT
                                user agent used in program, might be necessary if default doesnt work
          --filename FILENAME   image filename

                        
optional arguments:
  -h, --help   show this help message and exit
  
