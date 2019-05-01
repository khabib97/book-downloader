# Import libraries
import requests
import wget
import urllib
import time
import os
import array as arr
from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
url = 'https://doc.lagout.org/'

validExtension = {'pdf','PDF','epub','EPUB','mobi','MOBI','flv','FLV',
                    'awz3','AWZ3','chm','CHM','zip','ZIP','mp4','MP4',
                    'xml','XML','jpg','jpeg','opf','png','djvu'}

rootDirectory = "Books"

def generateFolder(dirName):
    try:
        if not os.path.exists(dirName):
            os.makedirs(dirName)
            print("Directory " , dirName ,  " Created ") 
    except Exception :
        print("Error creating folder")

def isDownloadable (fileExt) :
    return fileExt in validExtension

def getExtension(url):
    return url.split('.')[-1]

def getDirectoryName(url):
    _dir = url.split('/')
    dir_names = _dir[3:-1]
    dir_path = 'Books'
    for i in range(0,len(dir_names)) :
        dir_path += '/'+ dir_names[i]
    
    print(dir_path)
    generateFolder(dir_path)
    return dir_path


def downloader(url):
    fileExt = getExtension(url)
    if isDownloadable(fileExt):
        decodedURL = urllib.parse.unquote(url)
        dir_path = getDirectoryName(decodedURL)
        #wget.download(decodedURL, dir_path)
        print("Download: "+ decodedURL)
    else :
        response = requests.get(url)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in range(1,len(soup.findAll('a'))):
            current_a = soup.findAll('a')[i]['href']
            if "http://" in current_a or "https://" in current_a :
                print("BAD PARSING" + current_a)
            else :
                current_url  = url + current_a
                print("Recursive call :" + current_url)
                downloader(current_url)


#generateFolder(rootDirectory)
downloader(url)