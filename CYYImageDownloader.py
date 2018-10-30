#coding=utf-8
import json
import os
import time
import tkMessageBox
import Tkinter as tk

import docx
import pytube
import requests
from bs4 import BeautifulSoup
from docx.shared import Inches
from PIL import Image
from PIL import ImageTk


class Exhentai():
    def __init__(self, url):
        self.url = url
        # 紀錄圖片數量
        self.ex_image_url_count = 0
        self.ex_mainpage = 0
        self.ex_title = []
        self.ex_page = []
        self.ex_cookies = {
            'ipb_member_id': '',
            'ipb_pass_hash': '',
            'igneous': '',
            's': '',
            'lv': '',
        }
        # header資訊
        self.headers = {
            'user-agent':
            'Mozilla/5.0 (Macintosh Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

    # 分析exhentai連結
    def ex_analysis(self):

        r = requests.get(self.url, headers=headers, cookies=self.ex_cookies)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

            if self.ex_mainpage == 0:
                page = soup.select('.gdt2')

                for a in page:
                    self.ex_page.append(a.text)

                for a in self.ex_page[5].split():
                    self.ex_page[5] = a
                    break
                text_update('開始下載圖片\n')
                page_id = int(self.ex_page[5]) / 40

            title = soup.select('.gm > #gd2 > #gj')
            for a in title:
                self.ex_title.append(a.text)
                mkdir(a.text)

            # 以 select 抓出分頁網址
            urldata = soup.select('.gdtm > div > a')
            for sub_url in urldata:
                self.ex_image_url_count += 1
                try:
                    self.exhentai_image_url(sub_url['href'])
                except:
                    text_update('下載圖片過程發生問題\n')
                # 停頓5秒，以免速度過快
                time.sleep(5)

            if self.ex_mainpage == 0:
                self.ex_mainpage += 1
                for i in range(page_id):
                    next_url = self.url + '?p=' + str(i + 1)
                    self.exhentai_model(next_url)
                    time.sleep(20)

                if self.ex_image_url_count > 9:
                    text_update('總共 %d 張圖片\n' % self.ex_image_url_count)
                else:
                    text_update('總共 %d 張圖片\n' % self.ex_image_url_count)
                text_update('圖片下載完成\n')

    # 取得exhentai圖片網址
    def exhentai_image_url(self, imageurl):
        sub_r = requests.get(
            imageurl, headers=headers, cookies=self.ex_cookies)
        if sub_r.status_code == requests.codes.ok:
            soup = BeautifulSoup(sub_r.text, 'html.parser')
            url = soup.select('#i3 > a > img')
            for img in url:
                try:
                    self.exhentai_image_download(img['src'])
                except:
                    text_update('下載圖片過程發生問題\n')

    # 下載exhentai圖片
    def exhentai_image_download(self, galleryurl):
        filename = str(self.ex_image_url_count) + '.jpg'
        imgcontent = requests.get(galleryurl).content
        with open(self.ex_title[0] + '/' + filename, 'wb') as code:
            code.write(imgcontent)
            if self.ex_image_url_count > 9:
                text_update('第 %d 張圖片下載\n' % self.ex_image_url_count)
            else:
                text_update('第  %d 張圖片下載\n' % self.ex_image_url_count)


class Dcard():
    def __init__(self, url):
        self.__url = url
        self.dcard_text = []
        self.dcard_image_url_count = 0
        self.dcard_sentence_count = 0
        self.dcard_title = []

    # 分析dcard文章網址
    def dcard_analysis(self):
        r = requests.get(self.__url)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

            # 抓取文章標題並且修正
            title = soup.find("meta", property="og:title")
            self.dcard_fix_title(title["content"])

            # 創建資料夾
            mkdir(self.dcard_title[0])

            # 抓取文章內容及圖片網址
            text = soup.select('div.Post_content_NKEl9 > div > div')
            text_update('正在下載圖片\n')
            for a in text:
                model = 0
                txt = a.select('img[src]')
                for b in txt:
                    self.dcard_image_url_count += 1
                    try:
                        self.dcard_image_download(b.get('src'))
                    except:
                        text_update('下載圖片過程發生問題\n')
                    self.dcard_text.append(b.get('src'))
                    self.dcard_sentence_count += 1
                    model += 1
                if model == 0:
                    self.dcard_text.append(a.text)
                    self.dcard_sentence_count += 1
            if self.dcard_image_url_count > 9:
                text_update('總共 %d 張圖片\n' % self.dcard_image_url_count)
            else:
                text_update('總共  %d 張圖片\n' % self.dcard_image_url_count)
            text_update('圖片下載完成\n')

            # 下載dcard文章
            try:
                self.dcard_txt_download(self.__url)
            except:
                text_update('下載文章過程發生問題\n')

    # 下載圖片
    def dcard_image_download(self, dcardimageurl):

        # 將網址換成正確的格式
        dcardimageurl.replace('imgur.dcard.tw', 'i.imgur.com')

        filename = str(self.dcard_image_url_count) + '.jpg'
        imgcontent = requests.get(dcardimageurl).content
        with open(self.dcard_title[0] + '/' + filename, 'wb') as code:
            code.write(imgcontent)
            if self.dcard_image_url_count > 9:
                text_update('第 %d 張圖片下載\n' % self.dcard_image_url_count)
            else:
                text_update('第 %d 張圖片下載\n' % self.dcard_image_url_count)

    # 將標題縮減空白刪除無意義字元
    def dcard_fix_title(self, dcardtitle):
        tmp_title = []
        tmp_2 = []
        count = 0

        # 將原本的標題分成片段
        for i in dcardtitle.split():
            tmp_title.append(i)
            count += 1

        # 合成成一個新片段
        for i in range(count - 3):
            self.dcard_title.append(tmp_title[i])
        self.dcard_title[0] = ''.join(self.dcard_title)

        if '/' in self.dcard_title[0]:
            for i in self.dcard_title[0].split('/'):
                tmp_2.append(i)
            self.dcard_title[0] = '+'.join(tmp_2)

    #下載dcard文章
    def dcard_txt_download(self, url):
        text_update('------------------------------\n')
        text_update('正在下載文章\n')
        filename = self.dcard_title[0] + '.txt'
        with open(self.dcard_title[0] + '/' + filename, 'a') as code:
            for i in range(self.dcard_sentence_count - 1):
                code.write(self.dcard_text[i].encode('utf-8', 'ignore'))
                code.write('\n')
            code.write('\n')
            code.write("文章網址 :" + url.encode('utf-8', 'ignore'))
        text_update('文章儲存完成\n')
        text_update('------------------------------\n')


class Ptt():
    def __init__(self, url):
        self.url = url
        self.format_data = []
        self.ptt_information = []
        self.txt_data = []
        self.ptt_tmp = []
        self.image_url_count = 0
        self.sentence_count = 0
        self.ptt_cookies = {'over18': '1'}

    def analysis(self):
        r = requests.get(self.url, cookies=self.ptt_cookies)
        if r.status_code == requests.codes.ok:

            soup = BeautifulSoup(r.text, 'html.parser')
            ptt = soup.find_all('span', class_='article-meta-value')

            # 作者: ptt_information[0], 看板: ptt_information[1], 標題: ptt_information[2]
            for i in ptt:
                self.ptt_information.append(i.text)

            if '/' in self.ptt_information[2]:
                for i in self.ptt_information[2].split('/'):
                    self.ptt_tmp.append(i)
                self.ptt_information[2] = '+'.join(self.ptt_tmp)

            # 製作資料夾
            mkdir(self.ptt_information[2])

            # 以 class 找出網址
            urldata = soup.find_all('a', rel="nofollow")
            text_update('開始下載圖片\n')
            for s in urldata:
                if 'imgur' in s.text:
                    self.image_url_count += 1
                    try:
                        self.image_download(s.text)
                    except:
                        text_update('下載圖片過程發生問題\n')
                elif 'pbs' in s.text:
                    self.image_url_count += 1
                    try:
                        self.image_download(s.text)
                    except:
                        text_update('下載圖片過程發生問題\n')

            text_update('圖片下載完畢\n')
            text_update('------------------------------\n')
            text_update('總共 %d 張圖片\n' % self.image_url_count)

            # 抓取文章內容
            txt = soup.find(id='main-content')
            for i in txt.text.split('\n'):
                self.txt_data.append(i)
                self.sentence_count += 1

            # 製作文件
            try:
                self.ptt_word(self.url)
            except:
                text_update('下載文章過程發生問題\n')

    # 確認imgur網址的格式
    def double_check_imgur(self, checkurl):
        model = 0
        if 'i.imgur' not in checkurl:

            # 如果網址結尾有 JPG 或是 PNG 的話，則可以直接通過確認
            if 'jpg' in checkurl:
                model = 1

            if 'png' in checkurl:
                model = 1

            # 網址沒有 JPG 或是 PNG ，則要進入網頁搜尋正確的網址
            if model == 0:

                imgur = requests.get(checkurl)

                # 確認是否下載成功
                if imgur.status_code == requests.codes.ok:

                    # 以 BeautifulSoup 解析 HTML 程式碼
                    soup = BeautifulSoup(imgur.text, 'html.parser')

                    # 抓出正確的網址
                    urldata = soup.find("meta", property='og:image')
                    for a in urldata['content'].split('?'):
                        checkurl = a
                        break
        # 回傳正確網址
        return checkurl

    # ptt圖片下載
    def image_download(self, imageurl):
        if 'imgur' in imageurl:
            imageurl = self.double_check_imgur(imageurl)

        elif 'pbs' in imageurl:
            pass

        filename = str(self.image_url_count) + imageurl[-4:]
        imgcontent = requests.get(imageurl).content
        with open(self.ptt_information[2] + '/' + filename, 'wb') as code:
            code.write(imgcontent)
            text_update('第 %d 張圖片下載\n' % self.image_url_count)

        if '.jpg' in imageurl:
            try:
                self.format_data.append('.jpg')
                im = Image.open(
                    self.ptt_information[2].encode('utf-8', 'ignore') + '/' +
                    str(self.image_url_count) + '.jpg')
                im.save(
                    self.ptt_information[2].encode('utf-8', 'ignore') + '/' +
                    str(self.image_url_count) + '.jpg', "JPEG")
            except IOError:
                text_update('第 %d 張圖片下載失敗\n' % self.image_url_count)
                self.image_url_count -= 1
        elif '.png' in imageurl:
            try:
                self.format_data.append('.png')
                im = Image.open(
                    self.ptt_information[2].encode('utf-8', 'ignore') + '/' +
                    str(self.image_url_count) + '.png')
                im.save(
                    self.ptt_information[2].encode('utf-8', 'ignore') + '/' +
                    str(self.image_url_count) + '.png', "PNG")
            except IOError:
                text_update('第 %d 張圖片下載失敗\n' % self.image_url_count)
                self.image_url_count -= 1
        else:
            text_update('第 %d 張圖片下載失敗\n' % self.image_url_count)
            self.image_url_count -= 1

    # 製作Word文檔
    def ptt_word(self, url):
        num = 1
        txt = docx.Document()
        text_update('------------------------------\n')
        text_update('開始下載文章\n')
        for i in range(1, self.sentence_count):
            if u'文章網址' in self.txt_data[i]:
                break
            if num <= self.image_url_count:
                str1 = self.ptt_information[2] + '/' + str(
                    num) + self.format_data[num - 1]
                if 'https' in self.txt_data[i]:
                    txt.add_picture(str1, width=Inches(3))
                    num += 1
                    continue
                if 'http' in self.txt_data[i]:
                    txt.add_picture(str1, width=Inches(3))
                    num += 1
                    continue
            txt.add_paragraph(self.txt_data[i])

        txt.add_paragraph(u'\n網友' + self.ptt_information[0] + u'分享於' +
                          self.ptt_information[1])
        txt.add_paragraph(url + '\n')
        txt.save(self.ptt_information[2] + '.docx')
        text_update('文章下載完畢\n')
        text_update('------------------------------\n')


'''
下載Youtube影片
'''


class Youtube():
    def __init__(self, url):
        self.__url = url

    def download_video(self):
        yt = pytube.YouTube(self.__url)
        path = os.getcwd() + '/'
        text_update('------------------------------\n')
        text_update('開始下載影片\n')
        dl = yt.streams.first()
        dl.download(path)
        text_update('影片標題: ')
        text_update(yt.title + '\n')
        text_update('影片下載完畢\n')
        text_update('------------------------------\n')


'''
下載IG圖片
'''


class Instagram():
    def __init__(self, url):
        self.__url = url

    def analysis_ig(self):
        r = requests.get(self.__url)
        if r.status_code == requests.codes.ok:

            soup = BeautifulSoup(r.text, 'html.parser')
            getjson = soup.find_all("script", type="text/javascript")[3].string

            getjson = getjson[getjson.find('=') + 2:-1]
            data = json.loads(getjson)
            image_url = data['entry_data']['PostPage'][0]['graphql'][
                'shortcode_media']['display_url']
            text_update('------------------------------\n')
            text_update('開始下載圖片\n')
            filename = str(1) + '.jpg'
            imgcontent = requests.get(image_url).content
            with open(filename, 'wb') as code:
                code.write(imgcontent)
            text_update('圖片下載完畢\n')
            text_update('------------------------------\n')


# 建立資料夾
def mkdir(titlename):
    # 用 path = os.getcwd() 來取得腳本位置
    path = os.getcwd()

    # 創建文章標題的資料夾儲存圖片
    newpath = path + '/' + titlename
    if not os.path.isdir(newpath):
        os.mkdir(newpath)
        text_update('------------------------------\n')
        text_update('文章標題: ')
        text_update(titlename.encode('utf-8', 'ignore'))
        text_update('\n------------------------------\n')


state = 0

if __name__ == "__main__":

    windows = tk.Tk()

    # 標題
    windows.title('CYYDownloader')

    # 視窗大小
    windows.geometry('800x500')

    # 設置封面圖片
    img_open = Image.open('title.png')
    img_png = ImageTk.PhotoImage(img_open)
    label_img = tk.Label(windows, image=img_png)
    label_img.pack()

    def clear_box(event):
        web_url.delete(0, tk.END)
        return

    tk.Label(windows, text='下載網址: ', font=('Arial', '20')).place(x=10, y=100)
    get_web_url = tk.StringVar()
    get_web_url.set('請輸入文章網址:')
    web_url = tk.Entry(windows, textvariable=get_web_url, width=70)
    web_url.place(x=100, y=100)
    web_url.bind("<Button>", clear_box)

    # 輸出文字介面
    tk.Label(windows, text='下載狀態: ', font=('Arial', '20')).place(x=10, y=140)
    textbox = tk.Text(windows, height=10, width=80)
    textbox.place(x=10, y=180)

    # 顯示目前狀態
    def text_update(word):
        textbox.insert('insert', word)
        textbox.update()
        textbox.see(tk.END)

    # 彈出錯誤視窗
    def error_message():
        tkMessageBox.showerror(title='Warning', message='輸入無效網址，請重新輸入。')

    # 彈出下載完成
    def finish_download():
        tkMessageBox.showerror(title='Finish!!!!', message='下載完成！！！！！！！')

    # 主程式
    def run():
        global state
        if state == 1:
            textbox.delete(1.0, tk.END)
        url = get_web_url.get()
        if 'ptt' in url:
            state = 1
            ptt = Ptt(url)
            ptt.analysis()
            finish_download()
        elif 'dcard' in url:
            state = 1
            dcard = Dcard(url)
            dcard.dcard_analysis()
            finish_download()
        elif 'exhentai' in url:
            state = 1
            ex = Exhentai(url)
            ex.ex_analysis()
            finish_download()
        elif 'youtube' in url:
            state = 1
            yoube = Youtube(url)
            yoube.download_video()
            finish_download()
        elif 'instagram' in url:
            state = 1
            ig = Instagram(url)
            ig.analysis_ig()
            finish_download()
        elif url == 'q':
            windows.destroy()
        else:
            state = 0
            error_message()

    # 按鈕
    start_button = tk.Button(
        windows,
        text='開始下載',
        width=20,
        height=2,
        font=('Arial', '20'),
        command=run).place(
            x=10, y=360)
    end_button = tk.Button(
        windows,
        text='結束程式',
        width=20,
        height=2,
        font=('Arial', '20'),
        command=windows.destroy).place(
            x=300, y=360)

    # 主循環
    windows.mainloop()
