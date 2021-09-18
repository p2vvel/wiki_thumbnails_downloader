# Wikipedia Thumbnails Downloader
Simple script for downloading thumbnails from wiki articles


	wiki:
			show       show thumbnail url
			save       save thumbnail

	optional arguments:
		-h, --help   show this help message and exit

Show function displays links in stdout

	wiki show:
		--url URL             wiki article url
		--size SIZE           max thumbnail size [default=500px]
		--type {original,thumbnail}
													thumbnail or original image
		--user_agent USER_AGENT
													user agent used in program, might be necessary if default doesnt work

Save function saves images locally

	wiki save:
		-h, --help            show this help message and exit
		--url URL             wiki article url
		--size SIZE           max thumbnail size(might be smaller) [default=500px]
		--type {original,thumbnail}
													choose between thumbnail or original image
		--user_agent USER_AGENT
													user agent used in program, might be necessary if default doesnt work
		--filename FILENAME   downloaded image filename
