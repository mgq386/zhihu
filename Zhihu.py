#-*-coning:utf-8 -*-

import requests
import json
import re
import time
import os
from requests.exceptions import ConnectionError

authorization = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
user_agens = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
Cookie = 'd_c0="AJDCV4Y2WQuPTtTilpG2XUAr18C_imm5-fU=|1487745543"; _zap=75f377e7-ba5d-4d68-babd-378a8ba3710f; aliyungf_tc=AQAAANkCOxyQPAMAAsxgd2L2xsLGhQp8; acw_tc=AQAAAIV8CW5sjwQAAsxgd0L2m8LmpnmF; q_c1=88a295ae4d154c0eba733a8aa04340a9|1493803175000|1487745543000; l_n_c=1; r_cap_id="NzgyMzQxYjI3MGE1NDg1OGE4NDg2MmIxNTQ2ZDI0OGQ=|1493803190|d8a0346134da3d2a950f872965ac165fc490d0b2"; cap_id="YTRlNGZmOTUxZmYwNDlkMzliNjZjZDdiYWNiZGE3NmQ=|1493803190|af40683c39f67f452388a986d3ecd97828f32e34"; l_cap_id="NGY0Zjk0MGExOTYxNDg0OWFmYjUzNDQzZDA1ODgyM2Y=|1493803190|072efec8ece44b8b0e5389d8f0c7ceb390ec5c93"; n_c=1; __utmt=1; __utma=155987696.483324588.1493803206.1493803206.1493803206.1; __utmb=155987696.1.10.1493803206; __utmc=155987696; __utmz=155987696.1493803206.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
heads = {'User-Agent': user_agens, 'Cookie': Cookie, 'authorization': authorization}
path = os.getcwd()+'/zhihu'

def get_json_data(limit,offset):
    url='https://www.zhihu.com/api/v4/questions/38285230/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit={}&sort_by=default'.format(offset,limit)
    print url
    #url = 'https://www.zhihu.com/api/v4/questions/30502941/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit={}&sort_by=default'.format(limit,offset)
    try:
        time.sleep(5)
        response = requests.get(url,headers=heads)
        print response.status_code
        response.encoding = response.apparent_encoding
        parser_json_data(response.text)
    except:
        print 'error'

def parser_json_data(html):

    data = json.loads(html)
    userse_info = data.get('data')
    for user in userse_info:
        content = user['content']
        get_page_images(content)

def get_page_images(content):
    pattern = re.compile('src="(.*?)".*?class="origin_image',re.S)
    items = re.findall(pattern,content)
    for url in items:
        print url
        download_image(url)

def download_image(url):
    time.sleep(6)
    try:
        response =requests.get(url,headers=heads)
        response.encoding = response.apparent_encoding
        save_image(url,response.content)
    except:
        return None


def save_image(url,content):

    name = url.split('/')[-1]
    file_name = path+'/'+name
    print file_name
    file = open(file_name,'wb')
    file.write(content)
    file.close()
    print 'save {} success'.format(url)


def mkdir(name):
    path = name.strip()
    isExist = os.path.exists(path)
    if not  isExist:
        os.mkdir(path)
    else:
        print 'path is exist '

def main():
    limit = 20
    for i in  range(0,10):
        if i==0:
            offset=0
        else:
            offset=3

        get_json_data(limit,offset+i*limit)


if __name__ == '__main__':
    mkdir('zhihu')
    main()