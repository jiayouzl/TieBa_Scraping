# !/usr/bin/env python
# -*- coding: UTF-8 -*-

# https://tieba.baidu.com/f?kw=%E8%B7%AF%E7%94%B1%E5%99%A8&ie=utf-8

import re
import requests
import time
import threading
from pathlib import Path

def getHTML(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    try:
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return 'error'

def getList(html):
    regexp = re.compile(r'<a rel="noreferrer" href="/p/(.+?)"')
    getlists = regexp.findall(html)
    return getlists

def saveImages(listTemp):
    path = Path.cwd()
    imagepath = path / 'images_thread'
    print(imagepath)
    exit()
    if imagepath.exists() == False:
        imagepath.mkdir(parents = True, exist_ok = True)
    for List_i in listTemp:
        result = getHTML('https://tieba.baidu.com/p/' + List_i)
        comp = re.compile(r'<img class="BDE_Image" src="(.+?\.jpg)"')
        get_lists = re.findall(comp, result)
        name = 1
        for i in get_lists:
            print('正在下载页面ID：[' + List_i + ']中第：' + f'{name}' + '张图片')
            r = requests.get(i)
            save = imagepath / f'{List_i}_{name}.jpg'
            save.write_bytes(r.content)
            name += 1

def splitLite(listTemp, n: int):
    resules = []
    for i in range(0, len(listTemp), n):
        temp = listTemp[i:i + n]
        resules.append(temp)
    return resules

if __name__ == "__main__":
    st = time.time()
    url = 'https://tieba.baidu.com/f?kw=%E8%B7%AF%E7%94%B1%E5%99%A8&ie=utf-8'
    result = getHTML(url)
    idList = getList(result)
    split = splitLite(idList, 10)
    threadCount = len(split)
    threads = []
    for i in range(threadCount):
        print(split[i])
        t = threading.Thread(target = saveImages, args = (split[i], ))
        t.start()
        threads.append(t)
    for thread_end in threads:
        thread_end.join()

    print('multithread time:', int(time.time() - st), 's')
