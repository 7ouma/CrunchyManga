#!/usr/bin/env python2.7
# -*- coding: cp1252 -*-
about='''
Crunchyroll MangaDownloader v0.3.1 (Crunchymanga v0.3.1 for short).
All credit goes to Miguel A(Touman).
You can use this script as suits you. Just do not forget to leave the credit.

If you are in any doubt whatsoever about how to use this script do not hesitate to tell me. Contact me at 7ouman@gmail.com and I'll try to respond as soon as possible.

Beautifulsoup is the only external library used.

https://github.com/7ouma/CrunchyManga
'''

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
from zipfile import *

class MangaDownloader():

    def __init__(self):
        self.directorio = os.getcwd()
        self.read_config()
    ###Decrypt
    def xord(self,bytear, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(bytear, cycle(key)))
    ###End Decrypt
    #Zip Manga
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
            shutil.rmtree(path+"\\"+filename)
    #End Zip manga
    def downloadImage(self,imageUrl,image):
        try:
            if int(image) <= 9:
                image = "0" + image + ".jpg"
            else:
                image = image + ".jpg"
        except:
            image = image + ".jpg"
        try:
            descarga = urllib2.urlopen(imageUrl).read()
        except:
            cn = 1
            while cn <= 9:
                try:
                   descarga = urllib2.urlopen(imageUrl).read()
                   cn = 10
                except:   
                    if cn == 9:
                        print "\nError downloading the image.\n"
                    else:
                        print "\n"
                        for i in range(31):
                            sys.stdout.write('\rFailed to download image. Trying again in %d ' %(30-i))
                            sys.stdout.flush()
                            sleep(1)
                        print "\n"
                    cn += 1
        f = open(image,'wb')
        f.write(self.xord(descarga, 'B'))
        f.close()

       
    def Directorio(self):
        nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
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
            if not self.manga_cover == "":
                self.downloadImage(self.manga_cover,"Cover - Vol." + self.manga_vol)
        
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
        if re.search(r"^(https://)",url):
            url = url.replace("https://","http://")
        elif re.search(r"^(http://)",url):pass
        else:
            url = "http://"+url
        self.url = url
        
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
                cookies = cookielib.MozillaCookieJar('cookies.txt')
                cookies.save()
        cookies = cookielib.MozillaCookieJar('cookies.txt')
        cookies.load() 
        opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(cookies))
        opener.addheaders =[('Referer', 'http://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
        response = opener.open(url)
        html = response.read()
        cookies.save()
        return html
    #
    def login(self,usuario,password):
        try:
                with open('cookies.txt'): pass
        except IOError:
                cookies = cookielib.MozillaCookieJar('cookies.txt')
                cookies.save()
        url = 'https://www.crunchyroll.com/?a=formhandler'
        data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : usuario, 'password' : password}
        cookies = cookielib.MozillaCookieJar('cookies.txt')
        cookies.load() 
        opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(cookies))
        opener.addheaders =[('Referer', "http://www.crunchyroll.com"),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
        req = opener.open(url, urllib.urlencode(data))
        url = "http://www.crunchyroll.com"
        req = opener.open(url)
        html = req.read()
        if re.search(usuario+'(?i)',html):
                print 'You have been successfully logged in.\n\n'
                cookies.save()
        else:
                print 'Failed to verify your username and/or password. Please try again.\n\n'

    def CrunchyManga(self):
        cc = 1
        print "Analyzing link..."
        if re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read(\/(manga|comipo|artistalley))?\?(volume\_id|series\_id)\=[0-9]+&chapter\_num\=[0-9]+\.[0-9])",self.url): #Crunchyroll por episodios.
            try:
                html= self.download()
                soup = BeautifulSoup(html)
                self.manga_titulo = soup.find(u"span", {u"itemprop":u"title"}).text
                self.manga_titulo = self.manga_titulo.replace(':',' ')
                manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
                manga = manga.split("=")
                n = len(manga)-1
                serie_id = manga[1][:manga[1].find('&chapterNumber')]
                numero_cap = manga[2][:manga[2].find('&server')]
                self.manga_numcap  = numero_cap[:numero_cap.find('.00')]
                sesion_id = manga[n]
            except Exception,e:
                print e
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
            chapter_id=""
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
                    imagen = {}
                    for item in soup["pages"]:
                        try:
                            imagen[c] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                        except:      
                            imagen[c] = item["image_url"]
                        c=c+1
                except:
                    print "\n\nYou have to be premium user in order to download this chapter. "
                    return
                print u"\nDownloading %s - %s..."%(self.manga_titulo,self.manga_numcap)
                x = self.Directorio()
                if not x:
                    print "The folder %s - %s already exists and overwrite folders is deactivated."%(self.manga_titulo,self.manga_numcap)
                else:
                    while cc <= len(imagen):
                        sys.stdout.write('\rPage %d of %d' %(cc,len(imagen))) 
                        sys.stdout.flush()               
                        self.downloadImage(imagen[cc-1],str(cc))
                        cc = cc + 1
                    if self.zip:
                        self.zipmanga()
                    else:pass
        elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(manga|comipo|artistalley))?(\?volume\_id\=[0-9]+)$",self.url): #Crunchyroll por volumenes
            volume = re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(?:manga|comipo|artistalley))?(\?volume\_id\=([0-9]+))$",self.url) 
            try:
                html= self.download()
                soup = BeautifulSoup(html)
                manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
                manga = manga.split("=")
                n = len(manga)-1
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
                self.manga_numcap = capitulo[c].replace(".00","")
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
                imagen = {}
                self.manga_cover = ""
                if cv == True:
                    if not self.manga_vol == "0":
                        self.manga_cover = soup["volume"].pop("encrypted_image_url")
                    cv = False
                for item in soup["pages"]:
                    try:
                        imagen[c2] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                    except:      
                        imagen[c2] = item["image_url"]
                    c2=c2+1
                x = self.Directorio()
                cc = 1
                if not x:
                    print "The folder %s - %s already exists and overwrite folders is deactivated."%(self.manga_titulo,self.manga_numcap)
                    os.chdir(self.directorio)
                else:
                    while cc <= len(imagen):     
                        sys.stdout.write('\rPage %d of %d' %(cc,len(imagen)))
                        sys.stdout.flush()
                        self.downloadImage(imagen[cc-1],str(cc))
                        cc = cc + 1
                        sleep(0.25)       
                    if self.manga_vol == "0" and self.zip:
                        self.zipmanga() 
                    os.chdir(self.directorio)
                    rr +=1
                c = c+1
            if self.zip and self.manga_vol != "0" and rr > 0:
                self.zipmanga() 
            else:pass
        elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics\/(manga|comipo|artistalley)\/[a-z0-9\-]+\/)(volumes)$",self.url): #Crunchyroll por serie entera
            html= self.download(self.url)
            soup = BeautifulSoup(html)
            serie_id = soup.find(u"span",{u"id":u"sharing_add_queue_button"}).get(u"group_id")
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
                n = len(sesion_id)-1
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
                    self.manga_numcap = capitulo[c].replace(".00","")
                    print "\n\n%s chapters %d of %d: Downloading chapter %s"%(self.manga_titulo,c+1,len(capitulo),self.manga_numcap)
                    url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id[c]+"&auth="+cr_auth
                    html= self.download(url_capitulo)
                    soup = json.loads(html)
                    c2=0
                    imagen = {}
                    for item in soup["pages"]:
                        try:
                            imagen[c2] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                        except:      
                            imagen[c2] = item["image_url"]
                        c2=c2+1
                    x = self.Directorio()
                    cc = 1
                    if not x:
                        print "\nThe folder %s - %s already exists and overwrite folders is deactivated."%(self.manga_titulo,self.manga_numcap)
                        c = c+1
                    else:
                        while cc <= len(imagen):
                            sys.stdout.write('\rPage %d of %d' %(cc,len(imagen)) )
                            sys.stdout.flush()
                            self.downloadImage(imagen[cc-1],str(cc))
                            cc = cc + 1
                        c = c+1
                    os.chdir(self.directorio)
                    if self.zip and cc > 1:
                        self.zipmanga() 
                    else:pass   
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
                self.url = enlaces[c-1].replace("\n","")
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
            self.url = url_serie[i]
            self.CrunchyManga()
            i+=1        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url", type=str,help="Crunchyroll Link. if you get an error, try using double quotation marks (\")")
    parser.add_argument("-l","--login",nargs = 2, help="Crunchyroll login: -l User password. if your password has a blank, use double quotation marks (\"). Example: \"This is a password.\"")
    arg = parser.parse_args()
    Manga = MangaDownloader()
    def principal():
        seleccion = 0
        if arg.url:
            Manga.mangaurl(arg.url)
            Manga.CrunchyManga()
        elif arg.login:
            usuario = arg.login[0]
            password = arg.login[1]
            Manga.login(usuario, password)
        else:
            print "\nOptions:"
            print "1.- Download\n2.- Download pack\n3.- Login \n4.- Download ALL MANGAS from crunchyroll \n5.- About \n0.- Exit"
            try:
                seleccion = int(input("> "))
            except:
                print "The option you entered is wrong."
                principal()
            if seleccion == 1:
                url = raw_input("Link: ")
                if not url.replace(" ","") == "":
                    Manga.mangaurl(url)
                    Manga.CrunchyManga()
                principal()
            elif seleccion == 2 :
                Manga.PaqueteEnlace()
                principal()
            elif seleccion == 3:
                usuario = raw_input(u"User: ")
                password = raw_input(u"Password: ")
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
                print "ERROR: The option you entered is wrong."
                principal()
    def iniciar ():
        try:
            principal()
        except KeyboardInterrupt:
            iniciar ()
        except Exception,e:
            print e.message
    iniciar()
