# Import libraries
import requests
import wget
import urllib
import os
from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
url = 'https://doc.lagout.org/'

validExtension = {'pdf','PDF','epub','EPUB','mobi','MOBI','flv','FLV',
                    'awz3','AWZ3','chm','CHM','zip','ZIP','mp4','MP4',
                    'xml','XML','jpg','jpeg','opf','png','PNG','djvu','DJVU'}

def generateFolder(dirName):
    try:
        if not os.path.exists(dirName):
            os.makedirs(dirName)
    except Exception :
        print("Error creating folder")

def isDownloadable (fileExt) :
    return fileExt in validExtension

def getExtension(url):
    return url.split('.')[-1]

def getDirectory(url):
    splitedURL = url.split('/')
    dirPathArr = splitedURL[3:-1]
    dirPath = 'Books' #from current path
    for i in range(0,len(dirPathArr)) :
        dirPath += '/'+ dirPathArr[i]

    generateFolder(dirPath)
    return dirPath

def downloader(url):
    fileExt = getExtension(url)
    if isDownloadable(fileExt):
        decodedURL = urllib.parse.unquote(url)
        dirPath = getDirectory(decodedURL)
        wget.download(decodedURL, dirPath)
        print("\nDownload Complete: "+ decodedURL)
    else :
        response = requests.get(url)
        #print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in range(1,len(soup.findAll('a'))):
            current_a = soup.findAll('a')[i]['href']
            if "http://" not in current_a or "https://" not in current_a :
                #print("BAD PARSING :" + current_a)
                current_url  = url + current_a
                #print("Recursive call :" + current_url)
                downloader(current_url)

downloader(url)