from fake_useragent import UserAgent
import requests
import base64

def b64d(s):
    return base64.b64decode(s).decode()

def safe_get_request(url):
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
        err_msg = '<h1> my_stop_1 </h1>'
        return(err_msg)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        err_msg = '<h1> my_stop_1 </h1>'
        return(err_msg)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        err_msg = '<h1> my_stop_1 </h1>'
        return(err_msg)


    return(page.text)



from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Nothing here</h1>'


@app.route('/fetch/<url>')
def user(url):
    print(url)
    print(b64d(url))
    return safe_get_request(b64d(url))


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not found!</h1>', 404

@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>Page not found 505!</h1>', 500
