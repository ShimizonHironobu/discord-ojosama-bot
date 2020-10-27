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
    write_log(message, log_name, logging.INFO)



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
    write_log(message, log_name, logging.DEBUG)



def warning(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み 警告
    write_log(message, log_name, logging.WARNING)



def error(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み エラー
    write_log(message, log_name, logging.ERROR)



def critical(message='', log_name='') :
    """

    write_log wrapper infoログ書き込み

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    ----------

    """

    #ログ書き込み クリティカル
    write_log(message, log_name, logging.CRITICAL)



def write_log(message, log_name, log_type) :
    """

    logger wrapper

    Parameters
    ----------
    message : string ログメッセージ
    log_name : string ログファイル名
    log_type : int ログタイプ loging.INFO loging.DEBUG loging.ERROR loging.WARNING loging.CRITICAL
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
    log_dir = '.storage/logs/'
    file_handler = FileHandler(log_dir+output_file_name + '.log', 'a')

    #ログフォーマット設定
    file_handler.setFormatter(handler_format)
    #ハンドラー設定
    logger.addHandler(file_handler)

    if log_type == logging.INFO :
        logger.info(message)
    elif log_type == logging.DEBUG :
        logger.debug(message)
    elif log_type == logging.ERROR :
        logger.error(message)
    elif log_type == logging.WARNING :
        logger.warning(message)
    elif log_type == logging.CRITICAL :
        logger.critical(message)
