##########imports##########
import requests
import json
import os
# 停止SSL報錯
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
###########################
# 解析JSON
###########################


class Dcard:
    def __init__(self):
        self.dSession = requests.session()

        self.mainUrl = "https://www.dcard.tw/_api/forums/"

        self.forums = ''
        self.popular = ''
        self.limit = 0

        self.infomation = {
            'f': {
                'likeCount': 0,
                'commentCount': 0
            },
            'm':
                {
                    'likeCount': 0,
                    'commentCount': 0
            },
            'media': {
                'zero':
                {
                    'likeCount': 0,
                    'commentCount': 0
                },
                'notzero':
                {
                    'likeCount': 0,
                    'commentCount': 0
                }
            },
            'total':
                {
                    'forums': '',
                    'likeCount': 0,
                    'commentCount': 0
            }
        }

        self.forumsData = list()

    def showMessage(self):
        data = self.forumsData
        popular = self.popular
        limit = self.limit
        forums = self.forums
        print("[Info]板塊:{}|熱門:{}|欲擷取筆數:{}|總共抓取{}筆資料".format(
            forums, popular, limit, len(data)))

        self.infomation['total']['forums'] = forums

        for singleData in self.forumsData:
            # total
            self.infomation['total']['likeCount'] += int(
                singleData['likeCount'])
            self.infomation['total']['commentCount'] += int(
                singleData['commentCount'])
            # 男性
            if singleData['gender'] == "M":
                self.infomation['m']['likeCount'] += int(
                    singleData['likeCount'])
                self.infomation['m']['commentCount'] += int(
                    singleData['commentCount'])
            # 女性
            elif singleData['gender'] == "F":
                self.infomation['f']['likeCount'] += int(
                    singleData['likeCount'])
                self.infomation['f']['commentCount'] += int(
                    singleData['commentCount'])
            # 附圖
            if len(singleData['mediaMeta']) > 0:
                self.infomation['media']['notzero']['likeCount'] += int(
                    singleData['likeCount'])
                self.infomation['media']['notzero']['commentCount'] += int(
                    singleData['commentCount'])
            else:
                self.infomation['media']['zero']['likeCount'] += int(
                    singleData['likeCount'])
                self.infomation['media']['zero']['commentCount'] += int(
                    singleData['commentCount'])

    def showCatch(self, i, data):
        print(
            ("【Catch_{}】"
             "\n\t性別：{}"
             "\n\t標題：{}"
             "\n\t摘要：{}"
             "\n\t標籤：{}"
             "\n\t圖片數量：{}"
             "\n\t留言數量：{}"
             "\n\t愛心數量：{}").format(
                i + 1,
                data["gender"],
                data["title"],
                data["excerpt"][0:14] + '...',
                data["topics"],
                len(data["mediaMeta"]),
                data["commentCount"],
                data["likeCount"]
            )
        )

    def getForumsInfor(self, forums='nkfust', popular=True, limit=30):
        self.forums = forums
        self.limit = limit
        if popular:
            self.popular = 'true'
        else:
            self.popular = 'false'

        res = self.dSession.get(self.mainUrl + forums + '/posts?',
                                params={
                                    'popular':  self.popular,  # 熱門
                                    'limit': str(self.limit)  # 顯示文章篇數，最多100篇
                                },
                                verify=False)
        self.forumsData = res.json()
        self.showMessage()

    def getThisInfo(self):
        print(("###########[Info|{}]###########\n"
               "|---------------------|\n"
               " 男性發文統計\n"
               " ├———留言：{} 則\n"
               " └———愛心：{} 個\n"
               "|---------------------|\n"
               " 女性發文統計\n"
               " ├———留言：{} 則\n"
               " └———愛心：{} 個\n"
               "|---------------------|\n"
               " 發文附圖統計\n"
               " ├―——有圖\n"
               " │      ├———留言：{} 則\n"
               " │      └———愛心：{} 個\n"
               " └――—沒圖\n"
               "        ├———留言：{} 則\n"
               "        └———愛心：{} 個\n"
               "|---------------------|\n"
               "################################\n").format(
            self.infomation['total']['forums'],

            self.infomation['m']['commentCount'],
            self.infomation['m']['likeCount'],

            self.infomation['f']['commentCount'],
            self.infomation['f']['likeCount'],

            self.infomation['media']['notzero']['commentCount'],
            self.infomation['media']['notzero']['likeCount'],

            self.infomation['media']['zero']['commentCount'],
            self.infomation['media']['zero']['likeCount']
        ))

    def downloadImage(self, gender="none"):
        folder_path = './dacad/' + self.forums + '/'

        if (os.path.exists(folder_path) == False):  # 判斷主資料夾是否存在
            os.makedirs(folder_path)  # Create folder

        for i, data in enumerate(self.forumsData):
            if data['gender'] == gender or gender == "none":
                self.showCatch(i, data)
                media = data['mediaMeta']
                if len(media) > 0:
                    del media[0]
                    for index, image_url in enumerate(media):
                        image = self.dSession.get(image_url['url'])

                        img_path = folder_path + data['title'] + '/'

                        if (os.path.exists(img_path) == False):  # 判斷副資料夾是否存在
                            os.makedirs(img_path)  # Create folderＦ
                        # 以byte的形式將圖片數據寫入
                        with open(img_path + image_url['url'].split('/')[-1], 'wb') as file:
                            file.write(image.content)
                            file.flush()
                        file.close()  # close file
                        print("目前：第 {} 張照片，剩餘 {} 張需要下載".format(
                            index + 1, len(media) - index - 1))
                        # http://dangerlover9403.pixnet.net/blog/post/207823890-%5Bpython%5D-day14---python-%E5%BE%9E%E7%B6%B2%E8%B7%AF%E6%8A%93%E5%9C%96%E7%89%87
                    print(("---------------\n"
                           "{}-圖片下載完成\n"
                           "準備下載下一張...").format(data["title"]))
        print("[Info]全部圖片下載完成...")


# init
'''
if __name__ == "__main__":
    user = Dcard()
    user.getForumsInfor()
    user.downloadImage()
'''
