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
    file = open(filepath, 'r').read()

    parsed_text = ''
    for line in file.split("\n"):
        parsed_text = parsed_text + MeCab.Tagger('-Owakati').parse(line)
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


def make_markov_sentence():

    format = True
    max_chars = 50
    min_chars = 5

    #データの入ったディレクトリがなければ空文字を返す
    if not os.path.isdir(MARCOV_DATA_DIR) :
        return ''
    if not os.path.exists(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME) :
        return ''
    if not os.path.getsize(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME) :
        return ''

    # 連鎖で扱えるようpurseする
    parsed_text = parse_text(MARCOV_DATA_DIR + MARCOV_RAW_DATA_NAME)

    text_model = build_model(parsed_text, format=format, state_size=3)
    json = text_model.to_json()
    #モデルをバックアップする
    open(MARCOV_DATA_DIR + 'markov_model.json', 'w').write(json)

    sentence = None
    while True : 
        #連鎖による文字列を生成
        sentence = make_sentences(text_model, start='', max=max_chars, min=min_chars)
        if not sentence is None : 
            break

    return sentence 



