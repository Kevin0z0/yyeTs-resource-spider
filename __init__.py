from json import load

# 全局变量和预处理
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
baseurl = "http://www.rrys2020.com"
f = open('settings.json', 'r')
info = load(f)
zh_info = {
    "链接": "url",
    "排名": "rank",
    "剧种": "dramaType",
    "评分": "score",
    "原名": 'formerName',
    "地区": "region",
    "语 言": "language",
    "首播": "premiereDate",
    "制作公司": "company",
    "电视台": "company",
    "类型": "type",
    "翻译": "translator",
    "IMDB": "imdb",
    "别名": "alias",
    "編劇": "screenwriter",
    "导演": "directors",
    "主演": "actors",
    "简介": "introduction",
    "图片链接": "imgurl"
}
# 获取主要参数
result_info = {}
for key in zh_info.values():
    if info[key]:
        result_info[key] = info[key]

# 引入csv
export = info['export']
if export == 'csv':
    import csv

    def wirtecsv(txt, path='result.csv'):
        f = open(path, 'a', newline='', encoding='utf-8-sig')
        c = csv.writer(f)
        c.writerow(txt)
        f.close()

    txt = ['title', 'level']
    for i in result_info:
        txt.append(i)
    wirtecsv(txt)
# 引入pymongo
elif isinstance(export, dict):
    if export['db'] == 'mongodb':
        from mongo import DB
    elif export["db"] == "mysql":
        from mysql import DB

    db = DB(export)

