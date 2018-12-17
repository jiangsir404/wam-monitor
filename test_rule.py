#!/usr/bin/env python		
#coding:utf-8

'''
测试脚本，
如果selector 匹配出了内容，且显示两次获取md5是一样的，说明规则正确。
如果未匹配出内容，或md5不一样，说明规则有问题。
'''

import config
from log import logger
import hashlib
from download import Downloader
from bs4 import BeautifulSoup as bs


md5 = lambda x:hashlib.new('md5',x).hexdigest()


def process_selector(selector,string):
	soup = soup = bs(string,"html.parser")
	if '.' in selector:
		tag = selector.split('.')[0]
		_class = {'class':selector.split('.')[1]}
		res = soup.find(name=tag,attrs=_class)
		print 'selector get:',res 
		if not res:
			logger.error('wrong selector')
			exit()
		return res

	if '#' in selector:
		tag = selector.split('#')[0]
		_class = {'id':selector.split('#')[1]}
		res = soup.find(name=tag,attrs=_class)
		print 'selector get:',res 
		if not res:
			logger.error('wrong selector')
			exit()
		return res 



selector = "div.download_body" # tpshop selector
selector = "div.repository-content" #GitHub selector
selector = "ol.breadcrumb met-pinghei margin-vertical-20 padding-0 font-size-16" #metinfo selector
selector = "div#download" #destoon

def test_rule(url,regexp=''):
	download = Downloader()
	html1 = download.get(url)
	#print html1
	text1 = process_selector(selector,html1.text)
	md51 = md5(text1.encode('utf-8'))
	html2 = download.get(url)
	text2 = process_selector(selector,html2.text)
	md52 = md5(text2.encode('utf-8'))
	if md51 == md52:
		print 'md5 is same'
	else:
		print md51,md52


test_rule('http://www.destoon.com/download/')

