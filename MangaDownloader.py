# -*- coding: cp1252 -*-
'''
Script realizado por Miguel A(Touman).
Pueden usarlo como mejor les convenga, editarlo para que se adapte sus necesidades y todo lo demás que se les ocurra.
Solo recuerden dejar los creditos.
Crunchyroll MangaDownloader.

Si tienes alguna duda del funcionamiento del programa no dudes en enviarmela a touman@hotmail.com

Beautifulsoup es la única librería externa usada.
'''
from itertools import izip, cycle
import re
from BeautifulSoup import BeautifulSoup
import urllib2
import os
from urlparse import urlparse
global url
import json
import cookielib
import urllib
from os import path
directorioOriginal = os.getcwd()
def xord(bytear, key):
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(bytear, cycle(key)))
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
                    print "Error al descargar la imagen."
    f = open(image,'wb')
    f.write(xord(descarga, 'B'))
    f.close()
def Directorio(titulo,nombrecap,vol,cover):
    nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
    for i in nopermitido:
        try:
            titulo = titulo.replace(i,"")
        except: pass
    if os.path.isdir("Manga"):
        os.chdir("Manga")
    else:
        os.mkdir("Manga")
        os.chdir("Manga")
    if os.path.isdir(titulo):
        os.chdir(titulo)
    else:
        os.mkdir(titulo)
        os.chdir(titulo)
##
    if not vol == "0":
        if os.path.isdir(titulo + " - Vol." + vol):
            os.chdir(titulo + " - Vol." + vol)
        else:
            os.mkdir(titulo + " - Vol." + vol)
            os.chdir(titulo + " - Vol." + vol)
        if not cover == "":
            downloadImage(cover,"Cover - Vol." + vol)     
##
    if os.path.isdir(titulo + " - " + nombrecap):
        os.chdir(titulo + " - " + nombrecap)
    else:
        os.mkdir(titulo + " - " + nombrecap)
        os.chdir(titulo + " - " + nombrecap)
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
            print 'Te has logeado satisfactoriamente.\n\n'
            cookies.save()
    else:
            print 'Ha fallado el logeo, verifica que estás introduciendo un usuario y una contraseña correcta, luego intenta una vez más\n\n'
def MangaDownloader(url):    
    cc = 1    
    if url[0:8] == "https://":
        url = 'http://' + url[8:]
    if url[0:7] != 'http://':
        url = 'http://' + url
    if re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read(\/manga)?\?volume\_id\=[0-9]+&chapter\_num\=[0-9]+\.[0-9])",url): #Crunchyroll por episodios.
        try:
            print "Analizando URL..."
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
            print "El enlace ciertamente es de Crunchyroll, pero parece que no está correcto."
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
            print u"\nEl capitulo %s no está disponible. Intenta más tarde.\n"%numero_cap.replace(".00","")
            return
        else:
            url_capitulo = "http://api-manga.crunchyroll.com/chapter?session_id="+sesion_id+"&auth="+cr_auth+"&format=json&version=0&chapter_id="+chapter_id
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
                print "\n\nTienes que ser usuario premium para poder bajar este capitulo.\n ¿Lo eres? Entonces logeate."
                return
            print u"\nComenzando a descargar %s - %s..."%(titulo,nombrecap)
            Directorio(titulo,nombrecap,"0","")
            while cc <= len(imagen):     
                print "Descargando imagen %d/%d \n"%(cc,len(imagen))                
                downloadImage(imagen[cc-1],str(cc))
                cc = cc + 1
    elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/manga)?(\?volume\_id\=[0-9]+)$",url): #Crunchyroll por volumenes
        volume = re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics_read)(\/manga)?(\?volume\_id\=([0-9]+))$",url) 
        try:
            print "Analizando URL..."            
            html= download(url)
            soup = BeautifulSoup(html)
            manga = soup.find("object",{u"id":u"showmedia_videoplayer_object"}).find("embed",{u"type":u"application/x-shockwave-flash"}).get("flashvars")
            manga = manga.split("=")
            n = len(manga)-1
            serie_id = manga[1][:manga[1].find('&chapterNumber')]
            sesion_id = manga[n]
        except:
            print "El enlace ciertamente es de Crunchyroll, pero parece que no está correcto."
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
            print "Para descargar por volumenes en crunchyroll tienes que ser usuario premium. Los usuarios no premium solo pueden descargar el último episodio."
            return
        c = 0
        cv = True
        while c < len(capitulo):
            nombrecap = capitulo[c].replace(".00","")
            print "Descargando capitulo %d/%d"%(c+1,len(capitulo))
            if volumen == "0":
                print "Descargando %s - %s"%(titulo,nombrecap)
            else:
                print "Descargando %s Vol.%s ch.%s"%(titulo,volumen,nombrecap)
            url_capitulo = "http://api-manga.crunchyroll.com/chapter?session_id="+sesion_id+"&auth="+cr_auth+"&format=json&version=0&chapter_id="+chapter_id[c]
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
            Directorio(titulo,nombrecap,volumen,volcover)
            cc = 1
            while cc <= len(imagen):     
                print "Descargando imagen %d/%d"%(cc,len(imagen))
                downloadImage(imagen[cc-1],str(cc))
                cc = cc + 1
            c = c+1
            os.chdir(directorioOriginal)
    elif re.match(r"^(http:\/\/)(w{3}\.)?(crunchyroll\.com\/comics\/manga\/[a-z0-9\-]+\/)(volumes)$",url): #Crunchyroll por serie entera
        html= download(url)
        soup = BeautifulSoup(html)
        serie_id = soup.find(u"span",{u"id":u"sharing_add_queue_button"}).get(u"group_id")
        volumen_id = soup.find(u"li",{u"class":u"queue-item volume-simul"}).get(u"volume_id")
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
            print "Para descargar series completas en crunchyroll tienes que ser usuario premium. Los usuarios no premium solo pueden descargar el último episodio."
            return
        c = 0
        while c < len(capitulo):
            nombrecap = capitulo[c].replace(".00","")
            print "Descargando capitulo %d/%d"%(c+1,len(capitulo))
            print "Descargando %s capitulo %s"%(titulo,nombrecap)
            url_capitulo = "http://api-manga.crunchyroll.com/chapter?session_id="+sesion_id+"&auth="+cr_auth+"&format=json&version=0&chapter_id="+chapter_id[c]
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
            Directorio(titulo,nombrecap,"0","")
            while cc <= len(imagen):     
                print "Descargando imagen %d/%d"%(cc,len(imagen))
                downloadImage(imagen[cc-1],str(cc))
                cc = cc + 1
            c = c+1
            os.chdir(directorioOriginal)
    else:
        print "ERROR: El enlace ingresado no es de Crunchyroll/Manga"    
    os.chdir(directorioOriginal)
def PaqueteEnlace():
    c = 1
    try:
            with open('enlaces.txt'): pass
    except IOError:
            enlaces = open('enlaces.txt','w')
            enlaces.close()
##            print "The file \"enlaces.txt\" has been created. Please edit it with your links(One per line)."
            print "El archivo \"enlaces.txt\" ha sido creado. Por favor editalo con tus enlaces(Uno por linea)."
            return
    enlaces = open('enlaces.txt','r')
    enlaces = enlaces.readlines()
    n_len = len(enlaces)
    if n_len > 0:
        while c <= n_len:
            print "Descargando enlace %d/%d"%(c,n_len)
            MangaDownloader(u""+str(enlaces[c-1].replace("\n","")))
            c = c + 1
    else:
##        print "The file \"enlaces.txt\" is empty. Please edit it with your links(One per line)."
        print "El archivo \"enlaces.txt\" está vacío. Por favor editalo con tus enlaces(Uno por linea)."
def principal():
    print "Selecciona una opción"
##    print "1.- Download\n2.- Download Pack\n3.- Login \n0.- Exit"
    print "1.- Descargar\n2.- Descargar paquete de enlaces\n3.- Login \n0.- Exit"
    try:
        seleccion = int(input("> "))
    except:
        print "Has introducido una opción incorrecta."
        principal()
    if seleccion == 1:
        print "Introduce el enlace"
        url=u""+raw_input(">")
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
    elif seleccion == 0:
        SystemExit()
    else:
        print "ERROR: El numero de opción ingresada es incorrecta. Intenta una vez más"
        principal()
principal()
