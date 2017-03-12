#!/usr/bin/env python3
import fileinput
import time
import requests
import datetime
import re

user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
base_sleep = 600
sleep_step = 300
counter = 0
tries_on_error = 10
debug = True
requests_outlink_counter = 0
timeout = 60

def time_after_sleep(seconds):
    return (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).time()

def transform_outlink(url, tries, sleep):
    global requests_outlink_counter
    tries -= 1
    if sleep and requests_outlink_counter != 0:
        print('Sleeping for', sleep, 's [till ' +  str(time_after_sleep(sleep)) + ']')
        time.sleep(sleep)
    try:
        requests_outlink_counter += 1
        headers = {'user-agent':user_agent}
        response = requests.get(url, allow_redirects=True, headers=headers, timeout=timeout)
        if response.url != url:
            return response.url
        else:
            raise ValueError('Page responded with crawler protection')
    except:
        print('---Network / Plugin ERROR---')
        print('Error on request count:', requests_outlink_counter)
        print('Transformation of', url, 'failed')
        print('Retries left:', tries)	
        if tries:
            transform_outlink(url, tries, sleep+sleep_step)
def main():
    links = []
    for line in fileinput.input():
        for link in re.finditer(r'https?://bs.to/out/(\d*)', line, re.I):
            if link:
                links.append(link.group(0))
    print('Found', len(links), 'links')
    for link in links:
        print('Transforming', link,)
        print(transform_outlink(link, tries_on_error, base_sleep))

main()
