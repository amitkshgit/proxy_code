import base64
import asyncio
import requests
from flask import Flask
from fake_useragent import UserAgent
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def b64d(s):
    return base64.b64decode(s).decode()

async def scrape_c4ai(url):
    async with AsyncWebCrawler() as crawler:
        md_page = await crawler.arun(url=url)
        return(md_page.markdown)


async def safe_get_request(url):
    ua = UserAgent()
    headers = {'User-Agent' : ua.random}
    try:
        page = requests.get(url, headers=headers, verify=True, timeout=10)
        page.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        err_msg = '<h1> my_stop_1 </h1>'
        return(err_msg)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        err_msg = '<h1> my_stop_2 </h1>'
        return(err_msg)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        err_msg = '<h1> my_stop_3 </h1>'
        return(err_msg)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        err_msg = '<h1> my_stop_4 </h1>'
        return(err_msg)


    return(page.text)



app = Flask(__name__)

@app.route('/')
async def index():
    return '<h1>Nothing here</h1>'


@app.route('/app_xjpdWoBTvD/<url>')
async def user(url):
    #print(url)
    #print(b64d(url))
    #return await safe_get_request(await b64d(url))
    return await scrape_c4ai(await b64d(url))


@app.errorhandler(404)
async def page_not_found(e):
    return '<h1>Page not found!</h1>', 404

@app.errorhandler(500)
async def internal_server_error(e):
    print(e)
    return e, 500
    #return '<h1>Page not found 505!</h1>', 500

