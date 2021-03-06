import logging
import markovify
import MeCab
import re
import os

from lib import (
    log,
    config
)

MARCOV_DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/..'+config.get('app.storage.path')+'data/markov/'
MARCOV_RAW_DATA_NAME = 'message_data_raw.txt'
MARCOV_MODEL_DATA_NAME = 'message_data_model.json'

# logger = logging.getLogger(__name__)
# fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
# logging.basicConfig(level=logging.DEBUG, format=fmt)

# Toggle test_sentence_input
test_sentence_input = markovify.Text.test_sentence_input  # Stash
def disable_test_sentence_input():
    def do_nothing(self, sentence):
        return True
    markovify.Text.test_sentence_input = do_nothing
def enable_test_sentence_input():
    markovify.Text.test_sentence_input = test_sentence_input

def format_text(t):
    t = t.replace('　', ' ')  # Full width spaces
    t = re.sub(r'([。．！？…]+)', r'\1\n', t)  # \n after ！？
    t = re.sub(r'(.+。) (.+。)', r'\1 \2\n', t)
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'([。．！？…])\n」', r'\1」 \n', t)  # \n before 」
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'\n+', r'\n', t).rstrip('\n')  # Empty lines
    t = re.sub(r'\n +', '\n', t)  # Spaces
    return t

def parse_text(filepath):
    f = open(filepath, 'r')
    raw_data = f.read()
    f.close()

    parsed_text = ''
    for line in raw_data.split("\n"):
        parsed_text = parsed_text + MeCab.Tagger('-Owakati').parse(line)

    with open(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME, 'a') as f:
        print(parsed_text, file=f)
    f.close()
    return parsed_text

def build_model(text, format=True, state_size=2):
    """
    format=True: Fast.
    format=False: Slow. Funnier(?)
    """
    if format is True:
        # logger.info('Format: True')
        return markovify.NewlineText(format_text(text), state_size)
    else:
        # logger.info('Format: False')
        disable_test_sentence_input()
        text = markovify.Text(text, state_size)
        enable_test_sentence_input()
        return text

def make_sentences(text, start=None, max=300, min=1, tries=100):
    if start is (None or ''):   # If start is not specified
        for _ in range(tries):
            sentence = str(text.make_sentence()).replace(' ', '')
            if sentence and len(sentence) <= max and len(sentence) >= min:
                return sentence
    else:  # If start is specified
        for _ in range(tries):
            sentence = str(text.make_sentence_with_start(beginning=start)).replace(' ', '')
            if sentence and len(sentence) <= max and len(sentence) >= min:
                return sentence


def raw_data_parse() :
    #保存用ディレクトリがない場合は作成
    if not os.path.isdir(MARCOV_DATA_DIR) :
            os.makedirs(MARCOV_DATA_DIR)
    if not os.path.exists(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME) :
        return False
    if not os.path.getsize(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME) :
        return False

    # 連鎖で扱えるようpurseする この操作が重い
    parsed_text = parse_text(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME)

    format = True
    text_model = build_model(parsed_text, format=format, state_size=3)
    json = text_model.to_json()
    #モデルをバックアップする
    with open(MARCOV_DATA_DIR + MARCOV_MODEL_DATA_NAME, 'w') as f:
        print(json, file=f)
    f.close()

    return True


def make_markov_sentence(max_chars=20, min_chars=5,  state_size=3):

    #データの入ったディレクトリがなければ空文字を返す
    if not os.path.isdir(MARCOV_DATA_DIR) :
        return ''
    if not os.path.exists(MARCOV_DATA_DIR + MARCOV_MODEL_DATA_NAME) :
        return ''
    if not os.path.getsize(MARCOV_DATA_DIR + MARCOV_MODEL_DATA_NAME) :
        return ''

    # データを読み込み
    f = open(MARCOV_DATA_DIR + MARCOV_MODEL_DATA_NAME, "r")
    json = f.read()
    f.close()
    text_model = markovify.Text.from_json(json)

    
    # json = text_model.to_json()
    #モデルをバックアップする

    # open(MARCOV_DATA_DIR + 'markov_model.json', 'w').write(json)

    sentence = None
    #連鎖による文字列を生成
    sentence = make_sentences(text_model, start='', max=max_chars, min=min_chars)

    if sentence is None :
        sentence = "何も思いつきませんでしたわ！"

    return sentence 



def add_raw_message_data(message_text):
    #コードブロックのあるメッセージは飛ばす
    if '`' in message_text :
        return

    #メッセージの中からURLを排除
    message_text = re.sub(r"http(.+?)\s", '', message_text, flags=re.MULTILINE)
    
    #メッセージからメンションを排除
    message_text = re.sub(r"@(.+?)\s", '', message_text, flags=re.MULTILINE)

    #顔文字が入っている場合は飛ばす
    if ':' in message_text :
        return

    #保存用ディレクトリがない場合は作成
    if not os.path.isdir(MARCOV_DATA_DIR) :
            os.makedirs(MARCOV_DATA_DIR)

    with open(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME, 'a') as f:
        print(message_text, file=f)
    f.close()
