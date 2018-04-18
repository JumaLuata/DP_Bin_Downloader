# -*- coding:utf-8 -*-
import os
import sys
import json
import time
import urllib,urllib2
from bs4 import BeautifulSoup

class dapeng:
    def __init__(self,date):
        self.re_url = date[0]
        self.save_path = os.path.join("binary",str(date[1]))
        if os.path.exists(self.save_path) is False:
            os.makedirs(self.save_path)

    def start(self):
        dapeng.__get_bin(self, self.re_url)
        cmd_shell ('Successful Download.')
        cmd_shell ('The binaries are saved at '+ self.save_path)
        os._exit(0)

    def __get_bin(self,r_url):
        cmd_shell(r_url)
        _json = dict()
        _request = []
        case_num = 0
        html = urllib2.urlopen(r_url).read()
        soup = BeautifulSoup(html,"lxml")
        name = ['id','test_case','compiler','target']
        for tr in soup.find('tbody', ).find_all('tr'):
        	if str(tr.find('td', id = "td_list_needrun")=="Yes"):
	            _json[name[0]] = int(tr.find('td', id="td_list_id").get_text())
	            _json[name[1]] = str(tr.find('td',id="td_list_mcuauto_testcase").get_text())
	            _json[name[2]] = str(tr.find('td',id="td_list_mcuauto_compiler").get_text())
	            _json[name[3]] = str(tr.find('td', id="td_list_mcuauto_target").get_text())
	            _request.append(eval(str(_json).replace("\\n","").replace("\\t","")))
	            
        #Get the download address
        in_json = json.dumps(_request)
        req = json.loads(in_json)
        cmd_shell ( "\nThere are *" + str(case_num) + "* binaries to download.\n")
        cmd_shell ('The binaries are saved at ' + self.save_path)

        #Download
        for i in range(case_num):
            case_url = 'http://10.192.225.198/dapeng/information/requestdetail/'+str(req[i].get('id'))
            try:
                html_case = urllib2.urlopen(case_url).read()
                soup_case = BeautifulSoup(html_case, "lxml")
                td = soup_case.find_all('table')[3].find_all('td')[3]
                bin_url = 'http://10.192.225.198' + str(td.a['href'])
                bin_format = str(td.a.get_text()).split('.')
                bin_name = str(req[i].get('compiler')) + '@' + str(req[i].get('target')) + '@' + str(req[i].get('test_case')) + '.' + bin_format[1]
                urllib.urlretrieve(bin_url, os.path.join(self.save_path,bin_name))
                cmd_shell(str(i+1) + ' : [ ' + bin_name + ' ] has been downloaded.')
                time.sleep(5)
            except Exception as e:
                cmd_shell (str(e))
                os._exit(-1)

def cmd_shell(str=''):
    sys.stdout.write(str+'\n')
    sys.stdout.flush()

if __name__ == '__main__':
    DEBUG = 0
    argvs = sys.argv
    request_url = ''
    request_id = ''

    if DEBUG == 1:
        request_url = "http://10.192.225.198/dapeng/information/request/13819/?buildresult=1"
        request_id = '13819'
    else:
        if len(argvs) == 2:
            request_url = "http://10.192.225.198/dapeng/information/request/" + str(argvs[1]) + '/?buildresult=1'
            request_id = str(argvs[1])
            cmd_shell('Download All?(y/n):')
            sw_all = sys.stdin.read(1)
            if sw_all == 'y':
                request_url += '&page=all'
        else:
            print "\n* ERROR!"
            print "\n* Please input a useful Dapeng request id."
            print "\n* Like: python DP_Bin_Downloader.py <request_id>"
            os._exit(-1)

    request = [request_url ,request_id]
    dapeng(request).start()
