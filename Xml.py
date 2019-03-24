import xml.etree.ElementTree as et
import os.path

class Xml:
    
    def __init__(self, userID, sns):
        self.userID = userID
        self.sns = sns
    
    # XMLファイルを作成
    def createXmlFile(self):
        if(os.path.exists(self.userID + '_' + self.sns + '_DownloadUrls.xml') == False):
            root = et.Element('urls')
            tree = et.ElementTree(element=root)
            tree.write(self.userID + '_' + self.sns + '_DownloadUrls.xml', encoding='utf-8', xml_declaration=True)

    # XMLファイルを取得
    def getXmlFile(self):
        xml = et.parse(self.userID + '_' + self.sns + '_DownloadUrls.xml')
        return xml
    
    # XMLファイルとWebのURLリストを比較
    def compareXmlAndWeb(self, web_url_list):
        root = self.getXmlFile().getroot()
        xml_url_list = []
        for child in root:
            xml_url_list.append(child.text)
        return list(set(web_url_list) - set(xml_url_list))
    
    # 写真のURLをXMLファイルに追加
    def insertPicUrl(self, url):
        xml = self.getXmlFile()
        child = et.SubElement(xml.getroot(), 'url')
        child.text = url
        tree = et.ElementTree(xml.getroot())
        tree.write(self.userID + '_' + self.sns + '_DownloadUrls.xml', encoding='utf-8', xml_declaration=True)
