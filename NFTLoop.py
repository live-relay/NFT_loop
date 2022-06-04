#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import os
import traceback
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry




def spliceUrl(url, urlParams):

    ss = requests.session()
    ss.keep_alive = False
    if (not ('?' in url) and urlParams):
        url += '?'
    for key in urlParams:
        if (not url.endswith('?') and not url.endswith('&')):
            url += '&'
        url += (key + '=' + urlParams[key])
    return url




def getPageUrlList(url, page):
    resultList = []
    start = int(page['start'])
    end = int(page['end']) + 1
    for number in range(start, end):
        pageUrl = url
        if (not url.endswith('?') and not url.endswith('&')):
            pageUrl += '&'
        pageUrl += ('page=' + str(number))
        resultList.append({'page': str(number), 'url': pageUrl})
    return resultList


def readConfigContent():
    content = ''
    file = open('./config.json', 'r')
    for line in file:
        content += line
    return content


def makeFileDirs(filePath):
    try:
        index = filePath.rindex('/')
        os.makedirs(filePath[0:index])
    except:
        pass

def extract_address_list_from_file():
    with open('./address.json', 'r') as file:
        data = file.read().replace('\n', '')
        address_list = json.loads(data)
    return address_list

def main():
    configContent = readConfigContent()
    config = json.loads(configContent)

    address_list = extract_address_list_from_file()
    for address in address_list:
        config['urlParams']['user_addr'] = address
        process_data(config)


def process_data(config):
    url = spliceUrl(config['url'], config['urlParams'])
    urlList = getPageUrlList(url, config['page'])
    makeFileDirs(config['output'])
    for element in urlList:
        try:
            response = requests.get(element['url'], timeout=120)
            print('GET ' + element['url'] + ' ' + str(response.status_code))
            if (response.status_code == 200):
                text = response.text
                filePath = config['output']
                formattedFilePath = filePath.format(page=element['page'], wallet = config['urlParams']['user_addr'] )

                file = open(formattedFilePath, 'w')
                file.write(text)
        except Exception as e:
            print('GET ' + element['url'])
            traceback.print_exc()


if __name__ == '__main__':
    main()
