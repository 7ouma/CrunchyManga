Update 11/03/17
====
CrunchyManga now needs CFScrape in order to work.


Simply run `pip install cfscrape`. The PyPI package is at https://pypi.python.org/pypi/cfscrape/


Alternatively, clone [this](https://github.com/Anorov/cloudflare-scrape) repository and run `python setup.py install`.

CrunchyManga
============
Download Manga from Crunchyroll (Manga, ComicPo! and Artist Alley)

If you have a premium account you can download all the chapters, series, volumes you want, if not, you'll only be able to download the latest chapters.

When downloading a series from its link, you can choose to download all volumes and individual chapters available (Using your config file), the series as invididual chapters (using the config file) and only the chapters your need (using a parameter), example (**If you want to download a single chapter you don't have to do this (the info listed below). You can just use its direct link/url to download the chapterm example: http://www.crunchyroll.com/comics_read/manga?volume_id=1593&chapter_num=1.00**):

	Example 1: http://www.crunchyroll.com/comics/manga/bokura-wa-minna-kawaisou/volumes [1-15, 25, 50]
	
	What I'm doing here is asking the script to download chapters from 1 to 15, then chapter 25 and chapter 50
	
	Example 2: www.crunchyroll.com/comics/manga/fuuka/volumes [5-20, 50.5]
	
	This will download chapters 5 to 20, and chapter 50.5.
	
	Example 3 (Using CLI): CrunchyManga.py -u "http://www.crunchyroll.com/comics/manga/bokura-wa-minna-kawaisou/volumes [1-15, 25, 50]"
	
	Example 4 (Using CLI and windows executable): CrunchyManga.exe -u "http://www.crunchyroll.com/comics/manga/bokura-wa-minna-kawaisou/volumes [1-15, 25, 50]"
	
	Please note that even if you have the download_volumes option activated, the chapters will be downloaded as individual chapters.
	
	

- Config file, this file is created once you run the script. You can edit as you like, but, if you edit it while the script is running, please restart the script. The options:

		- dir: Your directory, if the directory doesn't exist, the script will take the script folder as default. Please note that you'll need to use double Backslash when using windows. Example: "dir": "c:\\manga" instead of "dir":"c:\manga"
		- zip: I think i don't have to say what does this option do. values: true/false
		- download_volumes: this only works with complete series downloads. if this option is true(activated), the script will download all the volumes available with covers and so, then the rest of the individial episodes.values: true/false
		- overwrite_folders: if false and the script detects that the chapter folder you are downloading exists, the download will stop. If you're downloading a whole series/volume, the script will skip the chapter and continue to the next one. Please, note that if the chapter is incomplete, you know. (Doesn't work with zip files yet). values: true/false
		- delete_files_after_zip: Only works if zip is activated, once the file is downloaded and zipped, the folder will be deleted only remaining the zip file.values: true/false


- Console parameters. Don't worry about this, you can use the script just clicking the mangadownloader.py file. This is just a test, that's why there are only two commands plus the help:

		- mangadownloader.py -u link / mangadownloader.py --url link. Please note that you'll need to use double quotation marks in some cases, to avoid error with the & from the url/link.
		- mangadownloader.py -l user password / mangadownloader.py --link user password. Please note that you'll need to use double quotation marks in some cases, to avoid error with blanks and some symbols.
		- mangadownloader.py -h / mangadownloader.py --help. Explains the script (parameters) usage.



*********************************************
Found a typo, a bug, wanna help?

I'm still learning, so if you have any feedback, contact me at 7ouman@gmail.com 
*********************************************
Python 2.7.x
