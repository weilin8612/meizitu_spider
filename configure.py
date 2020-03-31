#为了避免被封IP，建议 BEGIN_PAGE与AFTER_PAGE的差不超过2
#SLEEP的设置 15是一个长期稳定的数值, 如果为0 很快将会被封IP
#因为路径的设置,与windows并不兼容,如果仍要移植，仅需要改关于路径的代码即可,在main.py主程序中的图片保存open函数的name变量改掉即可.


#网站主页
BASE_URL = 'https://www.mzitu.com/xinggan/page/'

#从第几页下载
BEGIN_PAGE = 0

#下载到第几页结束
AFTER_PAGE = 2
LASTE_PAGE = 3
#图片保存路径
SAVE_PATH = '/home/weilin/Pictures/meizitu'

#防被封IP, 爬取间隔倍数, 若为0则是不停的下载
SLEEP = 15
