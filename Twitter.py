from requests_oauthlib import OAuth1Session
import json
import requests
import os.path

keys = {
    "CK":'',
    "CS":'',
    "AT":'',
    "AS":''
    }
class Twitter:
    def __init__(self, userID):
        self.userID = userID
        self.sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])
    
    # ユーザのTLを取得
    def getTimeLine(self):
        TL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {
            "screen_name":self.userID,
            "count":20,
            "include_entities" : True,
            "exclude_replies" : True,
            "include_rts" : False
        }
        req = self.sess.get(TL, params=params)
        timeline = json.loads(req.text)
        return timeline

    # ツイートからメディアのURLを取得
    def getMediaUrls(self, tweet):
        pic_urls = []
        if "extended_entities" in tweet:
            image_list = tweet['extended_entities']['media']
            for image in image_list:
                image_url = image['media_url']
                pic_urls.append(image_url + ":large")
        return pic_urls

    # 写真のみのページから写真をダウンロードし、その保存場所パスを返す
    def downloadImage(self, url):
        if (os.path.exists('download_images') == False):
            os.mkdir('download_images')
        if (os.path.exists('download_images/tw_' + self.userID) == False):
            os.mkdir('download_images/tw_' + self.userID)
        dst_path = os.path.join('download_images/tw_' + self.userID, os.path.basename(url)[0:os.path.basename(url).find('.jpg')] + '.jpg')
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(dst_path, 'wb') as f:
                f.write(r.content)
            print(url + 'を保存しました。')
        return os.path.abspath(dst_path)
