#!/usr/bin/env python
# -*- coding: cp1252 -*-
about='''
Crunchyroll MangaDownloader v0.3 (Crunchymanga v0.3 for short).
All credit goes to Miguel A(Touman).
You can use this script as suits you. Just do not forget to leave the credit.

If you are in any doubt whatsoever about how to use this script do not hesitate to tell me. Contact me at 7ouman@gmail.com and I'll try to respond as soon as possible.

Beautifulsoup is the only external library used.

https://github.com/7ouma/CrunchyManga
'''

changelog='''
CrunchyManga 0.3:
	- Added support to ComicPo! and Artist Alley.
	- The last regex i added was redundant. Fixed.
	- Added config file, this file is created once you run the script. You can edit as you like, but, if you edit it while the script is running, please restart the script. The options:
		* dir: Your directory, if the directory doesn't exist, the script will take the script folder as default. Please note that you'll need to use double \. Example: "dir": "c:\\manga" instead of "dir":"c:\manga"
		* zip: I think i don't have to say what does this option do. values: true/false
		* download_volumes: this only works with complete series downloads. if this option is true(activated), the script will download all the volumes available with covers and so, then the rest of the individial episodes.values: true/false
		* overwrite_folders: if false and the script detects that the chapter folder you are downloading exists, the download will stop. If you're downloading a whole series/volume, the script will skip the chapter and continue. Please, note that if the chapter is incomplete, you know. (Doesn't work with zip files yet). values: true/false
		* delete_files_after_zip: Only works if zip is activated, once the file is downloaded and zipped, the folder will be deleted only remaining the zip file.values: true/false
	- Added some console parameters. Don't worry about this, you can use the script as always, just clicking the mangadownloader.py file. This is just a test, that's why there are only two commands plus the help:
		* mangadownloader.py -u link / mangadownloader.py --url link. Please note that you'll need to use double quotation marks in some cases, to avoid error with the & from the url/link.
		* mangadownloader.py -l user password / mangadownloader.py --link user password. Please note that you'll need to use double quotation marks in some cases, to avoid error with blanks and some symbols.
		* mangadownloader.py -h / mangadownloader.py --help. Explains the script (parameters) usage.
	- Added "Download ALL MANGAS from crunchyroll" option. I think i don't have to say what does this option do.
'''
import shutil
import sys
from time import sleep
from itertools import izip, cycle
import re
try:
    from BeautifulSoup import BeautifulSoup
except:
    print "You need BeautifulSoup. https://github.com/7ouma/CrunchyManga"
    SystemExit()
import urllib2
import os
from urlparse import urlparse
import json
import cookielib
import urllib
from os import path
import argparse
from zipfile import *
global url

###Parser
parser = argparse.ArgumentParser()
parser.add_argument("-u","--url", type=str,help="Crunchyroll Link. if you get an error, try using double quotation marks (\")")
parser.add_argument("-l","--login",nargs = 2, help="Crunchyroll login: -l User password. if your password has a blank, use double quotation marks (\"). Example: \"This is a password.\"")
arg = parser.parse_args()
directorioOriginal = os.getcwd()
####End Parser

###Default Config
def config():
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
###End config

###Decrypt
def xord(bytear, key):
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(bytear, cycle(key)))
###End Decrypt

#Zip Manga
def zipmanga(path,filename):
    os.chdir(path)
    def zipdir(path, zip):
        for root, dirs, files in os.walk(path):
            for file in files:
                zip.write(os.path.join(root, file))
    print "\nCreating %s.zip\n"%(filename)
    zip_archive = ZipFile(filename+".zip", "w")
    zipdir(filename,zip_archive)
    zip_archive.close()
    os.chdir(directorioOriginal)
    if cdelete:
        shutil.rmtree(path+"\\"+filename)
#End Zip manga
def downloadImage(imageUrl,image):
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
                cn = cn + 1
                if cn == 9:
                    print "\nError downloading the image.\n"
                else:
                    print "\n"
                    for i in range(31):
                        sys.stdout.write('\rFailed to download image. Trying again in %d' %(30-i))
                        sys.stdout.flush()
                        sleep(1)
    f = open(image,'wb')
    f.write(xord(descarga, 'B'))
    f.close()

   
def Directorio(titulo,nombrecap,vol,cover):
    global filedir, filename, filevol
    nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
    for i in nopermitido:
        try:
            titulo = titulo.replace(i,"")
        except: pass
    directory = cdir
    whi = True
    while (whi):
        if directory == "default":
            if os.path.isdir("Manga"):
                os.chdir("Manga")
            else:
                os.mkdir("Manga")
                os.chdir("Manga")
            whi = False
        else:
            if os.path.isdir(directory):
                os.chdir(directory)
                whi = False
            else:
                print "\n%s doesn't exist. Using dafault folder."%(directory)
                directory = "default"  
    if os.path.isdir(titulo):
        os.chdir(titulo)
    else:
        os.mkdir(titulo)
        os.chdir(titulo)
    filedir = os.getcwd()
##
    filevol = titulo + " - Vol." + vol
    if not vol == "0":
        
        if os.path.isdir(filevol):
            os.chdir(filevol)
        else:
            os.mkdir(filevol)
            os.chdir(filevol)
        if not cover == "":
            downloadImage(cover,"Cover - Vol." + vol)
    
##
    filename = titulo + " - " + nombrecap        
    if crewrite and os.path.isdir(filename):
        os.chdir(filename)
        return True
    elif not os.path.isdir(filename):
        os.mkdir(filename)
        os.chdir(filename)
        return True
    else:
        return False
    
def download(url):
    try:
            with open('cookies.txt'): pass
    except IOError:
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
def login(usuario,password):
    try:
            with open('cookies.txt'): pass
    except IOError:
            cookies = cookielib.MozillaCookieJar('cookies.txt')
            cookies.save()
    url_ = 'https://www.crunchyroll.com/?a=formhandler'
    data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : usuario, 'password' : password}
    cookies = cookielib.MozillaCookieJar('cookies.txt')
    cookies.load() 
    opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel=0),
        urllib2.HTTPSHandler(debuglevel=0),
        urllib2.HTTPCookieProcessor(cookies))
    opener.addheaders =[('Referer', "http://www.crunchyroll.com"),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
    req = opener.open(url_, urllib.urlencode(data))
    url = "http://www.crunchyroll.com"
    req = opener.open(url)
    html = req.read()
    if re.search(usuario+'(?i)',html):
            print 'You have been successfully logged in.\n\n'
            cookies.save()
    else:
            print 'Failed to verify your username and/or password. Please try again.\n\n'
def MangaDownloader(url):    
    cc = 1
    if url[0:8] == "https://":
        url = 'http://' + url[8:]
    if url[0:7] != 'http://':
        url = 'http://' + url
    if re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read(\/(manga|comipo|artistalley))?\?(volume\_id|series\_id)\=[0-9]+&chapter\_num\=[0-9]+\.[0-9])",url): #Crunchyroll por episodios.
        try:
            print "Analyzing link..."
            html= download(url)
            soup = BeautifulSoup(html)
            titulo = soup.find(u"span", {u"itemprop":u"title"}).text
            titulo = titulo.replace(':',' ')
            manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
            manga = manga.split("=")
            n = len(manga)-1
            serie_id = manga[1][:manga[1].find('&chapterNumber')]
            numero_cap = manga[2][:manga[2].find('&server')]
            nombrecap = numero_cap[:numero_cap.find('.00')]
            sesion_id = manga[n]
        except:
            print "The link is certainly from Crunchyroll, but it seems that it's not correct. Verify it and try again."
            return
        cr_auth = "http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json"
        html = download(cr_auth)
        try:
            soup = json.loads(html)
            cr_auth=""
            for item in soup["data"]["auth"]:
                cr_auth=cr_auth+item            
        except:
            cr_auth = "null"            
        url_serie = "http://api-manga.crunchyroll.com/chapters?series_id="+serie_id
        html= download(url_serie)
        soup = json.loads(html)
        chapter_id=""
        for item in soup["chapters"]:
            if item["number"] == str(numero_cap):
                chapter_id = item["chapter_id"]
        if chapter_id == "":
            print u"\nThe chapter %s is not currently unavailable, try again later.\n"%numero_cap.replace(".00","")
            return
        else:
            url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id+"&auth="+cr_auth
            try:
                html= download(url_capitulo)
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
            print u"\nDownloading %s - %s..."%(titulo,nombrecap)
            x = Directorio(titulo,nombrecap,"0","")
            if not x:
                print "The folder %s - %s already exists and overwrite folders is deactivated."%(titulo,nombrecap)
            else:
                while cc <= len(imagen):
                    sys.stdout.write('\rPage %d of %d' %(cc,len(imagen))) 
                    sys.stdout.flush()               
                    downloadImage(imagen[cc-1],str(cc))
                    cc = cc + 1
                if czip:
                    zipmanga(filedir,filename)
                
                else:pass
    elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(manga|comipo|artistalley))?(\?volume\_id\=[0-9]+)$",url): #Crunchyroll por volumenes
        volume = re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/(?:manga|comipo|artistalley))?(\?volume\_id\=([0-9]+))$",url) 
        try:
            print "Analyzing link..."
            html= download(url)
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
        html= download(url_serie)
        soup = json.loads(html)
        titulo = soup["series"].pop("locale").pop("enUS").pop("name")
        capitulo = []
        chapter_id = []
        volume = volume.groups()
        volume = volume[5]
        for item in soup["chapters"]:
            if item.pop("volume_id") == volume:
                chapter_id.append(item.pop("chapter_id")) 
                capitulo.append(item.pop("number"))
                volumen = item.pop("volume_number")
        cr_auth = "http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json"
        html = download(cr_auth)
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
        if volumen == "0":
            print "Downloading individual chapters"
        while c < len(capitulo):
            nombrecap = capitulo[c].replace(".00","")
            if volumen == "0":
                print "\n%s: Chapters %d/%d"%(titulo,c+1,len(capitulo))
                print "\nDownloading %s - %s"%(titulo,nombrecap)
            else:
                print "\n%s Vol.%s: Chapters %d/%d"%(titulo,volumen,c+1,len(capitulo))
                print "\nDownloading %s Vol.%s ch.%s"%(titulo,volumen,nombrecap)
            url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id[c]+"&auth="+cr_auth
            html= download(url_capitulo)
            soup = json.loads(html)
            c2=0
            imagen = {}
            volcover = ""
            if cv == True:
                if not volumen == "0":
                    volcover = soup["volume"].pop("encrypted_image_url")
                cv = False
            for item in soup["pages"]:
                try:
                    imagen[c2] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                except:      
                    imagen[c2] = item["image_url"]
                c2=c2+1
            x = Directorio(titulo,nombrecap,volumen,volcover)
            cc = 1
            if not x:
                print "The folder %s - %s already exists and overwrite folders is deactivated."%(titulo,nombrecap)
                os.chdir(directorioOriginal)
            else:
                while cc <= len(imagen):     
                    sys.stdout.write('\rPage %d of %d' %(cc,len(imagen)))
                    sys.stdout.flush()
                    downloadImage(imagen[cc-1],str(cc))
                    cc = cc + 1
                    sleep(0.25)
                if volumen == "0" and czip:
                    zipmanga(filedir,filename) 
                os.chdir(directorioOriginal)
                rr +=1
            c = c+1
        if czip and volumen != "0" and rr > 0:
            zipmanga(filedir,filevol) 
        else:pass
    elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics\/(manga|comipo|artistalley)\/[a-z0-9\-]+\/)(volumes)$",url): #Crunchyroll por serie entera
        html= download(url)
        soup = BeautifulSoup(html)
        serie_id = soup.find(u"span",{u"id":u"sharing_add_queue_button"}).get(u"group_id")
        if cdownload_v:
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
                MangaDownloader("http://www.crunchyroll.com/comics_read/manga?volume_id="+vols)
                i+=1
        else:       
            volumen_id = soup.find(u"li",{ur"class":re.compile(u"queue-item volume-")}).get(u"volume_id")    
            url_vol = "http://www.crunchyroll.com/comics_read/manga?volume_id="+volumen_id
            html= download(url_vol)
            soup = BeautifulSoup(html)
            sesion_id = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
            sesion_id = sesion_id.split("=")
            n = len(sesion_id)-1
            sesion_id = sesion_id[n]
            url_serie = "http://api-manga.crunchyroll.com/chapters?series_id="+serie_id
            html= download(url_serie)
            soup = json.loads(html)
            titulo = soup["series"].pop("locale").pop("enUS").pop("name")
            capitulo = []
            chapter_id = []
            for item in soup["chapters"]:
                chapter_id.append(item.pop("chapter_id")) 
                capitulo.append(item.pop("number")) 
            cr_auth = "http://api-manga.crunchyroll.com/cr_authenticate?auth=&session_id="+sesion_id+"&version=0&format=json"
            html = download(cr_auth)
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
                nombrecap = capitulo[c].replace(".00","")
                print "\n\n%s chapters %d of %d: Downloading chapter %s"%(titulo,c+1,len(capitulo),nombrecap)
                url_capitulo = "http://api-manga.crunchyroll.com/list_chapter?session_id="+sesion_id+"&chapter_id="+chapter_id[c]+"&auth="+cr_auth
                html= download(url_capitulo)
                soup = json.loads(html)
                c2=0
                imagen = {}
                for item in soup["pages"]:
                    try:
                        imagen[c2] = item["locale"].pop("enUS").pop("encrypted_composed_image_url")
                    except:      
                        imagen[c2] = item["image_url"]
                    c2=c2+1
                x = Directorio(titulo,nombrecap,"0","")
                cc = 1
                if not x:
                    print "\nThe folder %s - %s already exists and overwrite folders is deactivated."%(titulo,nombrecap)
                    c = c+1
                else:
                    while cc <= len(imagen):
                        sys.stdout.write('\rPage %d of %d' %(cc,len(imagen)) )
                        sys.stdout.flush()
                        downloadImage(imagen[cc-1],str(cc))
                        cc = cc + 1
                    c = c+1
                os.chdir(directorioOriginal)
                if czip and cc > 1:
                    zipmanga(filedir,filename) 
                else:pass
            
    else:
        print "ERROR: The link is not from Crunchyroll/Manga"    
    os.chdir(directorioOriginal)
def PaqueteEnlace():
    c = 1
    try:
            with open('links.txt'): pass
    except IOError:
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
            MangaDownloader(u""+str(enlaces[c-1].replace("\n","")))
            c = c + 1
    else:
        print "The file \"links.txt\" is empty. Please edit it with your links(One per line)."


def AllMangas():
    html = download("http://www.crunchyroll.com/comics/manga/alpha?group=all")
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
        MangaDownloader(url_serie[i])
        i+=1        
def principal():
    if arg.url:
        MangaDownloader(arg.url)
    elif arg.login:
        usuario = arg.login[0]
        password = arg.login[1]
        login(usuario, password)
    else:
        print "\nOptions:"
        print "1.- Download\n2.- Download pack\n3.- Login \n4.- Download ALL MANGAS from crunchyroll \n5.- About \n0.- Exit"
        try:
            seleccion = int(input("> "))
        except:
            print "The option you entered is wrong."
            principal()
        if seleccion == 1:
            url=u""+raw_input("Link: ")
            MangaDownloader(url)
            principal()
        elif seleccion == 2 :
            PaqueteEnlace()
            principal()
        elif seleccion == 3:
            usuario = raw_input(u"User: ")
            password = raw_input(u"Password: ")
            login(usuario, password)
            principal()
        elif seleccion == 4:
            AllMangas()
            principal()
        elif seleccion == 5:
            print about
            principal()
        elif seleccion == 0:
            SystemExit()
        else:
            print "ERROR: The option you entered is wrong."
            principal()
##########    
def read():
    try:
        with open('config.json') as config_file:
            global cdir, czip, cdownload_v, crewrite, cask,cdelete
            x = json.load(config_file)
            cdir = x["dir"]
            czip = x["zip"]
            cdownload_v = x["download_volumes"]
            crewrite = x["overwrite_folders"]
            cdelete = x["delete_files_after_zip"]
            if czip == True or czip == False: pass
            else: config()
            if cdownload_v == True or cdownload_v == False: pass
            else: config()
            if crewrite == True or crewrite == False: pass
            else: config()
            if cdelete == True or cdelete == False: pass
            else: config()
                
    except Exception,e:
        print "Error: ",e
        config()
read()
try:
    principal()
except KeyboardInterrupt:
    principal ()
except Exception,e:
    print e.message
