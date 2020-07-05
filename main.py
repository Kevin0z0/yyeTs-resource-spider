# coding=utf-8
import re
import time
import requests
from __init__ import *
from json import loads
from threading import Thread
from pyquery import PyQuery as pq



def throw_error(e,num):
    print("出现[{}]错误，开始重新获取{}中的内容".format(e,num))
    time.sleep(1)


def get_level(html,level): # 获取影视分级
    try:
        s = re.search("icon/([a-e])-big",html).group(1) #获取url中的关键字
        if level == "all" or s in [x for x in level]:
            return s
        return False
    except:
        return "暂无" if level == "all" else False


def get_info(html):
    s = {}
    for i in html(".fl-info ul li").items():
        i = i.text().split("：")
        if i[0] in zh_info:
            s[zh_info[i[0]]] = i[1]
    return s


def get_score(num): # 获取评分
    try:
        doc = requests.post(baseurl + "/resource/getScore",data={"rid":num},headers=headers,timeout=5).content.decode()
        return loads(doc)['score']
    except Exception as e:
        throw_error(e, num)
        get_score(num)


def format_date(date):
    arr = date.split(" ")[0].split("-")
    num=0
    for i in arr:
        if i.isdigit():
            if num > 0:
                while len(i) < 2:
                    i = "0" + i
            arr[num] = i
            num += 1
    date = ''.join(arr)
    date += (8 - len(date)) * "0"
    return int(date)


def analyze(u):
    try:
        url = baseurl + u
        doc = requests.get(url, headers=headers,timeout=5).content.decode()
        html = pq(doc)
        # 获取标题和剧种
        title = re.search("title:'【(.*?)-.*?】《(.*?)》",doc).groups()
        # 获取影视分级
        items = html('.level-item img').attr('src')
        level = get_level(items, info["level"])
        # 如果返回的分级为false则跳过这条
        if level == False: return
        # 获取主要信息
        main_info = get_info(html)
        # 获取剧种
        if "dramaType" in result_info:
            main_info["dramaType"] = title[0]
        # 获取评分
        if "score" in result_info:
            main_info["score"] = get_score(u[-5:])
        if 'url' in result_info:
            main_info['url'] = url
        # 获取影片封面
        if "imgurl" in result_info:
            main_info['imgurl'] = re.search("pic:'(.*?)'",doc).group(1)
        # 获取本站排名
        if "rank" in result_info:
            main_info["rank"] = int(re.search("本站排名:.*?(\d*)$", html(".score-con p.f4").text()).group(1))
        # 获取简介
        if "introduction" in result_info:
            main_info["introduction"] = html(".resource-desc .con:last-child").text()
        result = {}
        # 写入标题和分级
        result["title"] = title[1]
        result["level"] = level.upper()
        # 遍历main_info,只写入有效数据
        for key, value in result_info.items():
            try:
                result[key] = main_info[key]
            except:
                result[key] = '暂无'

        # 修改日期格式
        if result["premiereDate"]:
            result["premiereDate"] = format_date(result["premiereDate"])

        print(result['title'])
        # 写入文件
        if export == 'csv':
            wirtecsv([i for i in result.values()])
        else:
            mycol.insert_one(result)
    except Exception as e:
        throw_error(e,u)
        analyze(u)


def main(num):
    try:
        url = baseurl + "/resourcelist/?page={}".format(num)
        doc = pq(requests.get(url, headers=headers, timeout=5).content.decode())
        arr = [i.attr("href") for i in doc(".fl-info a").items()]  #遍历a标签
        if len(arr) == 0:
            time.sleep(1)
            print("[*] 再次获取第{}页".format(num))
            main(num)
            return
        if info['threads']:
            for i in arr:
                Thread(target=analyze,args=(i,)).start()
        else:
            for i in arr:
                analyze(i)
        time.sleep(1)
    except Exception as e:
        throw_error(e,num)
        main(num)


if __name__ == '__main__':
    page = info['pageNum']
    if '-' in page:
        page = page.split('-')
        for i in range(int(page[0]),int(page[1])+1):
            print("> 第{}页".format(i))
            main(i)
    else:
        main(int(page))
