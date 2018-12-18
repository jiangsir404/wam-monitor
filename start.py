#!/usr/bin/env python		
#coding:utf-8

from download import Downloader
import config
from notification import Notification
from log import logger
import hashlib
from bs4 import BeautifulSoup as bs
import sys  
import time
reload(sys)  
sys.setdefaultencoding('utf8')   

md5 = lambda x:hashlib.new('md5',x).hexdigest()
dataConfig = config.Config()

debug = False

def start(rule_types):
    rules = config.get_rules(rule_types)
    if len(rules) == 0:
        logger.critical('get rules failed, rule types not found!')
        exit(0)
    logger.info('rules length: {rl}'.format(rl=len(rules)))
    return rules

def process_github(html):
	soup = bs(html.text,"html.parser")
	res = soup.find_all(name="div", attrs={'class':'repository-content'})
	#print res[0].text
	return res[0]

def process_selector(rule,string):
	selector = rule.selector
	soup = soup = bs(string,"html.parser")
	if '.' in selector:
		tag = selector.split('.')[0]
		_class = {'class':selector.split('.')[1]}
		res = soup.find(name=tag,attrs=_class)
		#print res 
		if not res:
			logger.error('%s app set wrong selector'%rule.corp)
			return None
		return res

	elif '#' in selector:
		tag = selector.split('#')[0]
		_class = {'id':selector.split('#')[1]}
		res = soup.find(name=tag,attrs=_class)
		if not res:
			logger.error('%s app set wrong selector'%rule.corp)
			return None
		return res 
	else:
		logger.error('%s app set wrong selector'%rule.corp)
		return None

def process(rules):
	for rule in rules:
		download = Downloader()
		html = download.get(rule.url)
		if html == None:
			logger.error('%s无法访问'%rule.corp)
			continue
		elif rule.selector:
			text = process_selector(rule,html.text)
		elif rule.types == 'github':
			rule.selector = "div.repository-content"
			text = process_selector(rule,html.text)
		else:
			text = html.text
		if text == None:
			continue
		hash_list = dataConfig.hash_list()
		html_md5 = md5(text.encode('utf-8')) #text编码为unicode
		if debug:
			print 'html:',text[:20]
			print 'hash_list:',hash_list
			print 'html_md5',html_md5
		
		if len(hash_list) > 0:
			if rule.corp in hash_list.keys():
				if html_md5 == hash_list[rule.corp]:
					logger.info('%s no change'%rule.corp)
				else: #如果hash改变，说明有更新，发送邮件通知
					logger.warning('%s has update'%rule.corp)
					dataConfig.update_hash(rule.corp,html_md5)
					context = '<a href={0}>{0}</a>'.format(rule.url)
					Notification(rule.message,'rivirsec@163.com','').notification(context)
			else: #如果不存在该corp,则添加该hash
				logger.info('添加新的监控app:%s'%rule.corp)
				dataConfig.add_hash(rule.corp,html_md5)
		else: #如果hash列表为空，则先初始化
			logger.info('wam init ....')
			dataConfig.add_hash(rule.corp,html_md5)


def test(app):
	
	#app = 'github'
	rules = start(app)
	#print rules
	process(rules)


def monitor(app):
	while(1):
		rules = start(app)
		process(rules)
		logger.info('sleep 30s')
		time.sleep(30)


if __name__ == '__main__':
	app = sys.argv[-1]
	#test(app)
	monitor(app)