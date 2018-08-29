from ELModel import loadData
from utils import readDataFromKeys
import json
def checkHttp(tablename,hostname):
    serverSet,clientSet,recordTimeSet = set(),set(),set()
    detail = {
        "query": {
            "match_phrase": {
                "HTTP_Client.Host": hostname
            }
        }
    }
    dataGen = loadData(table=tablename, detail=detail)
    for dataList in dataGen:
        for data in dataList:
            data = data['_source']
            firstIP = readDataFromKeys(data,'ConnectInfor.first')
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            recordTime = readDataFromKeys(data, 'ConnectInfor.RecordTime')
            get = readDataFromKeys(data, 'HTTP_Client.GET')
            post = readDataFromKeys(data, 'HTTP_Client.POST')
            print(json.dumps(data))
            if get is not None:
                print(get)
            if post is not None:
                print(post)
            serverSet.add(serverIP)
            clientSet.add(firstIP)
            recordTimeSet.add(recordTime)
    print('serverSet', serverSet)
    print('clientSet', clientSet)
    # print('recordTimeSet', recordTimeSet)




if __name__=='__main__':
    hostnames = ['121.51.140.139', 'vdp2precv.app.cntvwb.cn', '220.181.131.207', 'static5.baihe.com', 'apiv2.sohu.com', 'cl.vd.f.360.cn', 'n.sinaimg.cn', 'szminorshort.weixin.qq.com', 'bj-trail.ntalker.com', 'www.castu.tsinghua.edu.cn', 'pic7.iqiyipic.com', 'report.boxsvr.niu.xunlei.com:6643', 'sdl.360safe.com', 'www.eeban.com', 'js.passport.qihucdn.com', 'update.gouwu.sogoucdn.com', 'www.cae.cn', 'cgi.qqweb.qq.com', 'mapping.yoyi.com.cn', '106.11.42.21', '220.181.132.30', '3366.gtimg.com', 'news.sohu.com', 'dmd.metaservices.microsoft.com', 'r1.ykimg.com', 'd3g.qq.com', 'master13.teamviewer.com', 'ads.service.kugou.com', 'rq.upgrade.cloud.duba.net', '166.111.9.201', 'recv-wd.gridsumdissector.com', 'video.weibo.com', 'ime.sogou.com', 'aeu.alicdn.com', 'stat.pc.music.qq.com', 'master3.teamviewer.com', 'wan01.sogoucdn.com', 'artistpicserver.kuwo.cn', 'rgom10-en.url.trendmicro.com:80', 'www.soduso.com', '166.111.185.35:8080', 'at2.jyimg.com', 'www.iqiyipic.com', 'audio.xmcdn.com', 'discuz.gtimg.cn', 'planet.farnell.com', 'dayan.sinaapp.com', 'tb.himg.baidu.com', '106.38.184.136', 'image.so.com', 'mgxhtj.kuwo.cn', 'sdup.360.cn', '182.254.52.245', 'www.innovation.tsinghua.edu.cn', 'trustasia2-ocsp.digitalcertvalidation.com', 'lite-msa.hupu.com', '121.51.77.100', 'assets.dxycdn.com', 'fanyi.baidu.com', '116.62.182.15', 'www.soyoung.com', 'gpu-kappa:6007', '220.181.156.58', 'hf.myhome.tsinghua.edu.cn', 'us.blizzard.com', 'carat-cm.cn.miaozhen.com', 'adse.ximalaya.com', 'apps.wusp.qq.com', 'stat.5sing.kugou.com', 'cu001.sjk.ijinshan.com', '210.52.217.139', 'push.mail.163.com', 'mass.tsinghua.edu.cn:80', 'diskapi.baidu.com', 'newstu.myhome.tsinghua.edu.cn', 'g.msn.com', 'www.googletagservices.com', 'log.qvb.qcloud.com', 'si1.go2yd.com', 'down.idc3389.top', 'm.mall.icbc.com.cn', 'i-29.b-44396.ut.bench.utorrent.com', 'mc.corel.com', '166.111.72.99', 'commdata.v.qq.com', 'qzapp.qlogo.cn', '58.247.204.139', '157.255.173.146', 'search.video.iqiyi.com', 'i.gtimg.cn', 's.wisdom.www.sogou.com', 'ajax.58pic.com', 'proxy2.shellemon.com', 'update.pdfcomplete.com', 'ucstucmobile.tjcu.u3.ucweb.com:8080', 'scan.call.f.360.cn', '182.254.48.92', 'cdn.content.prod.cms.msn.com', 'hkshort.weixin.qq.com', 'ssl.gstatic.com:443']
    checkHttp('http_20180825','169.229.150.100')
