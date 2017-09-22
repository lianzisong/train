import ssl

import http.cookiejar as cookielib

import urllib.request as ur


#global cookie
COOKIE = cookielib.MozillaCookieJar('cookie.txt')
#global ssl context
CONTEXT = ssl._create_unverified_context()

def CookieSave():
    COOKIE.save(ignore_discard=True,ignore_expires=True)

def GeneralRequest(url):
    req = ur.Request(url, method='GET', )
    req.add_header('Accept', '*/*')
    req.add_header('Accept-Encoding', 'gzip, deflate, br')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Connection', 'keep-alive')
    req.add_header('If-Modified-Since', '0')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    return req

def GeneralSSLOpener():
    opener = ur.build_opener(ur.HTTPCookieProcessor(COOKIE), ur.HTTPSHandler(context=CONTEXT))
    return opener

def GetGeneralResponse(url):
    opener = GeneralSSLOpener()
    req = GeneralRequest(url)
    response = opener.open(req)
    return response

def GetCharSet(response):
    charset = response.headers.get('Content-Type')
    if charset:
        charset = charset.split(';')
        for item in charset:
            it = item.lower()
            it = it.split('=')
            if 'charset' in it:
                charset = it[1]
                break
    else:
        raise ValueError('incorrect Response')

    return charset


