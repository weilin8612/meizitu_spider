import requests
from user_agents import my_user_agent
from lxml import etree
import os
from time import sleep

def headers():
    return {
                # ':authority': 'www.mzitu.com',
                # ':method': 'GET',
                # ':scheme': 'https',
                # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                # 'accept-encoding': 'gzip, deflate, br',
                # 'accept-language': 'zh-CN,zh;q=0.9',
                # 'cache-control': 'max-age=0',
                # 'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1559132511,1559184202,1559295524,1560026651; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1560027027',
                # 'if-modified-since': 'Sat, 08 Jun 2019 20:50:26 GMT',
                'Referer': 'https://www.mzitu.com/xinggan/',
                'User-Agent': my_user_agent()
        }
base_url = 'https://www.mzitu.com/xinggan/page/'

def down_load(page, num=10000):
    """

    :param page: 爬下来多少页
    :param num: 每个美女下载多少张图
    :return:
    """
    #妹子图网址
    base_url = 'https://www.mzitu.com/xinggan/page/'
    #网站每一页的url
    urls = [base_url + str(i+1) for i in range(page)]
    for url in urls:
        #每一个妹子有单独的url目录,组成一个列表
        mz_urls = []

        res = requests.get(url, headers=headers())
        html = etree.HTML(res.text)
        lis = html.xpath('//ul[@id="pins"]/li')
        for li in lis:
            ele_url = li.xpath('./a/@href')
            mz_urls.append(ele_url[0])
        #已经获取每个女孩的主页mz_url
        for mz_url in mz_urls:
            #mz_url每一个图的url
            #meizi_urls = [mz_url + '/' + str(j + 1) for j in range(20)]
            res = requests.get(mz_url, headers=headers())
            html = etree.HTML(res.text)
            max = html.xpath('//div/a[last()-1]/span/text()')
            # sleep(1)
            if max:
                max = int(max[0])
                name = html.xpath('//div[@class="main-image"]/p/a/img/@alt')
                if num > max:
                    meizi_urls = [mz_url + '/' + str(j+1) for j in range(max)]
                else:
                    meizi_urls = [mz_url + '/' + str(j + 1) for j in range(num)]
                if os.path.exists(name[0]):
                    continue
                else:
                    os.mkdir(name[0])

            for meizi_url in meizi_urls:
                print(meizi_url)
                res = requests.get(meizi_url, headers=headers())
                html = etree.HTML(res.text)
                src = html.xpath('//div[@class="main-image"]/p/a/img/@src')
                # sleep(1)
                print(src)
                res = requests.get(src[0], headers=headers())
                wp = meizi_url.split('/')
                with open('./{0}/{1}.jpg'.format(name[0], wp[-1]), 'wb') as f:
                    f.write(res.content)




if __name__ == "__main__":
    down_load(3,100)