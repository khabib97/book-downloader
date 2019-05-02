# Import libraries
import requests
import wget
import urllib
import os
import traceback
from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
url = 'https://doc.lagout.org/'

def isDownloadable (response_content_type) :
    return 'text/html' not in response_content_type

@DeprecationWarning
def getExtension(url):
    return url.split('.')[-1]

def generateFolder(dirName):
    try:
        if not os.path.exists(dirName):
            os.makedirs(dirName)
    except Exception:
        print("\nError creating folder...")
        traceback.print_exc() 

def getDirectory(url):
    try:
        splitedURL = url.split('/')
        dirPathArr = splitedURL[3:-1]
        dirPath = 'Books' #from current path
        for i in range(0,len(dirPathArr)) :
            dirPath += '/'+ dirPathArr[i]
    except Exception:
        dirPath = 'Books'
        print("Directory name cereation error...")
        traceback.print_exc()
        

    generateFolder(dirPath)
    return dirPath

def download(url,path):
    try :
        wget.download(url, path)
        print("\nDownload Complete: "+ url)
    except Exception:
        print("\nError downloading file "+ url + " ...")
        traceback.print_exc()

def downloader(url):
    response = requests.head(url)
    if response.status_code != 200 :
        print('Request failed') 
    elif isDownloadable(response.headers['Content-Type']) :
        decodedURL = urllib.parse.unquote(url)
        dirPath = getDirectory(decodedURL)
        download(decodedURL,dirPath)
    else :
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in range(1,len(soup.findAll('a'))):
            current_a = soup.findAll('a')[i]['href']
            if "http://" not in current_a or "https://" not in current_a :
                #print("BAD PARSING :" + current_a)
                current_url  = url + current_a
                #print("Recursive call :" + current_url)
                downloader(current_url) 

downloader(url)