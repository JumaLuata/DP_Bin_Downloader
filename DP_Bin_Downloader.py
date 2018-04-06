# -*- coding:utf-8 -*-
import os
import sys
import json
import re
import urllib
import time
from requests import Session
from bs4 import BeautifulSoup

#downloader binary
#urllib.urlretrieve("url","binary/ide @ target @ testcase .out")
class dapeng:
    def __init__(self,date):
        self.re_url=date
        self.page='all'
        self.headers={
            "Host": "10.192.225.198",
            "Cookie": "csrftoken=2FKWEGBZ3QWCEGduuElOzT5kIcZtAvVx",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }

    def start(self):
        self.s = Session()  # 定义一个Session()对象
        dapeng.__get_bin(self, self.re_url)
        print 'Successful Download.'
        os._exit(0)

    def __get_bin(self,r_url):
        print r_url
        _json = dict()
        _request = []
        case_num = 0
        html = self.s.get(r_url,headers=self.headers).text
        soup = BeautifulSoup(html,"lxml")
        name = ['id','test_case','compiler','target']
        for tr in soup.find('div', class_="second-div-custom").find('div', id="list_div").find('tbody', ).find_all('tr'):
            _json[name[0]] = int(tr.find('td', id="td_list_id").get_text())
            _json[name[1]] = str(tr.find('td',id="td_list_mcuauto_testcase").get_text())
            _json[name[2]] = str(tr.find('td',id="td_list_mcuauto_compiler").get_text())
            _json[name[3]] = str(tr.find('td', id="td_list_mcuauto_target").get_text())
            _request.append(eval(str(_json).replace("\\n","").replace("\\t","")))
            case_num += 1

        in_json = json.dumps(_request)
        req = json.loads(in_json)
        print "There are " + str(case_num) + " to download.\n"

        for i in range(case_num):
            case_url = 'http://10.192.225.198/dapeng/information/requestdetail/'+str(req[i].get('id'))
            html_case = self.s.get(case_url, headers=self.headers).text
            soup_case = BeautifulSoup(html_case, "lxml")
            table = soup_case.find('div', class_="second-div-custom").find_all('table')
            td = table[2].find_all('td', class_='td-custom')
            case_url = 'http://10.192.225.198' + str(td[3].a['href'])
            case_name = 'binary/'+str(req[i].get('compiler'))+'@'+str(req[i].get('target'))+'@'+str(req[i].get('test_case'))+'.out'
            urllib.urlretrieve(case_url, case_name)
            print str(i)+' : [ '+case_name+' ] has been downloaded.'
            time.sleep(1)


if __name__ == '__main__':

    argvs = sys.argv
    DEBUG = 1
    request_url = ''

    if DEBUG == 1:
        request_url = "http://10.192.225.198/dapeng/information/request/13819"
    else:
        if len(argvs) == 2:
            request_url = "http://10.192.225.198/dapeng/information/request/" + str(argvs[1])
            print "The request url is "+ str(request_url)
        else:
            print "\n* ERROR!"
            print "\n* Please input a useful Dapeng request id."
            print "\n* Like: python DP_Bin_Downloader.py <request_id>"
            os._exit(1)

    dapeng(request_url).start()
