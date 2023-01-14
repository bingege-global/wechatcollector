import scrapy
from scrapy.linkextractors import LinkExtractor
import mysql.connector
from .. import db


class SogouWechatSpider(scrapy.Spider):
    name = "sogou_wechat"
    link_extractor = LinkExtractor(allow=r'^https:\/\/weixin\.sogou\.com\/link.*', restrict_css='.txt-box h3 a')
    # Set the headers here. 
    
    headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache",
    'cookie': "ABTEST=0|1673629626|v1; IPLOC=CN3502; SUID=081E3D3BBA18960A0000000063C18FBA; PHPSESSID=bsoef880vfrnonh9gs00unrqr6; SUV=00C3E8BF3B3D1E0863C18FBA63D9C273; SUID=081E3D3B1431A40A0000000063C18FBA; SNUID=9B8AA9A8949166BCD703F546947A6FE3; seccodeRight=success; successCount=1|Fri, 13 Jan 2023 17:12:28 GMT; JSESSIONID=aaattwfunKFYVh4QUB7vy; ariaDefaultTheme=undefined",
    'pragma': "no-cache",
    'sec-ch-ua': "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': "\"macOS\"",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "none",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        baseUrl = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query='
        for (id, key) in db.getAllKey():
            print(f'==> start request key: {key}')
            yield scrapy.Request(url=baseUrl+key, callback=self.parse, headers=self.headers, meta={ 'keyId': id })

    def parse(self, response):
        keyId = response.meta['keyId']
        # 解析和保持文章地址
        for link in self.link_extractor.extract_links(response):
            if not db.existsByUrl(link.url):
                db.saveArticle(link.url, link.text, keyId)

        # 解析下一页地址
        next_page = response.css('#sogou_next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse, headers=self.headers, meta={ 'keyId': keyId })
