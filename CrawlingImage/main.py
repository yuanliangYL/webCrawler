
import requests
import re
import os
import time
import html

# # 全局属性
headers = {
    # 告诉浏览器用户的身份
    "User-Agent": "iOS/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# 1.请求网页
def requesthtmlPage(url):
    try:
        respons = requests.get(url, headers=headers)
        html = respons.text
        # print(respons.text)
        # print(respons.request.headers)
        return html
    except:
        return "getHTMLText NULL"


# # 2.解析网页
def parsePage(html,parse_standard):
    try:
        list = re.findall(parse_standard, html)
        return list
    except:
        return "parseHTML NULL"


#设置目录
def creatDucoment(html,path_standard):

    if len(html):
        dir_name = re.findall(path_standard, html)[-1]
        print(dir_name)
    else:
        dir_name = path_standard

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return  dir_name


# 下载到指定路径：保存图片
def download(path,img_urls):

    for url in img_urls:
        time.sleep(0.1)
        file_name = url.split('/')[-1]
        respons = requests.get(url, headers=headers)

        print(path,file_name)
        if os.path.exists(path + '/' + file_name):
            continue

        with open(path + '/' + file_name, 'wb') as f:
            f.write(respons.content)


def getMianPageInfo(url):

    #  获取首页 #base: https://www.moestack.com/all
    html = requesthtmlPage(url)
    # 所有图片文件名称+跳转链接
    list = parsePage(html, '<a href="(.*?)" title=".*?" rel=".*?">(.*?)</a>')
    return list



def main():

   #  获取首页 #base: https://www.moestack.com/all
   list = getMianPageInfo("https://www.moestack.com/all")

   for singlePage in list:
       html_resource = requesthtmlPage(singlePage[0])
       list_urls =  parsePage(html_resource ,'<p><img src="(.*?)" alt=""/></p>')
       print(list_urls)
       path = creatDucoment("",html.unescape(singlePage[1]))

       download(path, list_urls)


if __name__ == "__main__":
    main()




