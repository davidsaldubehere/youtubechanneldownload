from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import youtube_dl
from bs4 import BeautifulSoup as bs
from os import path
import time
if path.exists('links.txt'):
    print('skipping fetching links')
else:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=webdriver.Chrome(options=options, executable_path='chromedriver.exe')
    driver.get("https://www.youtube.com/c/DudePerfect/videos")
    driver.set_window_size(1280,1024)
#scroll to the bottom of the page    
def scrollToBottom():
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    time.sleep(2)
    last_height = driver.execute_script(f"return document.getElementById('content').scrollHeight")
    print('downloading full page')
    while True:
        # Scroll down to bottom
        driver.execute_script(f"window.scrollTo(0, document.getElementById('content').scrollHeight)")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(f"return document.getElementById('content').scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return bs(driver.page_source, 'html.parser')
def storeLinks(soup):
    links=[]
    for link in soup.find_all('a'):
        if (link.get('href') != None):
            if("watch" in link.get("href")):
                links.append(link.get("href"))
                #open("links.txt", "a").write("\n" + link.get("href"))
    seen = set()
    result = []
    for item in links:
        if item not in seen:
            seen.add(item)
            result.append(item)
    for i in result:
        open("links.txt", "a").write("\n" + i)
def downloadLinks():
    #youtube-dl has no freaking documentation so im lucky I even got this far
    ydl_opts = {
        'format': '22',
        'outtmpl': "%(title)s%(upload_date)s.mp4"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for i in open("links.txt", "r").readlines()[::-1]:
            try:
                ydl.download([str('www.youtube.com' + i)])
            except Exception:
                print('failed')

if path.exists('links.txt'):
    downloadLinks()
else:
    print('getting links')
    html = scrollToBottom()
    storeLinks(html)
    downloadLinks()