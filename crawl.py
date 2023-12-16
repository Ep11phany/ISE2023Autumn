import requests
import json
import os

def mkdir(path):
 
	folder = os.path.exists(path)
 
	if not folder:
		os.makedirs(path)   

def download_img(img,dirName):
    dirName = dirName+"/"
    if(len(img)<10): return 
    img_binary = requests.get(img).content
            # 切割出最后一个字符串
    file_name = img.split('?')[0]
    file_name = file_name.split('/')[-1]
            # 切割 query字符
    file_name = dirName + file_name
    with open(file_name, 'wb') as fp:
        fp.write(img_binary)
    return

url1 = "https://www.aigei.com/lib/sticker/?page="
for i in range(37,124):
    dir_name = "./imgs/img/"+str(i)
    mkdir(dir_name)
    url = url1 + str(i) + "#resContainer"
    html = requests.get(url)
    text1 = html.content
    text1 = str(text1 ,'utf-8')
    box_index = text1.find("black mpic-resc-unitBox-title",0)
    index_start = text1.find("/view/",box_index)
    index_end = text1.find("s",index_start)
    num = 0
    while(not(index_start == -1 or index_start >= index_end)):
        temp =  dir_name+"/"+str(num)
        mkdir(temp)
        url = "https://www.aigei.com" + text1[index_start:index_end] 
        html = requests.get(url)
        text2 = html.content
        text2 = str(text2 ,'utf-8')
        pic_index_start = text2.find("s1.4sai.com",0)
        pic_index_end = text2.find("\"",pic_index_start) + 1
        while(not(pic_index_start == -1 or pic_index_start >= pic_index_end)):
            pic_index_start = text2.find("s1.4sai.com",pic_index_end)
            pic_index_end = text2.find("\"",pic_index_start)
            url = "https://" + text2[pic_index_start:pic_index_end] 
            print(url)
            download_img(url,temp)
        box_index = text1.find("black mpic-resc-unitBox-title",index_end)
        index_start = text1.find("/view/",box_index)
        index_end = text1.find("s",index_start) + 1
        num = num + 1
    breakpoint = 1