#!/usr/bin/env python        
#coding:utf-8

import os
import time
import json
import traceback
import configparser
from colorprint import logger

home_path = os.path.join(os.getcwd(),'data')
code_path = os.path.join(home_path, 'codes')
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
config_path = './config.ini'
rules_path = "./rule.ini"
# rules_path = os.path.join(project_directory, 'rules.gsil')


def get(level1=None, level2=None):
    """
    Get config value
    :param level1:
    :param level2:
    :return: string
    """
    if level1 is None and level2 is None:
        return
    config = configparser.ConfigParser()

    config.read(config_path)
    value = None
    try:
        value = config.get(level1, level2)
    except Exception as e:
        print(level1, level2)
        traceback.print_exc()
        print("config.ini file configure failed.\nError: {0}".format(e))
    return value


class Rule(object):
    def __init__(self, types=None, corp=None,  url='normal-match', selector=None, message=None):
        # eg: types=app,corp=thinkphp,url=http://xxx/commit ,message= thinkhp有commit更新
        self.types = types
        self.corp = corp
        self.selector = selector
        self.url = url
        self.message = message


def get_rules(rule_types):
    try:
        with open(rules_path) as f:
            rules_dict = json.load(f)
    except Exception as e:
        logger.critical('please config rules.gsil!')
        logger.critical(traceback.format_exc())

    #print rules_dict

    if ',' in rule_types:
        rule_types = rule_types.split(',')
    else:
        rule_types = [rule_types]
    rules_objects = []
    for types, rule_list in rules_dict.items(): #types=app rule_list = {0,1,2}
        # 仅选择指定的规则类型
        if types in rule_types:
            for corp_name, corp_rules in rule_list.items(): #corp_name=thinkphp corp_rules = {}
                #print 'corp_rules',corp_rules
                url = corp_rules['url'].strip() if corp_rules.has_key('url') else None
                message = corp_rules['message'].strip() if corp_rules.has_key('message') else '%s has change'%corp_name
                selector = corp_rules['selector'].strip() if corp_rules.has_key('selector') else None

                #print "url,message:",url,message
                r = Rule(types, corp_name, url, selector,message)
                rules_objects.append(r)
    return rules_objects


class Config(object):
    def __init__(self):
        self.project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        if os.path.isdir(home_path) is not True:
            os.makedirs(home_path)
        self.hash_path = os.path.join(home_path, 'hash')
        if os.path.isfile(self.hash_path) is not True:
            open(self.hash_path, 'a').close()
        # self.data_path = os.path.join(home_path, 'data')
        # if os.path.isdir(self.data_path) is not True:
        #     os.makedirs(self.data_path)
        # self.run_data = os.path.join(home_path, 'run')
        # self.run_data_daily = os.path.join(home_path, 'run-{date}'.format(date=time.strftime('%y-%m-%d')))

    def hash_list(self):
        """
        Get all hash list
        :return: list
        """
        with open(self.hash_path) as f:
            hashs = {}
            c = f.read().splitlines()
            for i in c:
                hashs[i.split(':')[0]] = i.split(':')[1]

            return hashs

    def add_hash(self, corp ,sha):
        """
        Append hash to file
        :param sha:
        :return: True
        """
        with open(self.hash_path, 'a') as f:
            f.write('{corp}:{line}\n'.format(corp=corp,line=sha))
        return True

    def update_hash(self,corp,sha):
        file_data = ""
        with open(self.hash_path,'r') as f:
            for i in f:
                hash_corp = i.split(':')[0]
                hash_sha = i.split(':')[1].strip()
                if hash_corp == corp:
                    i = i.replace(hash_sha,sha)
                file_data += i

        with open(self.hash_path,'w') as f:
            f.write(file_data)



    @staticmethod
    def copy(source, destination):
        """
        Copy file
        :param source:
        :param destination:
        :return:
        """
        if os.path.isfile(destination) is not True:
            logger.info('Not set configuration, setting....')
            with open(source) as f:
                content = f.readlines()
            with open(destination, 'w+') as f:
                f.writelines(content)
            logger.info('Config file set success({source})'.format(source=source))
        else:
            return