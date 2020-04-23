#!/usr/bin/python
# coding=utf-8

import os
import sys
import logging

p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
if p not in sys.path:
    sys.path.append(p)

import requests
from meizitu_spider.user_agents import my_user_agent
from lxml import etree

from meizitu_spider.configure import BASE_URL, BEGIN_PAGE, AFTER_PAGE, SAVE_PATH, SLEEP, LASTE_PAGE
from time import sleep
from random import randint





def headers():
    return {
        # 'authority': 'www.mzitu.com',
        # ':method': 'GET',
        # ':scheme': 'https',
        # 'accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'cache-control': 'max-age=0',
        # 'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1579806566,1579822432; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1579826804',
        # 'if-modified-since': 'Thu, 23 Jan 2020 15:22:35 GMT',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-site': 'same-origin',
        # 'sec-fetch-user': '\?1',
        # 'upgrade-insecure-requests': '1',
        'Referer': 'https://www.mzitu.com/xinggan/',
        'user-agent': 'Mozilla / 5.0(X11;Linuxx86_64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 79.0.3945.130Safari / 537.36'
    }


def Fheaders():
    return {
        'authority': 'i5.mmzztt.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'image / webp, image / apng, image / *, * / *;q = 0.8',
        'accept-encoding': "gzip, deflate, br",
        'accept-language': 'zh-CN,zh;q=0.9',
        'Referer': 'https: // www.mzitu.com/203554/3',
        'sec-fetch-mode': 'no - cors',
        'sec-fetch-site': 'cross - site',
        'user-agent': 'Mozilla / 5.0(X11;Linuxx86_64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 79.0.3945.130Safari / 537.36'
    }


def consist_everybaby_urls():
    page_urls = [BASE_URL + str(i + 1) for i in range(BEGIN_PAGE, AFTER_PAGE)]

    # 每个baby的主页列表
    baby_urls = []
    for url in page_urls:

        # 每个baby的主页列表
        header = headers()
        # if BEGIN_PAGE != 1 or BEGIN_PAGE != 2:
        #     header['Referer'] = 'https://www.mzitu.com/xinggan/page/{0}'.format(BEGIN_PAGE-1)
        res = requests.get(url, headers=header)
        # print(res)
        html = etree.HTML(res.text)
        lis = html.xpath('//ul[@id="pins"]/li')
        for li in lis:
            ele_url = li.xpath('./a/@href')
            baby_urls.append(ele_url[0])
    return baby_urls


def get_onebaby_name_pagemax(baby_url):
    res = requests.get(baby_url, headers=headers())
    html = etree.HTML(res.text)

    # 从baby专辑主页获取最大页数
    maxpage = html.xpath('//div/a[last()-1]/span/text()')

    # 提取baby专辑名
    name = html.xpath('//div[@class="main-image"]/p/a/img/@alt')
    # print(name)
    # 处理空相应造成的name 空列表的异常
    try:
        name = clean_dirname(name[0])
        name = SAVE_PATH + '/' + name
        maxpage = int(maxpage[0])
    except IndexError:
        logging.warning("获取页面失败，sleep后继续请求")
        sleep(1.5 * SLEEP)
        (name, maxpage) = get_onebaby_name_pagemax(baby_url)

    return (name, maxpage)


def clean_dirname(dirname):
    table = str.maketrans("/ ,.\b\t\\\'\"？", "xxxxxxxxxx")
    result = dirname.translate(table)
    return result


# def download_picture(babymainurl, name):
#
# src = get_onebady_every_picture_url(babymainurl)
#
#     res = requests.get(src, headers=headers())
#
#     #提取网址最后一个字段如 0, 1, 2 作为图片名,并下载保存图片
#     wp = babymainurl.split('/')[-1]
#     print("wp is" + wp)
#     with open('{0}/{1}/{2}'.format(SAVE_PATH, name, wp[-1] + '.jpg'), 'wb') as f:
#         f.write(res.content)


def download_picture(babymainurl, name, src, header):
    # src = get_onebady_every_picture_url(babymainurl)

    res = requests.get(src, headers=header)

    # 提取网址最后一个字段如 0, 1, 2 作为图片名,并下载保存图片
    wp = babymainurl.split('/')[-1]
    logging.info("正在下载第 {0} 张图片".format(wp))
    # print("正在下载第 {0} 张图片".format(wp))
    with open('{0}/{1}'.format(name, wp + '.jpg'), 'wb') as f:
        f.write(res.content)


def get_onebady_every_picture_url(babymainurl, header):
    res = requests.get(babymainurl, headers=header)
    html = etree.HTML(res.text)
    # 提取专辑中所有图片的高清原url
    src = html.xpath('//div[@class="main-image"]/p/a/img/@src')
    try:
        src = src[0]
    except IndexError:
        logging.warning("获取html失败，sleep后继续请求")
        sleep(1.5 * SLEEP)
        src = get_onebady_every_picture_url(babymainurl, header)

    return src


def start_run():
    i = 0
    baby_urls = consist_everybaby_urls()
    logging.info("构建baby专辑主页列表成功")
    # print("构建baby专辑主页列表成功")
    for baby_url in baby_urls:
        # print(baby_url)
        logging.info(baby_url)
        (name, maxpage) = get_onebaby_name_pagemax(baby_url)
        logging.info("将要下载专辑为{0},最大页数为{1}".format(name, maxpage))
        # print("将要下载专辑为{0},最大页数为{1}".format(name, maxpage))
        sleep(0.1 * SLEEP)

        # 每个bady专辑的每张图片的url组成了一个列表
        onebady_all_picture = [baby_url + "/" + str(i + 1) for i in range(maxpage)]
        # print("构建专辑每张图片url列表成功，数量是{0}".format(len(onebady_all_picture)))
        logging.info("构建专辑每张图片url列表成功，数量是{0}".format(len(onebady_all_picture)))

        # 为没张专辑建立目录
        if os.path.exists(name):
            # print("已经有此专辑,进行下一张下载")
            logging.info("已经有此专辑,进行下一张下载")
            continue
        else:
            os.mkdir(name)
            # print("建立目录成功")
            logging.info("建立目录{0}成功".format(name))

        # 下载图片
        referer_headers = baby_url
        for onepicture in onebady_all_picture:
            # 找出专辑当前页在headers中的referer,并找出图片源地址
            add_header = Fheaders()
            add_header['Referer'] = referer_headers
            src = get_onebady_every_picture_url(onepicture, add_header)

            # 找出当前图片在herders中的referer,并下载图片
            add_header['Referer'] = onepicture
            download_picture(onepicture, name, src, add_header)
            sleep(randint(1, 3) * SLEEP / 30)
        i += 1
        # print("已经下载完第 {0} 张专辑, baby是 {1} 的专辑图片".format(i, name))
        logging.info("已经下载完第 {0} 张专辑, baby是 {1} 的专辑图片".format(i, name))


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    while AFTER_PAGE < LASTE_PAGE:
        logging.info("第{0}页专辑下载开始".format(AFTER_PAGE))
        # print("第{0}页专辑下载开始".format(AFTER_PAGE))
        start_run()
        logging.info("第{0}页专辑下载完成".format(AFTER_PAGE))
        # print("第{0}页专辑下载完成".format(AFTER_PAGE))
        BEGIN_PAGE += 1
        AFTER_PAGE += 1