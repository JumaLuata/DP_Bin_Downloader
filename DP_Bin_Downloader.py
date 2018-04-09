# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib
import time
from requests import Session
from bs4 import BeautifulSoup


class dapeng:
    def __init__(self,date):
        self.re_url = date[0]
        self.save_path = 'binary/'+date[1]+'/'
        if os.path.exists(self.save_path) is False:
            os.makedirs(self.save_path)
        self.headers={
            "Host": "10.192.225.198",
            "Cookie": "csrftoken=2FKWEGBZ3QWCEGduuElOzT5kIcZtAvVx",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }

    def start(self):
        self.s = Session()  # 定义一个Session()对象
        dapeng.__get_bin(self, self.re_url)
        cmd_shell ('Successful Download.')
        cmd_shell ('The binaries are saved at '+ self.save_path)
        os._exit(0)

    def __get_bin(self,r_url):
        cmd_shell(r_url)
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
        #Get the download address
        in_json = json.dumps(_request)
        req = json.loads(in_json)
        cmd_shell ( "\nThere are *" + str(case_num) + "* binaries to download.\n")
        cmd_shell ('The binaries are saved at ' + self.save_path)

        #Download
        for i in range(case_num):
            case_url = 'http://10.192.225.198/dapeng/information/requestdetail/'+str(req[i].get('id'))
            html_case = ''
            try:
                html_case = self.s.get(case_url, headers=self.headers).text
            except:
                print 'Website access failed!'
                os._exit(1)
            soup_case = BeautifulSoup(html_case, "lxml")
            table = soup_case.find('div', class_="second-div-custom").find_all('table')
            td = table[2].find_all('td', class_='td-custom')
            case_url = 'http://10.192.225.198' + str(td[3].a['href'])
            case_name = str(req[i].get('compiler'))+'@'+str(req[i].get('target'))+'@'+str(req[i].get('test_case'))+'.out'
            urllib.urlretrieve(case_url, (self.save_path+case_name))
            cmd_shell (str(i)+' : [ '+case_name+' ] has been downloaded.')
            time.sleep(5)#延迟5S等文件下载完

def cmd_shell(str=''):
    sys.stdout.write(str+'\n')
    sys.stdout.flush()

if __name__ == '__main__':
    DEBUG = 0
    argvs = sys.argv
    request_url = ''
    request_id = ''

    if DEBUG == 1:
        request_url = "http://10.192.225.198/dapeng/information/request/13819"
        request_id = '13819'
    else:
        if len(argvs) == 2:
            request_url = "http://10.192.225.198/dapeng/information/request/" + str(argvs[1])
            request_id = str(argvs[1])
            #cmd_shell("The request url is "+ request_url)
            cmd_shell('Download All?(y/n):')
            sw_all = sys.stdin.read(1)
            if sw_all == 'y':
                request_url += '/?page=all'
        else:
            print "\n* ERROR!"
            print "\n* Please input a useful Dapeng request id."
            print "\n* Like: python DP_Bin_Downloader.py <request_id>"
            os._exit(1)

    request = [request_url ,request_id]
    dapeng(request).start()
