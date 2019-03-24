from Instagram import Instagram
from Twitter import Twitter
from Dropbox import Dropbox
from Xml import Xml
import os
import logging
from datetime import datetime

INSTAGRAM_USER_ID = 'fukasemio'
TWITTER_USER_ID = 'fukasemio330'
USER_NAME = '深瀬美桜'

def getInstagramImages():
    instagram = Instagram(INSTAGRAM_USER_ID)
    dropbox = Dropbox(USER_NAME, 'instagram')
    xml = Xml(INSTAGRAM_USER_ID, 'instagram')
    
    xml.createXmlFile()
    dropbox.makeDropboxFolder()
    
    url_list = instagram.getImageUrlList()
    not_download_url_list = xml.compareXmlAndWeb(url_list)
    
    for url in not_download_url_list:
        img_urls = instagram.getOnlyImageUrls(url)
        for img in img_urls:
            path = instagram.downloadImage(img)
            dropbox.uploadPicture(path)
            xml.insertPicUrl(url)
            os.remove(path)

def getTwitterImages():
    twitter = Twitter(TWITTER_USER_ID)
    dropbox = Dropbox(USER_NAME, 'twitter')
    xml = Xml(TWITTER_USER_ID, 'twitter')
    
    xml.createXmlFile()
    dropbox.makeDropboxFolder()
    
    timeline = twitter.getTimeLine()
    url_list = []
    for tweet in timeline:
        img_url = twitter.getMediaUrls(tweet)
        if img_url is not None:
            url_list.extend(img_url)
    not_download_url_list = xml.compareXmlAndWeb(url_list)

    for url in not_download_url_list:
        path = twitter.downloadImage(url)
        dropbox.uploadPicture(path)
        xml.insertPicUrl(url)
        os.remove(path)

if __name__ == "__main__":
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        getInstagramImages()
        getTwitterImages()
    except Exception as e:
        for msg in e.args:
            logging.error(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ':' + msg)
