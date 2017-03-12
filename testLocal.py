#!/usr/bin/env python3

import urllib.request
import re
import sys
import time
import requests

encoding = 'utf-8'
url = 'http://localhost:4242/shit'

try:
	headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'}
	print(requests.get(url, allow_redirects=False, headers=headers))
except:
	print('---Network / Plugin ERROR---')
	print('Transformation of', url, 'failed')

