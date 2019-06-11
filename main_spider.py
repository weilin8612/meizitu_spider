import requests
from user_agents import my_user_agent
from lxml import etree
import os

headers = {
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
    urls = [base_url + str(i) for i in range(page)]
    for url in urls:
        #每一个妹子有单独的url目录,组成一个列表
        mz_urls = []

        res = requests.get(url, headers=headers)
        html = etree.HTML(res.text)
        lis = html.xpath('//ul[@id="pins"]/li')
        for li in lis:
            ele_url = li.xpath('./a/@href')
            mz_urls.append(ele_url[0])
        #已经获取每个女孩的主页mz_url
        for mz_url in mz_urls:
            #mz_url每一个图的url
            #meizi_urls = [mz_url + '/' + str(j + 1) for j in range(20)]
            res = requests.get(mz_url, headers=headers)
            html = etree.HTML(res.text)
            max = html.xpath('//div/a[last()-1]/span/text()')
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
                res = requests.get(meizi_url, headers=headers)
                html = etree.HTML(res.text)
                src = html.xpath('//div[@class="main-image"]/p/a/img/@src')
                print(src)
                res = requests.get(src[0], headers=headers)
                wp = meizi_url.split('/')
                with open('./{0}/{1}.jpg'.format(name[0], wp[-1]), 'wb') as f:
                    f.write(res.content)




if __name__ == "__main__":
    down_load(3, 30)