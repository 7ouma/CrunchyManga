from __future__ import print_function
#!/usr/bin/env python
# -*- coding: cp1252 -*-
from getpass import getpass
import shutil
import sys
from time import sleep
from itertools import izip, cycle
import re
try:
    from BeautifulSoup import BeautifulSoup
except ImportError,e:
    print("CrunchyManga needs BeautifulSoup3 to work. Please install it (pip install BeautifulSoup) or use the portable version (https://github.com/7ouma/CrunchyManga/blob/master/BeautifulSoup.py) and place it in the same folder as this script.")
    sleep(60)
    exit()
import urllib2
import os
from urlparse import urlparse
import json
import cookielib
import urllib
from os import path
import argparse
from zipfile import *


about = '''
Crunchyroll Manga Downloader v0.4.2 Beta (CrunchyManga v0.4.2 Beta for short).
All credits goes to Miguel A (Touman).

You can use this script as suits you. Just do not forget to leave the credit.

If you are in any doubt whatsoever about how to use this script or want to support me, do not hesitate to tell me. Contact me at 7ouman@gmail.com

https://github.com/7ouma/CrunchyManga
'''

changelog = '''
Crunchyroll Manga Downloader v0.4.2 Beta (CrunchyManga v0.4.2 Beta for short).
What's new in this version?

* 28/09/2015: Fixed premium downloads.

* This version is a new one made from scratch, so some features like Download volumes, complete mangas, packs and CLI are not working yet.

* This version downloads only individual chapters so far, I hope to finish it soon.

* Several bugs have been fixed (it may still have some bugs left in the script).


Remember, this is a Beta! if you want to use all features get the buggy v0.3.2. Some things may change in the stable and the next version.

'''

class MangaDownloader:  
    def __init__(self, setConfig = True):
        self.error = False
        self.errors = []
        self.PageError = []
        self.downloadtype = ""
        self.manga_titulo = None
        self.chapterNumber = None
        self.volumeNumber = None
        self.directorio = os.getcwd()
        if setConfig:
            x = self.LoadSettings()
            if x:self.setConfig(x)
    def xord(self, bytear, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(bytear, cycle(key)))

    def zipManga(self, dir):
        self.errors = []
        try:
            zip = ZipFile(dir+".zip", "w", ZIP_DEFLATED)
            for root, dirs, files in os.walk(dir):
                for file in files:
                    x = os.path.join(root, file)
                    y = x[len(dir)+len(os.sep):]
                    zip.write(x,y)
            zip.close()
        except Exception,e:
            zip.close()
            os.remove(dir+".zip")
            self.addError("\nSomething went wrong: %s (%s)"%(e.message, e.args))
            return False
        if self.delete_files:
            shutil.rmtree(dir)
        return True


    def Directorio(self, manga_titulo, chapter, number = None):
    	manga = os.path.join(self.dir,manga_titulo)
    	if not self.CheckDir(manga): os.mkdir(manga)
    	chapter = os.path.join(self.dir,manga_titulo, manga_titulo + " - " + chapter)
        if self.CheckDir (chapter) or os.path.isfile(chapter+".zip"):
            x = True
            if not self.overwrite:
                if self.CheckDir(chapter) and not os.path.isfile(chapter+".zip"):
                    x = False if len(os.listdir(chapter)) < number else True
                if x:return False

            else:
                if os.path.isfile(chapter+".zip"):os.remove(chapter+".zip")
                if not self.CheckDir(chapter):os.mkdir(chapter)
        else:os.mkdir(chapter)    
      
        return chapter

    def CheckDir(self, dir):
        if not os.path.isdir(dir):
            return False
        return True
    
    def addError(self, error):
        self.errors.append(error)
        '''
        This method will create a logfile "Errorlog.txt".
        '''

    def addPageError(self, error):
        self.PageError.append(error)
   
    def LoadSettings(self, filename = "config.json"):       
        try:
            with open(filename) as config:
                return json.load(config)
        except (OSError, IOError),e:
            self.addError("Config.json doesn't exist. Config.json has been created.")
            self.config()
            return False

    def checkStr(self, string):
        nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
        return "".join(i for i in string if not i in nopermitido)
    def IsLogged(self, user = None):
        pass
        '''
        This method'll check if the user is logged in.

        '''
    def setConfig(self, config):
        try:
            self.dir = config["dir"]
            while True:
                if self.dir.lower() == "default":
                    self.dir = os.path.join(self.directorio, "Manga")
                    if not self.CheckDir(self.dir):os.mkdir(self.dir)
                    break
                else:
                    if not self.CheckDir(self.dir):
                        self.addError("\n%s doesn't exist. Using default folder."%(self.dir))
                        self.dir = "default"
                        self.error = True
                    else:break
            if self.boolStr(config["zip"]):
                self.zip = True if self.checkBool(config["zip"]) else False
            else:
                self.error = True
                self.zip  = False
            if self.boolStr(config["download_volumes"]):
                self.d_volumes = True if self.checkBool(config["download_volumes"]) else False
            else:
                self.error = True
                self.d_volumes = True
            

            if self.boolStr(config["overwrite_folders"]):
                self.overwrite = True if self.checkBool(config["overwrite_folders"]) else False
            else:
                self.error = True
                self.overwrite = False

            if self.boolStr(config["delete_files_after_zip"]):
                self.delete_files = True if self.checkBool(config["delete_files_after_zip"]) else False
            else:
                self.error = True
                self.delete_files = False
        except (ValueError),e:
            self.error = True
        except Exception,e:
            self.addError("\nSomething went wrong: %s (%s)"%(e.message, e.args))
        finally:
            if self.error:
                self.addError("\nConfig.json is broken. Config.json has been fixed (Some settings may be lost).")
                try:
                    self.config(self.dir, self.zip, self.d_volumes, self.overwrite, self.delete_files)
                except:
                    self.config()


    def boolStr(self, bool):
        return True if str(bool).lower() == "true" or str(bool).lower() == "false" else False
    def checkBool(self,bool):
        return True if str(bool).lower() == "true" else False
    def config(self, directorio = "default", zip = "false", download_volumes = "true", overwrite_folders = "false", delete_files_after_zip = "false"):
        config = '''{
"dir":"'''+directorio.replace("\\","\\\\")+'''",
"zip":'''+str(zip).lower()+''',
"download_volumes": '''+str(download_volumes).lower()+''',
"overwrite_folders": '''+str(overwrite_folders).lower()+''',
"delete_files_after_zip":'''+str(delete_files_after_zip).lower()+'''
}'''
        f = open("config.json",'wb')
        f.write(config)
        f.close()

    def numCap(self,numCap):
        chp = []
        if re.match(r"([0-9]+)((\.)([0-9]{1,2})?)?",numCap):
            ch = re.match(r"([0-9]+)(?:(\.)([0-9]{1,2})?)?",numCap)
            ch = ch.groups()
            Cap = ch[0]
            for i in ch:
                chp.append(i)
            if not chp[1]:
                chp[1] = "."
                chp[2] = "00"
                numCap = numCap + chp[1]+chp[2]
            else:
                if not chp[2]:
                    chp[2] = "00"
                    numCap = numCap + chp[2]
                if not chp[2][0] == "0":
                    Cap = Cap + "."+chp[2][0]
                if len(chp[2]) == 1:
                    numCap = numCap + "0"
            return Cap,numCap
        return False
    def downloadHtml(self, url, login = [False,None,None]):
        self.code = ""
        self.cookies()
        try:
            cookies = cookielib.MozillaCookieJar('cookies.txt')
            cookies.load() 
            opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(cookies))
            opener.addheaders =[('Referer', 'http://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
            if login[0]:
                data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : login[1], 'password' : login[2]}
                response = opener.open(url, urllib.urlencode(data))
                html = opener.open("http://www.crunchyroll.com")
                if re.search(login[1]+'(?i)',html.read()):
                    cookies.save()
                    return True
                else:
                    return False
            else:
                response = opener.open(url)
            html = response.read()
            cookies.save()
            return html
        except urllib2.HTTPError, e:
            self.addError("Crunchyroll: Error - %s."%e.code)
            self.code = e.code
        except urllib2.URLError, e:
            self.addError("Error: No internet connection available.")
        except Exception,e:
            self.addError("Error: %s."%e.message)


    def downloadImg(self, page):
        try:
            descarga = self.xord(urllib2.urlopen(page).read(),'B')
            return descarga
        except (urllib2.HTTPError,urllib2.URLError,Exception), e:
            self.addPageError(page)

    def saveImg(self, img, name, directorio):
	    f = open(os.path.join(directorio,name), 'wb' )
	    f.write(img)
	    f.close()
    def getPages(self, chapter):
        i = 0
        pages = {}
        for item in chapter["pages"]:
            pages[i] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
            if not pages[i]:
                pages[i] = item["image_url"]
            i+=1
        return pages
    def Chapter(self,sesion_id,url_serie,manga_titulo,chapterNumber):
        self.errors = []
        cr_auth = self.cr_auth("http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json")
        if not cr_auth:return
        serie = self.downloadHtml(url_serie)
        serie = json.loads(serie)
        chapter_id = None
        for item in serie["chapters"]:
            if item["number"] == str(chapterNumber[1]):
                chapter_id = item["chapter_id"]
        if not chapter_id:
            self.addError("\n%s - %s is not available yet, try again later.\n"%(manga_titulo,chapterNumber[0]))
            return False
        url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id+"&auth="+cr_auth
        chapter = self.downloadHtml(url_capitulo)
        if not chapter:
            if self.code == 400:
                self.errors = []
                self.addError("\nTo download %s - %s you have to be premium user.\n"%(manga_titulo,chapterNumber[0]))
            return False
        chapter = json.loads(chapter)
        return self.getPages(chapter)


    def Volume(self, soup):
        self.errors = []

    def cr_auth(self, url):
        cr_auth = self.downloadHtml(url)
        if cr_auth:
            cr_auth = json.loads(cr_auth)
            cr_auth = "null" if cr_auth['error'] else cr_auth["data"]["auth"]
        return cr_auth 
    def Manga(self, url):
        pass

    def MangaData(self):

    	return self.manga_titulo,self.chapterNumber
    def getUrl(self, url, downloadtype = None):
        if not downloadtype: downloadtype = self.downloadtype 
        self.errors = []
        html = self.downloadHtml(url)
        if not html:
            return False
        soup = BeautifulSoup(html)
        manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"})
        if manga:
            manga = manga.find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars").split("=")
            manga_titulo = soup.find(u"span", {u"itemprop":u"title"}).text
            #nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
            #for i in nopermitido:manga_titulo = manga_titulo.replace(i,' ')
            manga_titulo = self.checkStr(manga_titulo)
            self.manga_titulo = manga_titulo
            n = len(manga)-2
            serie_id = manga[1][:manga[1].find('&chapterNumber')]
            chapterNumber = self.numCap(manga[2][:manga[2].find('&server')])
            if chapterNumber: self.chapterNumber = chapterNumber[0]
            sesion_id = manga[n]
            url_serie = "http://api-manga.crunchyroll.com/chapters?series_id="+serie_id
        if downloadtype == "Chapter":
            return self.Chapter(sesion_id,url_serie,manga_titulo,chapterNumber)
        elif downloadtype == "Volume":
            return self.Volume(soup)
        elif downloadtype == "Complete":
            pass
        else:
            self.addError("Error: Invalid download type.")

    def numImg(self, num):
        num = str(num)
        if len(num) == 1: num="00"+num
        elif len (num) == 2: num ="0"+num
        return num

    def UrlCheck(self,url):
        self.errors = []
        self.downloadtype = ""
        if not url.replace(" ","") == "":
            if re.search(r"^(https://)",url):
                url = url.replace("https://","http://")
            elif re.search(r"^(http://)",url):pass
            else:
                url = "http://"+url
            url = url.replace(" ","")
        if re.match(r"^(http:\/\/)(w{3}\.)?crunchyroll\.com\/comics_read(\/(?:manga|comipo|artistalley))?\?(volume\_id|series\_id)\=(\d+)\&chapter_num\=((\d+)(\.(\d{1,2})?)?)$",url): #Crunchyroll por episodios.
            self.downloadtype = "Chapter"
        elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(manga|comipo|artistalley))?(\?volume\_id\=[0-9]+)$",url): #Crunchyroll por volumenes
            self.downloadtype = "Volume"
        elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics\/(manga|comipo|artistalley)\/[a-z0-9\-]+\/)(volumes)$",url): #Crunchyroll por serie entera
            self.downloadtype = "Complete"
        if self.downloadtype:
            return url
        else:
            self.addError("Error: The url is not from Crunchyroll Manga")
    def cookies(self):
        try:
            with open("cookies.txt"):pass
        except(OSError, IOError):
            cookies = cookielib.MozillaCookieJar("cookies.txt")
            cookies.save()
            return False
        return True
    def login(self, user, password):
        self.errors = []
        login = self.downloadHtml("https://www.crunchyroll.com/?a=formhandler",[True, user, password])
        if login:
            return True
        return False



if __name__ == '__main__':
    def PrintErrors(x):
        for i in x:
            print (i)

    def cls():
        os.system('cls' if os.name=='nt' else 'clear')
    MenuTxt = '''Options:
1.- Download.
2.- Download Pack.
3.- Login.
4.- Edit Settings.
5.- About.
6.- Changelog.
0.- Exit.
>'''

    SettingsTxt = '''Edit Settings:
1.- Directory
2.- Zip
3.- Download mangas by volumes
4.- Overwrite folders
0.- Cancel.
>'''
    while True:
        Menu = True
        Manga = MangaDownloader()
        while Menu:
            if Manga.errors:
                PrintErrors(Manga.errors)
                break
            option = str(raw_input(MenuTxt))
            if option =="1":
                url = Manga.UrlCheck(str(raw_input("Url: ")))
                if Manga.errors:
                    PrintErrors(Manga.errors)
                else:
                    download = Manga.getUrl(url)
                    if not download:
                        PrintErrors(Manga.errors)
                    else:
                        i = 1
                        dl = len(download)
                        data = Manga.MangaData()
                        if data:
                            x = Manga.Directorio(data[0],data[1],dl)
                            if x:
                                while i<=dl:
                                    print('\r%s - %s: Page %d of %d' %(data[0], data[1], i, dl ), end='')
                                    Manga.saveImg(Manga.downloadImg(download[i-1]), Manga.numImg(i)+".jpg", x)
                                    i+=1
                                if Manga.zip:
                                    print ("\n\nCompressing %s - %s"%(data[0], data[1]))
                                    zip = Manga.zipManga(x)
                                    if zip:
                                        print ("%s - %s.zip has been created."%(data[0], data[1]))
                                    else:
                                        PrintErrors(Manga.errors)

                            else:
                                print ("%s - %s already exists and overwrite files is deactivated."%(data[0], data[1]))
            elif option == "2":
                pass
            elif option == "3":
                cls()
                print("////////Login//////////")
                user = str(raw_input("User: "))
                password = str(raw_input("Password: "))
                if Manga.login(user,password):
                    print("You have been successfully logged in.\n\n") 
                else:
                    print("Incorrect user or password. Please try again.\n\n")
                sleep(3)
                cls()

            elif option == "4":
                cls()
                sett = True
                while True:
                    while sett:
                        cls()
                        option = str(raw_input(SettingsTxt))
                        if option == "1":
                            while True:
                                edit = False
                                settings = Manga.LoadSettings()
                                print ("Current directory: %s"%(settings["dir"]))
                                option = str(raw_input("\n1.- Edit directory \n0.- Cancel.\n>"))
                                if option == "1":
                                    dir = str(raw_input("New directory: "))
                                    if dir.lower() == "default":
                                        edit = True
                                    elif Manga.CheckDir(dir):
                                        edit = True
                                    else:
                                        print ("Invalid directory. \"%s\" doesn't exist."%dir)

                                    if edit:
                                        Manga.config(
                                            directorio = dir, 
                                            zip = settings["zip"], 
                                            download_volumes = settings["download_volumes"],
                                            overwrite_folders = settings["overwrite_folders"], 
                                            delete_files_after_zip = settings["delete_files_after_zip"])
                                        break

                                elif option == "0":
                                    break
                                else:
                                    print ("Invalid option")
                        elif option == "2":
                            while True:
                                settings = Manga.LoadSettings()
                                print("Zip after downloading: %s"%(Manga.checkBool(settings["zip"])))
                                option = str(raw_input("\n1.- Change to " + ("True" if not Manga.checkBool(settings["zip"]) else "False\n2.- Delefe files after zip: %s"%(settings["delete_files_after_zip"])) +"\n0.- Cancel\n>"))
                                if option == "1":
                                    Manga.config(
                                            directorio = settings["dir"], 
                                            zip = False if Manga.checkBool(settings["zip"]) else True, 
                                            download_volumes = settings["download_volumes"],
                                            overwrite_folders = settings["overwrite_folders"], 
                                            delete_files_after_zip = settings["delete_files_after_zip"])
                                elif option == "2" and Manga.checkBool(settings["zip"]):
                                    Manga.config(
                                            directorio = settings["dir"], 
                                            zip = settings["zip"], 
                                            download_volumes = settings["download_volumes"],
                                            overwrite_folders = settings["overwrite_folders"], 
                                            delete_files_after_zip = False if Manga.checkBool(settings["delete_files_after_zip"]) else True)
                                elif option == "0":
                                    break
                                else:
                                    print ("Invalid option")


                                
                        elif option == "3":
                            while True:
                                settings = Manga.LoadSettings()
                                print("Download mangas by volumes: %s"%(Manga.checkBool(settings["download_volumes"])))
                                option = str(raw_input("\n1.- Change to " + ("True" if not Manga.checkBool(settings["download_volumes"]) else "False") +"\n0.- Cancel\n>"))
                                if option == "1":
                                    Manga.config(
                                            directorio = settings["dir"], 
                                            zip = settings["zip"], 
                                            download_volumes = False if Manga.checkBool(settings["download_volumes"]) else True,
                                            overwrite_folders = settings["overwrite_folders"], 
                                            delete_files_after_zip = settings["delete_files_after_zip"])
                                elif option == "0":
                                    break
                                else:
                                    print ("Invalid option")
                        elif option == "4":
                            while True:
                                settings = Manga.LoadSettings()
                                print("Overwrite folders: %s"%(Manga.checkBool(settings["overwrite_folders"])))
                                option = str(raw_input("\n1.- Change to " + ("True" if not Manga.checkBool(settings["overwrite_folders"]) else "False") +"\n0.- Cancel\n>"))
                                if option == "1":
                                    Manga.config(
                                            directorio = settings["dir"], 
                                            zip = settings["zip"], 
                                            download_volumes = settings["download_volumes"],
                                            overwrite_folders = False if Manga.checkBool(settings["overwrite_folders"]) else True, 
                                            delete_files_after_zip = settings["delete_files_after_zip"])
                                elif option == "0":
                                    break
                                else:
                                    print ("Invalid option")
                        elif option == "0":
                            sett = False
                            break
                        else:
                            print ("Invalid option")
                    if not sett:
                        break
                cls()
            elif option == "5":
                print(about)
            elif option == "6":
                print (changelog)
            elif option == "0":
                print("Thanks for using CrunchyManga (:...")
                Menu = False
                sleep(3)
                break
            else:
                print ("Invalid option.")
        if not Menu:
            break   

