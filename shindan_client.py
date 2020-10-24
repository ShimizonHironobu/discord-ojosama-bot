import urllib
from pyquery import PyQuery as pq

def request(id, name='おじょうさま'):
    """

    診断メーカーの結果を取得する

    Parameters
    ----------
    id : string 診断メーカーのid
    name : string 診断したい名前
    ----------

    Parameters
    ----------
    string 診断結果
    ----------

    """

    #診断結果のページを取得 
    # data postするパラメータ
    data = urllib.parse.urlencode({'u': name}).encode('utf-8')
    request = urllib.request.Request('https://shindanmaker.com/' + id, data)
    response = urllib.request.urlopen(request)
    html = response.read()
    
    #取得したページソースの中から診断結果文字列を取得する
    dom = pq(html)
    return dom('div.result2>div').text()
