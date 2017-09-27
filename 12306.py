import urllib.request as ur
import urllib.error as uerror
import urllib.parse as up
import gzip
import time
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs
import json

#user define
import userdef


MainCookieURL = 'https://kyfw.12306.cn/otn/leftTicket/init'
INDEX = 'https://kyfw.12306.cn/otn/leftTicket/queryX'

date = "2017-10-07"
#from_station = "STS"
from_station_ch ='古田会址'
#to_station = "XMS"
to_station_ch = '厦门'
purpose_codes = "ADULT"

station = dict()


def GetMainCookie():
    userdef.CookieSave()
    opener = userdef.GeneralSSLOpener()
    req = userdef.GeneralRequest(MainCookieURL)
    try:
        response = opener.open(req)
        userdef.CookieSave()
    except uerror.HTTPError as e:
        print(e.reason)
    except uerror.URLError as e:
        print(e.reason)
    except Exception as e:
        print(e)
    finally:
        return

def GetRequest():
    global station
    url = INDEX + "?" + "leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" \
          + station[from_station_ch] + "&leftTicketDTO.to_station=" + station[to_station_ch] + "&purpose_codes=" + purpose_codes
    req = userdef.GeneralRequest(url)
    req.add_header('Referer','https://kyfw.12306.cn/otn/leftTicket/init')

    #general the cookie
    seq = ';'
    cookielist = list()
    for item in userdef.COOKIE:
        cookielist.append(item.name+'='+item.value)
    #cookielist.append('fp_ver=4.5.1')
    cookielist.append('RAIL_DEVICEID=nyWrp4dKm5xSjZ9bSxY7Khmwvhj_aHsz6OFPrzPwdPRau6Loepve1rAu5py1gUO4PS2IEoq_k1X1Uxdxj9j_4inXyTLBEbt6IdluRoIMFqOZIDN_qCvm9cqOKXBojfTYPzpHxZcMpr6wxhfHqtz2C1TLZOfTS3Om')
    temp = from_station_ch+','+ station[from_station_ch]
    cookielist.append('_jc_save_fromStation='+up.quote(temp))
    temp = to_station_ch+','+station[to_station_ch]
    cookielist.append('_jc_save_toStation='+up.quote(temp))
    cookielist.append('_jc_save_fromDate='+date)
    cookielist.append('_jc_save_toDate='+date)
    cookielist.append('_jc_save_wfdc_flag=dc')
    #cookielist.append('RAIL_EXPIRATION='+str(int(time.time()+86400)))
    cookie = seq.join(cookielist)

    req.add_header('Cookie',cookie)
    return req

def GetStationInfo():
    global station
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    response = userdef.GetGeneralResponse(url)
    charset = userdef.GetCharSet(response)
    info = response.read().decode(charset)
    info = info.split('=')

    if len(info) != 2:
        raise ValueError('can not get the station information!')    
    
    info = info[1]
    info = info.strip(';\'')
    info = info.split('@')
    for item in info:
        if item.strip(): 
            item = item.split('|')
            if item[1] in station:
                raise ValueError('Station info error',item[1])
            station[item[1]] = item[2]


def ParseTicket(jsondata,charset):
    jsondata = json.loads(jsondata,encoding=charset)
    if 'data' not in jsondata:
        raise ValueError('Ticket info error')
    
    if 'result' not in jsondata['data']:
        raise ValueError('Ticket info result error')

    for item in jsondata['data']['result']:
        print(item)

    
        
    print('test')
    pass


if __name__ == '__main__':
    #get the cookie
    GetMainCookie()
    #get the station info
    GetStationInfo()    
    #get the special request
    req = GetRequest()

    opener = userdef.GeneralSSLOpener()
    response = opener.open(req)

    #get the ticket information
    #unzip the content
    isgzip = response.headers.get('Content-Encoding')
    if isgzip and isgzip == 'gzip':
        data = gzip.decompress(response.read())
    else:
        raise ValueError('not zip data,modify the code')
    
    charset = userdef.GetCharSet(response)

    #decode the data to the charset
    data = data.decode(charset)

    #parse the ticket information
    ParseTicket(data,charset)