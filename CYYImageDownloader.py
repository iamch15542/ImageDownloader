#coding=utf-8
#Ver3.2.2
import docx
import os
import requests
import time
from bs4 import BeautifulSoup
from docx.shared import Inches
from PIL import Image

# header資訊
headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# exhentai需要的cookies
'''
請自己去Chrome看cookies的內容
再填入對應的位置即可
'''
exhentai_cookies = {
  'ipb_member_id' : '',
  'ipb_pass_hash' : '',
  'igneous' : '',
  's' : '',
  'lv' : '',
}

ptt_cookies = {'over18' : '1'}

# 紀錄圖片數量
ex_image_url_count = 0
ex_mainpage = 0

# 分析exhentai連結
def exhentai_model(url):
    # 建立 list
	global ex_title, ex_image_url_count, ex_page, ex_mainpage
	ex_title = []
	ex_page = []

	# 查詢要求的網站
	r = requests.get(url, headers = headers, cookies = exhentai_cookies)

	# 確認是否下載成功
	if r.status_code == requests.codes.ok:

		# 以 BeautifulSoup 解析 HTML 程式碼
		soup = BeautifulSoup(r.text, 'html.parser')

		if ex_mainpage == 0:
			# 獲得圖片張數
			page = soup.select('.gdt2')

			for a in page:
				ex_page.append(a.text)

			for a in ex_page[5].split():
				ex_page[5] = a
				break
			print u'---------開始下載圖片---------'
			page_id = int(ex_page[5])/40

		title = soup.select('.gm > #gd2 > #gj')
		for a in title:
			# 製作資料夾
			ex_title.append(a.text)
			mkdir(a.text)

		# 以 select 抓出分頁網址
		urldata = soup.select('.gdtm > div > a')
		for s in urldata:
			ex_image_url_count += 1
			exhentai_image_url(s['href'])
			# 停頓5秒，以免速度過快
			time.sleep(2)

		if ex_mainpage == 0:
			ex_mainpage += 1
			for i in range(page_id):
				next_url = url +'?p=' + str(i + 1)
				exhentai_model(next_url)
				time.sleep(20)


			if ex_image_url_count > 9:
				print u'--------總共 %d 張圖片--------' %ex_image_url_count
			else:
				print u'--------總共 %d 張圖片---------' %ex_image_url_count
			print u'---------圖片下載完成---------'

# 取得exhentai圖片網址
def exhentai_image_url(imageurl):

	# 查詢要求的網站
	r1 = requests.get(imageurl, headers = headers, cookies = exhentai_cookies)
	
	# 確認是否下載成功
	if r1.status_code == requests.codes.ok:

		# 以 BeautifulSoup 解析 HTML 程式碼
		soup = BeautifulSoup(r1.text, 'html.parser')

		# 以 class 抓出圖片網址
		url = soup.select('#i3 > a > img')

		for s in url :
			exhentai_image_download(s['src'])

# 下載exhentai圖片
def exhentai_image_download(galleryurl):
	filename = str(ex_image_url_count) + '.jpg'
	imgcontent = requests.get(galleryurl).content
	with open(ex_title[0] + '/' + filename, 'wb') as code:
		code.write(imgcontent)  
		if ex_image_url_count > 9:
			print u'-------第 %d 張圖片下載-------' %ex_image_url_count
		else:
			print u'-------第  %d 張圖片下載-------' %ex_image_url_count

# 分析dcard文章網址
def dcard_model(url):
	# 建立 list
	global textdata, dcard_image_url_count, dcard_sentence_count
	textdata = []

	# 查詢要求的網站
	r = requests.get(url)

	# 記錄圖片及句子數量
	dcard_image_url_count = 0
	dcard_sentence_count = 0

	# 確認是否下載成功
	if r.status_code == requests.codes.ok:

		# 以 BeautifulSoup 解析 HTML 程式碼
		soup = BeautifulSoup(r.text, 'html.parser')

		# 抓取文章標題並且修正
		title = soup.find("meta", property = "og:title")
		dcard_fix_title(title["content"])

		# 創建資料夾
		mkdir(dcard_title[0])

		# 抓取文章內容及圖片網址
		text = soup.select('div.Post_content_NKEl9 > div > div')
		print u'---------正在下載圖片---------'
		for a in text:
			model = 0
			txt = a.select('img[src]')
			for b in txt:
				dcard_image_url_count += 1
				dcard_image_download(b.get('src'))
				textdata.append(b.get('src'))
				dcard_sentence_count += 1
				model += 1
			if model == 0:
				textdata.append(a.text)
				dcard_sentence_count += 1
		if dcard_image_url_count > 9:
			print u'--------總共 %d 張圖片--------' %dcard_image_url_count
		else:
			print u'--------總共  %d 張圖片--------' %dcard_image_url_count
		print u'---------圖片下載完成---------'

		# 下載dcard文章
		dcard_txt_download(url)

# 下載圖片
def dcard_image_download(dcardimageurl):

	# 將網址換成正確的格式
	dcardimageurl.replace('imgur.dcard.tw', 'i.imgur.com')

	filename = str(dcard_image_url_count) + '.jpg'
	imgcontent = requests.get(dcardimageurl).content
	with open(dcard_title[0] +'/' + filename, 'wb') as code:
		code.write(imgcontent)   
		if dcard_image_url_count > 9:
			print u'-------第 %d 張圖片下載-------' %dcard_image_url_count
		else:
			print u'-------第 %d 張圖片下載--------' %dcard_image_url_count

# 將標題縮減空白刪除無意義字元
def dcard_fix_title(dcardtitle):
	global dcard_title
	tmp_title = []
	dcard_title = []
	tmp_2 = []
	count = 0

	# 將原本的標題分成片段
	for i in dcardtitle.split():
		tmp_title.append(i)
		count += 1

	# 合成成一個新片段
	for i in range(count - 3):
		dcard_title.append(tmp_title[i])
	dcard_title[0] = ''.join(dcard_title)

	if '/' in dcard_title[0]:
		for i in dcard_title[0].split('/'):
			tmp_2.append(i)
		dcard_title[0] = '+'.join(tmp_2)

#下載dcard文章
def dcard_txt_download(url) :
	print '------------------------------'
	print u'---------正在下載文章---------'
	filename = dcard_title[0] + '.txt'
	with open(dcard_title[0] + '/' + filename, 'a') as code:
		for i in range (dcard_sentence_count - 1) :
			code.write(textdata[i].encode('utf-8', 'ignore'))
			code.write('\n')
		code.write('\n')
		code.write("文章網址 :" + url.encode('utf-8', 'ignore'))
	print u'---------文章儲存完成---------'
	print '------------------------------'

# 分析ptt文章網址
def ptt_model(url):
	
	# 建立 list
	global txt_data, image_url_count, sentence_count, ptt_information, format_data
	format_data = []
	ptt_information = []
	txt_data = []

	# 查詢要求的網站
	r = requests.get(url, cookies = ptt_cookies)

	# 紀錄文章句數跟圖片數量
	image_url_count = 0
	sentence_count = 0

	# 確認是否下載成功
	if r.status_code == requests.codes.ok:

		# 以 BeautifulSoup 解析 HTML 程式碼
		soup = BeautifulSoup(r.text, 'html.parser')

		# 抓取作者, 看板及標題資訊
		ptt = soup.find_all('span', class_ = 'article-meta-value')

		# 作者: ptt_information[0], 看板: ptt_information[1], 標題: ptt_information[2]
		for i in ptt:
			ptt_information.append(i.text)

		# 製作資料夾
		mkdir(ptt_information[2])

		# 以 class 找出網址
		urldata = soup.find_all('a', rel = "nofollow")
		print u'---------開始下載圖片---------'
		for s in urldata:
			if 'imgur' in s.text:
				image_url_count += 1
				image_download(s.text)
			elif 'pbs' in s.text:
				image_url_count += 1
				image_download(s.text)
		
		print u'---------圖片下載完畢---------'
		print '------------------------------'
		print u'--------總共 %d 張圖片---------' %image_url_count

		# 抓取文章內容
		txt = soup.find(id = 'main-content')
		for i in txt.text.split('\n'):
			txt_data.append(i)
			sentence_count += 1

		# 製作文件
		ptt_word(url)

# 確認imgur網址的格式
def double_check_imgur(checkurl):
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
				urldata = soup.find("meta", property = 'og:image')
				for a in urldata['content'].split('?'):
					checkurl = a
					break
	# 回傳正確網址
	return checkurl

# ptt圖片下載
def image_download(imageurl):
	if 'imgur' in imageurl:
		imageurl = double_check_imgur(imageurl)

	elif 'pbs' in imageurl:
		pass
	
	filename = str(image_url_count) + imageurl[-4:]
	imgcontent = requests.get(imageurl).content
	with open(ptt_information[2] + '/' + filename,'wb') as code:
			code.write(imgcontent)		
			print u'-------第 %d 張圖片下載--------' %image_url_count

	if '.jpg' in imageurl:
		format_data.append('.jpg')
		im = Image.open(ptt_information[2].encode('utf-8','ignore') + '/' + str(image_url_count) + '.jpg')
		im.save(ptt_information[2].encode('utf-8','ignore') + '/' + str(image_url_count) + '.jpg', "JPEG")
	if '.png' in imageurl:
		format_data.append('.png')
		im = Image.open(ptt_information[2].encode('utf-8','ignore') + '/' + str(image_url_count) + '.png')
		im.save(ptt_information[2].encode('utf-8','ignore') + '/' + str(image_url_count) + '.png', "PNG")	

# 製作Word文檔
def ptt_word(url):
	num = 1
	txt = docx.Document()
	print '------------------------------'
	print u'---------開始下載文章---------'
	for i in range(1, sentence_count):
		if u'文章網址' in txt_data[i]:
			break
		if num <= image_url_count:
			str1 = ptt_information[2] + '/' + str(num) + format_data[num - 1]
			if 'https' in txt_data[i]:
				txt.add_picture(str1, width = Inches(3))
				num += 1
				continue
			if 'http' in txt_data[i]:
				txt.add_picture(str1, width = Inches(3))
				num += 1
				continue
		txt.add_paragraph(txt_data[i])

	txt.add_paragraph(u'\n網友' + ptt_information[0] + u'分享於' + ptt_information[1])
	txt.add_paragraph(url + '\n')
	txt.save(ptt_information[2] + '.docx')
	print u'---------文章下載完畢---------'
	print '------------------------------'

# 建立資料夾
def mkdir(titlename) :
    # 用 path = os.getcwd() 來取得腳本位置
    path = os.getcwd()

    # 創建文章標題的資料夾儲存圖片
    newpath = path + '/' + titlename
    if not os.path.isdir(newpath):
        os.mkdir(newpath)
        print '------------------------------'
        print u'文章標題 :',
        print titlename.encode('utf-8', 'ignore')
        print '------------------------------'

# 初始化介面
def initial_interface():
	print '----------------------------------'
	print u'--------歡迎使用Kuso下載器--------'
	print u'---------直接輸入網址即可---------'
	print '----------------------------------'

#主程式
def main():
	initial_interface()
	while(1):
		url = raw_input("請輸入文章網址:[離開程式請輸入 q ]\n")
		if 'ptt' in url:
			ptt_model(url)
		elif 'dcard' in url:
			dcard_model(url)
		elif 'exhentai' in url:
			exhentai_model(url)
		elif url == 'q':
			break;
		else:
			print u'----輸入無效模式，請重新輸入。----'
	print u'-----------程式結束-----------'

if __name__ == "__main__":
	main()
