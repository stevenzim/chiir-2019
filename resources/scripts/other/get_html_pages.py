"""A script to download the html for websites in Waterloo and my    annotations"""


import urllib.request

import copy

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

from src import helper
import config

storage_path = 'resources/data/annotations/web_page_html/'
annotations_list = copy.copy(helper.load_json_from_file(config.JUDGMENTS_PATH))

anno_list = list(annotations_list.keys())

# THE HEADER TRICK BELOW IS A HACK THANKS TO:
# https://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
url='http://www.3fatchicks.com/8-benefits-of-echinacea/'
hdr = {'User-Agent':'Mozilla/5.0',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
request=urllib.request.Request(url,None,headers=hdr)
response = urllib.request.urlopen(request)
data = response.read() #



for item in anno_list:
    name_to_use = annotations_list[item]['IMAGE_NAME'] + '.html'
    url = annotations_list[item]['URL']
    try:
        request = urllib.request.Request(url, None, headers=hdr)
        page = urllib.request.urlopen(request)
        o_file = open(storage_path + name_to_use, 'wb')
        o_file.write(page.read())
        o_file.close()
        print('Download SUCCESSFUL FOR: ' + url)
    except Exception as error:
        print(error)
        try:
            o_file = open(storage_path + annotations_list[item]['IMAGE_NAME'] + '.error', 'w')
            o_file.write(annotations_list[item]['IMAGE_NAME'] + ' ' + str(error))
            o_file.close()
            print('Download FAILED FOR: ' + url)
        except Exception as error2:
            o_file = open(storage_path + item + '.error', 'w')
            o_file.write(item + '_' + annotations_list[item]['IMAGE_NAME'] + ' ' + str(error2))
            o_file.close()
            print('Download FAILED FOR AND BAD DATA IN ANNOTATION!: ' + url)

#
# Remote end closed connection without response
# Download FAILED FOR: http://drvee.wordpress.com/2008/10/31/dental-sealants/
#
# Remote end closed connection without response
# Download FAILED FOR: http://healthland.time.com/2010/09/13/would-you-like-some-bpa-with-that-dental-sealant-dear/
#
#     HTTP
#     Error
#     429: Too
#     Many
#     Requests
#     Download
#     FAILED
#     FOR: https: // www.researchgate.net / publication / 236094826
#     _Sealants_for_preventing_dental_decay_in_the_permanent_teeth
#
# HTTP Error 500: Internal Server Error
# Download FAILED FOR: http://www.shielddentalcare.com/dental-sealants/
#
# HTTP Error 500: Internal Server Error
# Download FAILED FOR: http://www.shielddentalcare.com/dental-sealants/
#
# Remote end closed connection without response
# Download FAILED FOR: http://beyondmeds.com/2009/06/30/warnings-of-the-dangers-of-benzodiazepines/
#
# HTTP Error 301: The HTTP server returned a redirect error that would lead to an infinite loop.
# The last 30x error message was:
# Moved Permanently
# Download FAILED FOR: http://www.stuff.co.nz/life-style/well-good/4482524/Echinacea-myth-debunked
