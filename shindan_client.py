# httpアクセスするためのプログラム

import urllib
from pyquery import PyQuery as pq

def request(url):
    """

    診断メーカーの結果を取得する

    Parameters
    ----------
    url : string 診断メーカーURL
    ----------

    Parameters
    ----------
    string 診断結果
    ----------

    """

    #診断結果のページを取得
    data = urllib.parse.urlencode({'u': 'おじょうさま'}).encode('utf-8')
    request = urllib.request.Request(url, data)
    response = urllib.request.urlopen(request)
    html = response.read()
    
    #取得したページソースの中から診断結果文字列を取得する
    dom = pq(html)
    return dom('div.result2>div').text()
