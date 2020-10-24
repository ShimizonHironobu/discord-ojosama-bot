import datetime
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter


def info(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み インフォ
    write_log(message, log_name, 'INFO')



def debug(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み デバッグ
    write_log(message, log_name, 'DEBUG')



def warning(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み エラーログ
    write_log(message, log_name, 'WARNING')



def error(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み エラーログ
    write_log(message, log_name, 'ERROR')



def critical(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み エラーログ
    write_log(message, log_name, 'CRITICAL')



def write_log(message, log_name, log_type) :
    """

    logger wrapper

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    log_type : string ログタイプ 'INFO' 'DEBUG' 'ERROR'
    ----------

    """

    logger = getLogger()
    logger.setLevel(logging.DEBUG)
    #フォーマット
    handler_format = Formatter('%(asctime)s[%(levelname)s] - %(message)s')

    #現在の日付を取得
    now_date = datetime.date.today().strftime('%Y-%m-%d')

    #出力先ファイル名を指定 logname-日付
    output_file_name = log_name+'-'+now_date if log_name != '' else now_date
    log_dir = './log/'
    file_handler = FileHandler(log_dir+output_file_name + '.log', 'a')

    #ログフォーマット設定
    file_handler.setFormatter(handler_format)
    #ハンドラー設定
    logger.addHandler(file_handler)

    if log_type == 'INFO' :
        logger.info(message)
    elif log_type == 'DEBUG' :
        logger.debug(message)
    elif log_type == 'ERROR' :
        logger.error(message)
    elif log_type == 'WARNING' :
        logger.warning(message)
    elif log_type == 'CRITICAL' :
        logger.critical(message)
