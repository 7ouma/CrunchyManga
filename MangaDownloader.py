#!/usr/bin/env python2.7
# -*- coding: cp1252 -*-
about='''
Crunchyroll MangaDownloader v0.3.2.4 (Crunchymanga v0.3.2.4 for short).
All credit goes to Miguel A(Touman).
You can use this script as suits you. Just do not forget to leave the credit.

If you are in any doubt whatsoever about how to use this script do not hesitate to tell me. Contact me at 7ouman@gmail.com and I'll try to reply as soon as possible.

Beautifulsoup and cfscrape (with its dependencies) are the only external libraries used.

https://github.com/7ouma/CrunchyManga
'''
from getpass import getpass
import shutil
import sys
from time import sleep
from itertools import izip, cycle
import re
from BeautifulSoup import BeautifulSoup
import urllib2
import os
from urlparse import urlparse
import json
import cookielib
import urllib
from os import path
import argparse
from zipfile import *
import cfscrape
from cookielib import LWPCookieJar

class MangaDownloader():

    def __init__(self):
        self.directorio = os.getcwd()
        self.read_config()
        self.scraper = cfscrape.create_scraper()
        self.UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"


    def xord(self,bytear, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(bytear, cycle(key)))


    def zipmanga(self):
        if self.manga_vol == "0":
            filename = self.filename
        else:
            filename = self.filevol
        os.chdir(self.filedir)
        def zipdir(path, zip):
            for root, dirs, files in os.walk(path):
                for file in files:
                    zip.write(os.path.join(root, file))
        print "\nCreating %s.zip\n"%(filename)
        zip_archive = ZipFile(filename+".zip", "w")
        zipdir(filename,zip_archive)
        zip_archive.close()
        os.chdir(self.directorio)
        if self.delete_files:
            try: 
                shutil.rmtree(self.filedir+"\\"+filename)
            except:
                shutil.rmtree(self.filedir+"/"+filename)

                
    def downloadPages( self, pages ):     
        i = 0
        try:
            while i < len( pages ):
                sys.stdout.write('\rPage %d of %d' %( i+1, len( pages ) ) ) 
                sys.stdout.flush()
                descarga = self.DownloadImages( pages[i] )
                if descarga is not None:
                    if (i+1) <= 9:
                            image = "00" + str(i+1) + ".jpg"
                    elif (i+1) <= 99:
                            image = "0" + str(i+1) + ".jpg"
                    else:
                            image = str(i+1) + ".jpg"
                    f = open( image, 'wb' )
                    f.write( self.xord( descarga, 'B' ) )
                    f.close()
                    i+=1
                else:
                    return 0
            return 1
        except:
            os.chdir(self.directorio)
    def DownloadImages(self, img):
		
        n_try = 1
        while n_try <=9:
            try:
                descarga = urllib2.urlopen(img).read()
                n_try = 10
                return descarga
            except (urllib2.URLError,KeyboardInterrupt):
                if n_try < 9:
                    for c in range(31):
                        sys.stdout.write( '\rFailed to download image. Trying again in %d ' %( 30-c ) )
                        sys.stdout.flush()
                        sleep(1)
                else:
                    sys.stdout.write('\rError downloading the chapter. Try again later.')
                    sys.stdout.flush()
                    os.chdir(self.directorio)
                    return None
            n_try += 1
    def Directorio(self,manga_cover = ""):
        nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
        os.chdir(self.directorio)
        try:
            self.manga_vol
        except AttributeError:
            self.manga_vol = "0"
        for i in nopermitido:
            self.manga_titulo = self.manga_titulo.replace(i,"")
        whi = True
        while (whi):
            if self.dir == "default":
                if os.path.isdir("Manga"):
                    os.chdir("Manga")
                else:
                    os.mkdir("Manga")
                    os.chdir("Manga")
                whi = False
            else:
                if os.path.isdir(self.dir):
                    os.chdir(self.dir)
                    whi = False
                else:
                    print "\n%s doesn't exist. Using dafault folder."%(self.dir)
                    self.dir = "default"  
        if os.path.isdir(self.manga_titulo):
            os.chdir(self.manga_titulo)
        else:
            os.mkdir(self.manga_titulo)
            os.chdir(self.manga_titulo)
        self.filedir = os.getcwd()
    ##
        self.filevol = self.manga_titulo + " - Vol." + self.manga_vol
        if not self.manga_vol == "0":
            
            if os.path.isdir(self.filevol):
                os.chdir(self.filevol)
            else:
                os.mkdir(self.filevol)
                os.chdir(self.filevol)
            if not manga_cover == "":
                descarga = self.DownloadImages(manga_cover)
                if descarga is not None:
                    image = "Cover - Vol." + self.manga_vol + ".jpg"
                    f = open(image,'wb')
                    f.write(self.xord(descarga, 'B'))
                    f.close()
    ##
        self.filename = self.manga_titulo + " - " + self.manga_numcap       
        if self.overwrite and os.path.isdir(self.filename):
            os.chdir(self.filename)
            return True
        elif not os.path.isdir(self.filename):
            os.mkdir(self.filename)
            os.chdir(self.filename)
            return True
        else:
            return False


    def read_config(self):
        _config = True
        while (_config):
            try:
                with open('config.json') as config_file:
                    x = json.load(config_file)
                    self.dir = x["dir"]
                    self.zip = x["zip"]
                    self.d_volumes = x["download_volumes"]
                    self.overwrite = x["overwrite_folders"]
                    self.delete_files = x["delete_files_after_zip"]
                    if self.zip == True or self.zip == False: pass
                    else: self.config()
                    if self.d_volumes == True or self.d_volumes == False: pass
                    else: self.config()
                    if self.overwrite == True or self.overwrite == False: pass
                    else: self.config()
                    if self.delete_files == True or self.delete_files == False: pass
                    else: self.config()
                    _config = False
            except (OSError, IOError):
                self.config()
            except Exception,e:
                print "Error: ",e
                self.config()
    def mangaurl(self,url):
        if not url.replace(" ","") == "":
            
            if re.search(r"^(https://)",url):
                url = url.replace("https://","http://")
            elif re.search(r"^(http://)",url):pass
            else:
                url = "http://"+url
            self.url = url.replace(" ","")
        
        
    def config(self):
        print "Seens like config.json is broken or doesn't exist. Creating config file..."
        config = '''
{
"dir":"default",
"zip":false,
"download_volumes": false,
"overwrite_folders": false,
"delete_files_after_zip":false
}

'''
        f = open("config.json",'wb')
        f.write(config)
        f.close()
    def download(self,url=""):
        if url == "":
            url = self.url
        else:
            url = url
        try:
                with open('cookies.txt'): pass
        except (OSError, IOError):
                cookies = LWPCookieJar('cookies.txt')
                cookies.save()      
        cookies = self.scraper
        cookies.cookies = LWPCookieJar('cookies.txt')
        cookies.cookies.load()
        html = self.scraper.get(url).content
        cookies.cookies.save()
        return html
    #
    def login(self,usuario,password):
        try:
                with open('cookies.txt'): pass
        except IOError:
                cookies = LWPCookieJar('cookies.txt')
                cookies.save()
        url = 'https://www.crunchyroll.com/login'
        cookies = self.scraper
        cookies.cookies = LWPCookieJar('cookies.txt')
        page = self.scraper.get(url).content
        page = BeautifulSoup(page)
        hidden = page.findAll("input",{u"type":u"hidden"})
        hidden = hidden[1].get("value")
        logindata = {'formname' : 'login_form', 'fail_url' : 'http://www.crunchyroll.com/login', 'login_form[name]' : usuario, 'login_form[password]' : password,'login_form[_token]': hidden,'login_form[redirect_url]':'/'}
        req = self.scraper.post(url, data = logindata)
        url = "http://www.crunchyroll.com"
        html = self.scraper.get(url).content
        if re.search(usuario+'(?i)',html):
                print 'You have been successfully logged in.\n\n'
                cookies.cookies.save()
        else:
                print 'Failed to verify your username and/or password. Please try again.\n\n'
                cookies.cookies.save()

    def CrunchyManga(self):
        cc = 1
        regex = r"\[{1} *(\d+(?:\.\d{1,2})?(?: *\- *\d+(?:\.\d{1,2})?)?)(\ *,{1} *(\d+(?:\.\d{1,2})?(?: *\- *\d+(?:\.\d{1,2})?)?))* *\]{1}$"
        chapters_ = re.search(regex,self.url)
        ch_dwn = None
        if chapters_:
            url = self.url.split ("[")
            ch_dwn = url[1]
            self.url = url[0]            
        print "Analyzing link %s..."%self.url
        if re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read(\/(manga|comipo|artistalley))?\?(volume\_id|series\_id)\=[0-9]+&chapter\_num\=[0-9]+(\.[0-9])?)",self.url): #Crunchyroll por episodios.
            try:
                html= self.download()
                soup = BeautifulSoup(html)
                self.manga_titulo = soup.find(u"span", {u"itemprop":u"title"}).text
                self.manga_titulo = self.manga_titulo.replace(':',' ')
                manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
                manga = manga.split("=")
                n = len(manga)-2
                serie_id = manga[1][:manga[1].find('&chapterNumber')]
                numero_cap = manga[2][:manga[2].find('&server')]
                if re.match(r"([0-9]+)(\.[0-9]{1,2})",numero_cap):
                    ch = re.match(r"([0-9]+)(\.[0-9]{1,2})",numero_cap)
                    ch = ch.groups()
                    if ch[1].__len__() == 2:
                        numero_cap = numero_cap + "0"
                    x = numero_cap[-2:]
                    if x == "00":
                        self.manga_numcap = numero_cap[:-3]
                    else:
                        self.manga_numcap = numero_cap[:-1]
                else:
                    self.manga_numcap = numero_cap
                sesion_id = manga[n][:manga[n].find('&config_url')]
            except Exception,e:
                print "The link is certainly from Crunchyroll, but it seems that it's not correct. Verify it and try again."
                return
            cr_auth = "http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json"
            html = self.download(cr_auth)
            try:
                soup = json.loads(html)
                cr_auth=""
                for item in soup["data"]["auth"]:
                    cr_auth=cr_auth+item            
            except:
                cr_auth = "null"            
            url_serie = "http://api-manga.crunchyroll.com/chapters?series_id="+serie_id
            html= self.download(url_serie)
            soup = json.loads(html)
            chapter_id = ""
            for item in soup["chapters"]:
                if item["number"] == str(numero_cap):
                    chapter_id = item["chapter_id"]
            if chapter_id == "":
                print u"\nThe chapter %s is not currently unavailable, try again later.\n"%self.manga_numcap
                return
            else:
                url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id+"&auth="+cr_auth
                try:
                    html= self.download(url_capitulo)
                    soup = json.loads(html)
                    c=0
                    pages = {}
                    for item in soup["pages"]:
                        try:
                            pages[c] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                        except:      
                            pages[c] = item["image_url"]
                        c=c+1
                except Exception,e:
                    print "\n\nYou have to be premium user in order to download this chapter. "
                    return
                print u"\nDownloading %s - %s..."%(self.manga_titulo,self.manga_numcap)
                x = self.Directorio()
                if not x:
                    print "The folder %s - %s already exists and overwrite folders is deactivated."%(self.manga_titulo,self.manga_numcap)
                    os.chdir(self.directorio)
                else:              
                    descarga = self.downloadPages(pages)
                    os.chdir(self.directorio)
                    if self.zip and descarga == 1:
                        self.zipmanga()
        elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(manga|comipo|artistalley))?(\?volume\_id\=[0-9]+)$",self.url): #Crunchyroll por volumenes
            volume = re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(?:manga|comipo|artistalley))?(\?volume\_id\=([0-9]+))$",self.url) 
            try:
                html= self.download()
                soup = BeautifulSoup(html)
                manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
                manga = manga.split("=")
                n = len(manga)-2
                serie_id = manga[1][:manga[1].find('&chapterNumber')]
                sesion_id = manga[n]
            except:
                print "The link is certainly from Crunchyroll, but it seems that it's not correct. Verify it and try again."
                return
            url_serie = "http://api-manga.crunchyroll.com/chapters?series_id="+serie_id
            html= self.download(url_serie)
            soup = json.loads(html)
            self.manga_titulo = soup["series"].pop("locale").pop("enUS").pop("name")
            capitulo = []
            chapter_id = []
            volume = volume.groups()
            volume = volume[5]
            for item in soup["chapters"]:
                if item.pop("volume_id") == volume:
                    chapter_id.append(item.pop("chapter_id")) 
                    capitulo.append(item.pop("number"))
                    self.manga_vol = item.pop("volume_number")
            cr_auth = "http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json"
            html = self.download(cr_auth)
            try:
                soup = json.loads(html)
                cr_auth=""
                for item in soup["data"]["auth"]:
                    cr_auth=cr_auth+item
            except:
                print "To download volumes you need a premium account. Standard accounts can only download the latest chapter."
                return
            c = 0
            cv = True
            rr = 0
            if self.manga_vol == "0":
                print "Downloading individual chapters"
            while c < len(capitulo):
                x = capitulo[c][-2:]
                if x == "00":
                    capitulo[c] = capitulo[c][:-3]
                else:
                    capitulo[c] = capitulo[c][:-1]
                self.manga_numcap = capitulo[c]
                if self.manga_vol == "0":
                    print "\n%s: Chapters %d/%d"%(self.manga_titulo,c+1,len(capitulo))
                    print "\nDownloading %s - %s"%(self.manga_titulo,self.manga_numcap)
                else:
                    print "\n%s Vol.%s: Chapters %d/%d"%(self.manga_titulo,self.manga_vol,c+1,len(capitulo))
                    print "\nDownloading %s Vol.%s ch.%s"%(self.manga_titulo,self.manga_vol,self.manga_numcap)
                url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id[c]+"&auth="+cr_auth
                html= self.download(url_capitulo)
                soup = json.loads(html)
                c2=0
                pages = {}
                manga_cover = ""
                if cv == True:
                    if not self.manga_vol == "0":
                        manga_cover = soup["volume"].pop("encrypted_image_url")
                    cv = False
                for item in soup["pages"]:
                    try:
                        pages[c2] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                    except:      
                        pages[c2] = item["image_url"]
                    c2=c2+1
                x = self.Directorio(manga_cover)
                if not x:
                    print "The folder %s - %s already exists and overwrite folders is deactivated."%(self.manga_titulo,self.manga_numcap)
                    os.chdir(self.directorio)
                else:
                    descarga = self.downloadPages(pages)
                    if self.manga_vol == "0" and self.zip and descarga == 1:
                        self.zipmanga()
                    os.chdir(self.directorio)
                    rr +=1
                c = c+1
            if self.zip and self.manga_vol != "0" and rr > 0:
                self.zipmanga() 
        elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics\/(manga|comipo|artistalley)\/[a-z0-9\-]+\/)(volumes)$",self.url): #Crunchyroll por serie entera
            html= self.download(self.url)
            soup = BeautifulSoup(html)
            serie_id = soup.find(u"span",{u"id":u"sharing_add_queue_button"}).get(u"group_id")
            if ch_dwn is not None:
                temp = self.d_volumes
                self.d_volumes = False
                ch_dwn = ((ch_dwn.replace(" ","")).replace("]","")).split(",")
            if self.d_volumes:
                i = 0
                vol_id = []
                try:
                    if soup.find(u"li",{ur"class":u"queue-item volume-simul"}).get(u"volume_id"):                
                        volumen_id = soup.findAll(u"li",{ur"class":re.compile(u"queue-item volume-")})
                        while i < len(volumen_id):
                            if i == len(volumen_id)-1:
                                vol_id.append(volumen_id[0].get(u"volume_id"))
                            else:
                                vol_id.append(volumen_id[i+1].get(u"volume_id"))
                            i+=1
                except:
                    volumen_id = soup.findAll(u"li",{ur"class":re.compile(u"queue-item volume-")})
                    for vols in volumen_id:
                        vol_id.append(vols.get(u"volume_id") )
                i=0
                for vols in vol_id:
                    print "Downloading all volumes and individual chapters available. Volumes: %d/%d"%(i+1,len(vol_id))
                    self.url = "http://www.crunchyroll.com/comics_read/manga?volume_id="+vols
                    self.CrunchyManga()
                    i+=1
            else:       
                volumen_id = soup.find(u"li",{ur"class":re.compile(u"queue-item volume-")}).get(u"volume_id")    
                url_vol = "http://www.crunchyroll.com/comics_read/manga?volume_id="+volumen_id
                html= self.download(url_vol)
                soup = BeautifulSoup(html)
                sesion_id = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
                sesion_id = sesion_id.split("=")
                n = len(sesion_id)-2
                sesion_id = sesion_id[n]
                url_serie = "http://api-manga.crunchyroll.com/chapters?series_id="+serie_id
                html= self.download(url_serie)
                soup = json.loads(html)
                self.manga_titulo = soup["series"].pop("locale").pop("enUS").pop("name")
                capitulo = []
                chapter_id = []
                for item in soup["chapters"]:
                    chapter_id.append(item.pop("chapter_id"))
                    capitulo.append(item.pop("number"))
                
                if ch_dwn is not None:
                    ch = []
                    ch_id = []
                    
                    for i in ch_dwn:
                        c = 0
                        if re.search("-",i):
                            x = i.split("-")
                            x1 = x[0]
                            x2 = x[1]
                            if float(x1) > float(x2):
                                x1 = x[1]
                                x2 = x[0]
                            for i2 in capitulo:
                                if float(i2) >= float(x1) and float(i2) <= float(x2):
                                    ch.append (i2)
                                    ch_id.append(chapter_id[c])
                                c+=1
                        else:
                            for i2 in capitulo:
                                if float(i) == float(i2):
                                    ch.append (i2)
                                    ch_id.append(chapter_id[c])
                                c+=1
                        
                    capitulo = ch
                    chapter_id = ch_id
                cr_auth = "http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json"
                html = self.download(cr_auth)
                try:
                    soup = json.loads(html)
                    cr_auth=""
                    for item in soup["data"]["auth"]:
                        cr_auth=cr_auth+item
                except:
                    print "To download complete series you need a premium account. Standard accounts can only download the latest chapter."
                    return
                c = 0
                while c < len(capitulo):
                    x = capitulo[c][-2:]
                    if x == "00":
                        capitulo[c] = capitulo[c][:-3]
                    else:
                        capitulo[c] = capitulo[c][:-1]
                    self.manga_numcap = capitulo[c]
                    print "\n\n%s chapters %d of %d: Downloading chapter %s"%(self.manga_titulo,c+1,len(capitulo),self.manga_numcap)
                    url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id[c]+"&auth="+cr_auth
                    html= self.download(url_capitulo)
                    soup = json.loads(html)
                    c2=0
                    pages = {}
                    for item in soup["pages"]:
                        try:
                            pages[c2] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                        except:      
                            pages[c2] = item["image_url"]
                        c2=c2+1
                    x = self.Directorio()
                    cc = 1
                    if not x:
                        print "\nThe folder %s - %s already exists and overwrite folders is deactivated."%(self.manga_titulo,self.manga_numcap)
                    else:
                        descarga = self.downloadPages(pages)
                        cc +=1
                    os.chdir(self.directorio)
                    if self.zip and cc > 1 and descarga == 1:
                        self.zipmanga()
                    c = c+1
                if ch_dwn is not None and temp:
                    self.d_volumes = True
        else:
            print "ERROR: The link is not from Crunchyroll/Manga"
        os.chdir(self.directorio)
    
    def PaqueteEnlace(self):
        c = 1
        try:
                with open('links.txt'): pass
        except (OSError, IOError):
                enlaces = open('links.txt','w')
                enlaces.close()
                print "The file \"links.txt\" has been created. Please edit it with your links(One per line)."
                return
        enlaces = open('links.txt','r')
        enlaces = enlaces.readlines()
        n_len = len(enlaces)
        if n_len > 0:
            while c <= n_len:
                print "Loading link %d/%d"%(c,n_len)
                self.mangaurl( enlaces[c-1].replace("\n","") )
                print self.url
                self.CrunchyManga()
                c = c + 1
        else:
            print "The file \"links.txt\" is empty. Please edit it with your links(One per line)."


    def AllMangas(self):
        html = self.download("http://www.crunchyroll.com/comics/manga/alpha?group=all")
        soup = BeautifulSoup(html)
        series = soup.findAll(u"ul",{u"class":u"clearfix medium-margin-bottom"})
        i = 0
        serie =[]
        url_serie = []
        for item in series:
            serie2 = item.findAll("li")
            for item2 in serie2:
                serie.append(item2.find("a").text)
                url_serie.append("http://www.crunchyroll.com" + item2.find(u"a").get(u"href"))
        while i < len(url_serie):
            print "Downloading all mangas from crunchyroll %d/%d\n%s"%(i+1,len(url_serie),serie[i])
            self.mangaurl(url_serie[i])
            self.CrunchyManga()
            i+=1        

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url", type=str,help="Crunchyroll Link. if you get an error, try using double quotation marks (\")")
    parser.add_argument("-l","--login",nargs = 2, help="Crunchyroll login: -l User password. if your password has a blank, use double quotation marks (\"). Example: \"This is a password.\"")
    arg = parser.parse_args()
    def principal():
        Manga = MangaDownloader()
        try:
            if arg.url:
                Manga.mangaurl(arg.url)
                Manga.CrunchyManga()
            elif arg.login:
                usuario = arg.login[0]
                password = arg.login[1]
                Manga.login(usuario, password)
            else:
                seleccion = 0
                print "\nOptions:"
                print "1.- Download\n2.- Download pack\n3.- Login \n4.- Download ALL MANGAS from crunchyroll \n5.- About \n0.- Exit"
                try:
                    seleccion = int(input("> "))
                except:
                    print "Invalid option"
                    principal()
                if seleccion == 1:
                    Manga.mangaurl(raw_input("Link: "))
                    Manga.CrunchyManga()
                    principal()
                elif seleccion == 2 :
                    Manga.PaqueteEnlace()
                    principal()
                elif seleccion == 3:
                    usuario = raw_input(u"User: ")
                    password = getpass()
                    #~ password = raw_input(u"Password: ")
                    Manga.login(usuario, password)
                    principal()
                elif seleccion == 4:
                    Manga.AllMangas()
                    principal()
                elif seleccion == 5:
                    print about
                    principal()
                elif seleccion == 0:
                    SystemExit()
                else:
                    print "ERROR: Invalid option."
                    principal()
        except KeyboardInterrupt:
            principal ()
        except Exception,e:
            print "\n",e.message
            principal()
            
    principal()
