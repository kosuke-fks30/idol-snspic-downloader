from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os.path

class Instagram:
    def __init__(self, userID):
        self.userID = userID
        self.options = Options()
        self.options.set_headless(True)
        self.driver = webdriver.Chrome(chrome_options=self.options)

    # ユーザーページから写真ページのURL一覧を取得
    def getImageUrlList(self):
        url_list = []
        self.driver.get("https://www.instagram.com/" + self.userID + "/")

        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        image_urls = soup.select("div.v1Nh3.kIKUG._bz0w a")
        for img_url in image_urls:
            url_list.append(img_url['href'])
        
        return url_list

    # 写真ページから写真のみ表示されるページを取得
    def getOnlyImageUrls(self, image_url):
        url_list = []
        self.driver.get("https://www.instagram.com" + image_url)
        
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        image_urls = soup.select("div.KL4Bh img")
        for img_url in image_urls:
            url_list.append(img_url['src'])

        return url_list

    # 写真のみのページから写真をダウンロードし、その保存場所パスを返す
    def downloadImage(self, url):
        if (os.path.exists('download_images') == False):
            os.mkdir('download_images/')
        if (os.path.exists('download_images/ig_' + self.userID) == False):
            os.mkdir('download_images/ig_' + self.userID)
        dst_path = os.path.join('download_images/ig_' + self.userID, os.path.basename(url)[0:os.path.basename(url).find('.jpg')] + '.jpg')
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(dst_path, 'wb') as f:
                f.write(r.content)
            print(url + 'を保存しました。')
        return dst_path
