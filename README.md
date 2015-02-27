CrunchyManga
============
v0.1
--------------------------------------------------------------
Download Manga from crunchyroll

If you have a premium account you can download all the chapters, series, volumes you want, if not, you'll only be able to download the latest chapters.

v0.2 - 22/01/2015
-------------------------------------------------------

- The script had stopped working due to the last crunchyroll update. Added some minimal fixes and now the script is in english.

v0.2.1 - 23/01/2015
-------------------------------------------------------

- Complete series downloads have been fixed in this update.

v0.2.2 - 09/02/2015
-------------------------------------------------------

- Added new regex. This fixes the "ERROR: The link is not from Crunchyroll/Manga" with new crunchyroll links (individual chapters). 

v0.2.2.1 - 10/02/2015
-------------------------------------------------------

- Complete series downloads when the manga has no individual chapters(simulpub bar) have been fixed in this update. Ex: http://www.crunchyroll.com/comics/manga/japan-sinks/volumes
 
v0.3 - 17/02/2015
-------------------------------------------------------
- Added support to ComicPo! and Artist Alley.
- The last regex i added was redundant. Fixed.
- Added config file, this file is created once you run the script. You can edit as you like, but, if you edit it while the script is running, please restart the script. The options:

		- dir: Your directory, if the directory doesn't exist, the script will take the script folder as default. Please note that you'll need to use double Backslash when using windows. Example: "dir": "c:\\manga" instead of "dir":"c:\manga"
		- zip: I think i don't have to say what does this option do. values: true/false
		- download_volumes: this only works with complete series downloads. if this option is true(activated), the script will download all the volumes available with covers and so, then the rest of the individial episodes.values: true/false
		- overwrite_folders: if false and the script detects that the chapter folder you are downloading exists, the download will stop. If you're downloading a whole series/volume, the script will skip the chapter and continue. Please, note that if the chapter is incomplete, you know. (Doesn't work with zip files yet). values: true/false
		- delete_files_after_zip: Only works if zip is activated, once the file is downloaded and zipped, the folder will be deleted only remaining the zip file.values: true/false
- Added some console parameters. Don't worry about this, you can use the script as always, just clicking the mangadownloader.py file. This is just a test, that's why there are only two commands plus the help:

		- mangadownloader.py -u link / mangadownloader.py --url link. Please note that you'll need to use double quotation marks in some cases, to avoid error with the & from the url/link.
		- mangadownloader.py -l user password / mangadownloader.py --link user password. Please note that you'll need to use double quotation marks in some cases, to avoid error with blanks and some symbols.
		- mangadownloader.py -h / mangadownloader.py --help. Explains the script (parameters) usage.
		
- Added "Download ALL MANGAS from crunchyroll" option. I think i don't have to say what does this option do.

v0.3.1 - 28/02/2015
-------------------------------------------------------
- The script works as always, same script, better syntax. Expect some other changes soon.

*********************************************
Found a typo, a bug, wanna help?

I'm still learning, so if you have any feedback, contact me at 7ouman@gmail.com 
*********************************************
Python 2.7.x
