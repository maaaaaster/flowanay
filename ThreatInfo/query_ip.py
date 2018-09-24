#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import threading
import queue
import json
import time
import os
# import pymysql
import time
import datetime
import re
#from VirusCollector.logger import Logger

analysePath = "/home/juquanyong/attack_ip/"
analyseResult="./query.ip.result"

queue = queue.Queue()
# cur = pymysql.cursors
re_total = {}
cnt = 0
#logger = Logger(__file__.split("/")[-1])

# preInsertSql = "INSERT INTO ip_info (pcad_id,ip,ipvoid_result,mxtool_result,cisco_result,virustotal_result,result) values (%s,%s,%s,%s,%s,%s,%s)"
validePeriod = 30


class query_ip(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def ipvoid(self, ip_name):
        url_ipvoid = r"http://www.ipvoid.com/ip-blacklist-check/"
        finsh = False
        while not finsh:
            try:
                payload = {'ip': ip_name}
                r = requests.post(url_ipvoid, data=payload)
                finsh = True
            except Exception as ex:
                print(str(ex))
        if "BLACKLISTED" in str(r.text):
            return "ipvoid:Y"
        else:
            return "ipvoid:N"

    '''
    def bulkblacklist(self,ip_name):
        url_bulk=r'http://www.bulkblacklist.com/'
    '''

    def mxtoolbox(self, ip):
        url = r"https://mxtoolbox.com/Public/Lookup.aspx/DoLookup2"
        payload = json.dumps(
            {"inputText": "blacklist:" + ip, "resultIndex": 1})
        headers = {
            "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Content-Type": r"application/json; charset=UTF-8",
            "Referer": r"https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a41.206.73.246&run=toolpage",
            "Accept": r"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": r"gzip, deflate, br",
            "Accept-Language": r"zh-CN,zh;q=0.9",
            "Connection": r"keep-alive",
            "Content-Length": r"55",
            "Host": r"mxtoolbox.com",
            "MasterTempAuthorization": r"509f6bbb-2d49-4706-aecb-9da915303bf2",
            "Origin": r"https://mxtoolbox.com",
            "X-Requested-With": r"XMLHttpRequest"
            }
        finsh = False
        while not finsh:
            try:
                r = requests.post(url, data=payload, headers=headers)
                finsh = True
            except Exception as e:
                print(str(e))
        if "We notice you are on a blacklist" in str(r.text):
            return "mxtoolbox:Y"
        else:
            return "mxtoolbox:N"

    def cisco(self, ip):
        url = r"https://talosintelligence.com/sb_api/blacklist_lookup?query_type=ipaddr&query_entry=" + ip
        headers = {
            "user-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Accept": r"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": r"gzip, deflate, br",
            "Accept-Language": r"zh-CN,zh;q=0.9",
            "referer": r"https://talosintelligence.com/reputation_center/lookup?search=" + ip,
            "cookie": r"__cfduid=df184adec464699be8bfe86c1832ef5e11510555968; _gat=1; _ga=GA1.2.161703073.1510555972; _gid=GA1.2.1788890643.1512549480; _talos_website_session=RFgybWFpUmVVYVZPUW5ZSmxOaFFYaURZU1RaMlBsSFp1YzVCZmh5aDBzRDZmbkVGSXk4SHpFYW8yL0doc3RYRjZTOHdVRGkwcjJlWWtLUi81Y21xajlEVERFTWsrVFpHNE54Z1oyelZlWVZaNEp3WTJ5cFpJcEg1VVFUWDgyellxMFM3NmM3WXlnSWo1SlVlbFRjbU1JcmtrSXNqK1FiZEJHc0xwQXlkS0lZZnB1R3gwWUt2TmVwUE9VdWRQME5sbmZpV3RUdXVxY2V1V004eW1ianQvMVpHVy9vS20zZFU4ODZtR2RqUVhCcU5EZmlBRm5lSVlYKzdUd0RSbFl5c0w5ZU02cDdkSUlGdUlpc0hqeHF0Uk9xUlhjampjVTJKL3FxaXdLa3g0cnhUYUFGbWpnS0VSaXJXSHVmVUY3MjctLUZRaWpiaFFmYlc2eU5XdDhTQ2htUlE9PQ%3D%3D--b77a9ae15fadcf225b5a5fcbbfe262da3de66f7a"
            }
        payload = {"query_type": "ipaddr", "query_entry": ip}
        finsh = False
        while not finsh:
            try:
                r_info = requests.get(url, headers=headers, data=payload)
                finsh = True
            except Exception as ex:
                print(str(ex))
        # print r_info.text
        if "classifications" in r_info.text:
            return r_info.text[r_info.text.index('classifications":["') + 19:r_info.text.index('"]', r_info.text.index(
                'classifications":["') + 19)]
        else:
            return "maySafe"

    def virustotal(self, ip):
        url = "https://www.virustotal.com/en/ip-address/" + ip + "/information/"
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "accept-encoding": "gzip, deflate, br",
                   "accept-language": "zh-CN,zh;q=0.9",
                   "cache-control": "max-age=0",
                   "content-length": "19",
                   "content-type": "application/x-www-form-urlencoded",
                   "cookie": r"VT_PREFERRED_LANGUAGE=en-us; __utma=194538546.174638165.1513582037.1513582037.1513582037.1; __utmc=194538546; __utmz=194538546.1513582037.1.1.utmcsr=cybercrime-tracker.net|utmccn=(referral)|utmcmd=referral|utmcct=/index.php; _ga=GA1.2.174638165.1513582037; _gid=GA1.2.2129582753.1513585172; _gat=1; __utmt=1; __utmb=194538546.43.10.1513582037",
                   "origin": "https://www.virustotal.com",
                   "referer": r"https://www.virustotal.com/en/",
                   "upgrade-insecure-requests": r"1",
                   "user-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
                   }
        normalSearch = False
        while not normalSearch:
            response = requests.get(url)
            if (re.match(r'[\s\S]*(id="detected-urls")[\s\S]*"', response.text)):
                normalSearch = True
            else:
                pass
                #logger.debug("search virustotal alnormal." +
                             #"\n" + response.text)
        responseContent = response.text
        if self.deteched(responseContent) and self.recent(responseContent):
            return "virustotal:Y"
        else:
            return "virustotal:N"

    def deteched(self, responseContent):
        match_object = re.match(
            '[\s\S]*(id="detected-urls")[\s\S]*?([\d/]+)</span>[\s\S]*', responseContent)
        if match_object:
            if match_object.group(2):
                if 0 == match_object.group(2).split("/")[0]:
                    return False
                else:
                    return True

    def recent(self, responseContent):
        match_object = re.match(
            r'[\s\S]*(id="detected-urls")[\s\S]*?<span>([\d\s:-]+)</span>[\s\S]*', responseContent)
        if match_object:
            if match_object.group(2):
                if match_object.group(2):
                    date = time.strptime(
                        match_object.group(2), "%Y-%m-%d %H:%M:%S")
                    # ÓÐÊ±·ÖÃë£¬ËùÒÔÌì¼Ó1
                    deadTime = datetime.datetime(
                        date[0], date[1], date[2]) + datetime.timedelta(days=1)
                    # ¼ì²âÓÐÐ§ÌìÊý
                    deadTime = datetime.datetime(
                        date[0], date[1], date[2]) + datetime.timedelta(days=validePeriod)
                    return (deadTime - datetime.datetime.now()).days > 0
            else:
                return False

    def run(self):
        while 1:
            try:
                ip = self.queue.get().strip()
                #cnt+=1
                #print(cnt)
                print(ip)
                time.sleep(2)
                if ip in re_total:
                    self.queue.task_done()
                    continue

                re_ipvoid = self.ipvoid(ip)
                if str(re_total.get(ip)) == "None":
                    re_total[ip] = [re_ipvoid]
                else:
                    if re_ipvoid not in re_total[ip]:
                        re_total[ip].append(re_ipvoid)

                re_mxtoolbox = self.mxtoolbox(ip)
                if str(re_total.get(ip)) == "None":
                    re_total[ip] = [re_mxtoolbox]
                else:
                    if re_mxtoolbox not in re_total[ip]:
                        re_total[ip].append(re_mxtoolbox)

                re_cisco = self.cisco(ip)
                if str(re_total.get(ip)) == "None":
                    re_total[ip] = [re_cisco]
                else:
                    if re_cisco not in re_total[ip]:
                        re_total[ip].append(re_cisco)

                    # ÍøÕ¾¶Ô²éÑ¯´ÎÊýÓÐÏÞÖÆ
                    #                 re_virustotal = self.virustotal(ip)
                    #                 if str(re_total.get(ip)) == "None":
                    #                     re_total[ip] = [re_virustotal]
                    #                 else:
                    #                     if re_virustotal not in re_total[ip]:
                    #                         re_total[ip].append(re_virustotal)

                self.queue.task_done()
            except Exception as e:
                print(e)
                self.queue.task_done()
                return



def work():
    fw = open(analyseResult, "w")
    for file in os.listdir(analysePath):
        global re_total,cnt
        re_total = {}
        print(file)
        f = open(analysePath + file)
        ip_list = []
        for line in f.readlines():
            ip_list.append(line.strip('\r\n'))
        f.close()  # ÔÚIP void £¬txtoolbox,cisco²éÑ¯¶ÔÓ¦ipÊÇ²»ÊÇÔÚblacklist
        print(ip_list)
        t = query_ip(queue)
        t.setDaemon(True)
        t.start()
        for ip in ip_list:
            queue.put(ip)
        queue.join()
        time.sleep(1)
        
        for (k, v) in re_total.items():
            print(k,v)
            fw.write(str(k) + "\t" + str(v) + "\n")
    fw.close()

work()
