import urllib
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lib import (
    log,
    config
)

from pyquery import PyQuery as pq

#診断メーカーのベースURL
SHINDAN_MAKER_BASE_URL = 'https://shindanmaker.com/'
SHINDAN_LIST_DIR_PATH = os.path.dirname(os.path.abspath(__file__))+'/..'+config.get('app.storage.path')+'data/shidan/'
SHINDAN_LIST_FILE_NAME = 'id_list.json'

def request(id, name='おじょうさま'):
    '''

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

    '''

    #診断結果のページを取得 
    # data postするパラメータ
    data = urllib.parse.urlencode({'u': name}).encode('utf-8')
    request = urllib.request.Request(SHINDAN_MAKER_BASE_URL + id, data)
    response = urllib.request.urlopen(request)
    html = response.read()
    response.close()
    
    #取得したページソースの中から診断結果文字列を取得する
    dom = pq(html)
    return dom('div.result2>div').text()




def add(url):
    """

    診断メーカーを診断のリストリストに追加する

    Parameters
    ----------
    url : string 診断メーカーのurl
    ----------

    Parameters
    ----------
    int 0:登録失敗 1:登録成功 2:登録済
    ----------

    """

    try:
        # 診断名を取得する
        # URLが有効なものであるかもここで確認
        shindan_name = ''
        f = urllib.request.urlopen(url)
        html = f.read()
        f.close()

        dom = pq(html)
        shindan_name = dom('div.shindantitle2>h1>a').text()

        # 診断名を取得出来ない場合はそれはエラーである
        if shindan_name == '' :
            raise Exception('shindan_client.add : shindanmaker url is invalid.')

        # 診断IDを取得
        shindan_id = url.replace(SHINDAN_MAKER_BASE_URL, '')

        # 診断リストpath生成
        shindan_file_path = SHINDAN_LIST_DIR_PATH + SHINDAN_LIST_FILE_NAME

        # 保存する診断のデータ
        add_shindan_data = {'id' : shindan_id, 'name' : shindan_name}

        #診断リストディレクトリがなければ作成
        if not os.path.isdir(SHINDAN_LIST_DIR_PATH) :
            os.makedirs(SHINDAN_LIST_DIR_PATH)

        # 診断リストファイルがなければ作成
        if not os.path.exists(shindan_file_path) :
            with open(shindan_file_path, "a") as create_file:
                create_file.write(json.dumps({'data' : [add_shindan_data]}))
            create_file.close()
        else:

            write_shindan_data = {'data' : []}
            # ファイルの空チェック　空であればファイル内のデータチェックは飛ばす
            if os.path.getsize(shindan_file_path) :
                #診断リストに既に同じ診断がないかチェックを行うために読み込む
                read_file = open(shindan_file_path, "r")
                id_list_json = json.load(read_file)
                read_file.close()
                id_list_data = id_list_json['data']

                for file_shindan_data in id_list_data:
                    write_shindan_data['data'].append({'id' : file_shindan_data['id'], 'name' : file_shindan_data['name']})
                    if file_shindan_data['id'] == shindan_id :
                        return 2

            # 新しく追加する診断のデータを追加
            write_shindan_data['data'].append(add_shindan_data)

            # 診断リストの保存
            with open(shindan_file_path, 'w') as edit_file:
                edit_file.write(json.dumps(write_shindan_data))     
            edit_file.close()

    except Exception as e:
        log.warning(e)
        return 0

    return 1
    



def get_list():
    """

    登録されている診断メーカーのリストを表示

    Parameters
    ----------
    ----------

    Parameters
    ----------
    list 
    ----------

    """

    # 診断リストのファイルパス
    shindan_file_path = SHINDAN_LIST_DIR_PATH + SHINDAN_LIST_FILE_NAME

    #診断リストディレクトリがなければ空リストを返す
    if not os.path.isdir(SHINDAN_LIST_DIR_PATH) :
        return []

    # 診断リストファイルがなければ作成
    if not os.path.exists(shindan_file_path) :
       return []

    if not os.path.getsize(shindan_file_path) :
        return []

    #診断リストに既に同じ診断がないかチェックを行うために読み込む
    read_file = open(shindan_file_path, "r")
    id_list_json = json.load(read_file)
    read_file.close()
    return id_list_json['data']


'''
デフォルトの追加リスト
'''
# add('https://shindanmaker.com/950470');
# add('https://shindanmaker.com/950505');
# add('https://shindanmaker.com/950183');
# add('https://shindanmaker.com/949656');
# add('https://shindanmaker.com/949909');
# add('https://shindanmaker.com/950139');
# add('https://shindanmaker.com/950227');
