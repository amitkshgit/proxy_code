import base64
import datetime
import requests
import http.client, urllib
from urllib.parse import parse_qs
from fake_useragent import UserAgent

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

def app(environ, start_response):
    ## Process params
    query_string = environ.get('QUERY_STRING', '')
    parameters = parse_qs(query_string)

    # Get values from parameters (parse_qs returns a dictionary of lists)
    # For example, if key1=value1, parameters will be {'key1': ['value1']}
    encoded_url = parameters.get('url', [''])[0]
    ## B64 decode
    url = base64.urlsafe_b64decode(encoded_url).decode('utf-8')
    ## Code for html
    current_time = datetime.datetime.now()
    current_time_formatted = current_time.strftime('%Y-%m-%d %H:%M:%S')
    #data_raw = 'From App1: Hello, World! ' + current_time_formatted + '\n'
    data_raw = f'From App1: Hello, World! {current_time_formatted} \nFetch Url:: {url}'
    webpage_text = safe_get_request(url)
    data_raw = f'{data_raw} \n\n\n\nWebpage Data \n\n\n\n --------------------------- \n\n\n\n {webpage_text}'
    data = data_raw.encode()
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
