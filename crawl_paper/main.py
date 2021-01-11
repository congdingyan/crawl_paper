#导入必要库
import os#创建本地目录
import re#用于操作字符串
import urllib.request#下载网页内容
import requests#获取网页代码
import socket#非必须的库，防止下载过程中因超时而引起的失败
import time

# 创建本地目录，存放下载的论文
local_dir = 'D:\\CVPR16\\'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

#第一步获取网页代码
def get_context(url):
    web_context = requests.get(url)
    return web_context.text

url = 'https://openaccess.thecvf.com/CVPR2016'
web_context = get_context(url)
#print(web_context)

#第二步解析网页代码，获取想要的信息
'''
(?<=href=\"): 寻找开头，匹配此句之后的内容
.+: 匹配多个字符（除了换行符）
?pdf: 匹配零次或一次pdf
(?=\">pdf): 以">pdf" 结尾
|: 或
'''
#link pattern: href="***_CVPR_2016_paper.pdf">pdf
link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)",web_context)
#name pattern: <a href="***_CVPR_2016_paper.html">***</a>
name_list = re.findall(r"(?<=2016_paper.html\">).+(?=</a>)",web_context)
#print(link_list)
#time.sleep(10)

#设置最长超时时间为30s
socket.setdefaulttimeout(30)
#第三步，利用获取的信息，执行相应的操作
cnt = 0
while cnt < len(link_list):
    file_name = name_list[cnt]#作为文件名
    download_url = link_list[cnt]#作为下载链接
    #为了可以保存为文件名，将标点符号和空格替换为'_'
    #file_name = re.sub('[:\?/]+',"_",file_name).replace(' ','_')
    file_path = local_dir + file_name + '.pdf'

    try:
        #执行下载的具体函数
        urllib.request.urlretrieve("https://openaccess.thecvf.com/" + download_url, file_path)
        #print(download_url)
        print('download success: ' + file_name)
    except socket.timeout:#超时则执行失败
        print('download Fail: ' + file_name)
    cnt += 1

print('Finished')

