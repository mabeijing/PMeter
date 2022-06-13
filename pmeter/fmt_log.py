import logging
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler as FileHandler

from pmeter import __BASE_DIR__

fmt = f'%(asctime)s - %(levelname)s - %(name)s - ThreadId:%(thread)d - %(filename)s:%(funcName)s:%(lineno)d - %(message)s'
log_file: str = __BASE_DIR__.joinpath('logs', 'pymeter_run.log')
when = 'D'
backCount: int = 3


def format_logger(log_name: str = None) -> logging.Logger:
    logger = logging.getLogger(log_name)
    logger.setLevel(level=logging.DEBUG)
    formatter: Formatter = Formatter(fmt)

    stream_handler: StreamHandler = StreamHandler()  # 往屏幕上输出
    stream_handler.setLevel(level=logging.DEBUG)
    stream_handler.setFormatter(formatter)  # 设置屏幕上显⽰的格式
    logger.addHandler(stream_handler)  # 把对象加到logger⾥

    file_handler: FileHandler = FileHandler(filename=log_file, when=when, backupCount=backCount, encoding='utf-8')
    file_handler.setLevel(level=logging.DEBUG)
    file_handler.setFormatter(formatter)  # 设置⽂件⾥写⼊的格式
    logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    log = format_logger(__name__)
    log.info('info')
    log.error('error')
    log.critical('critical')
