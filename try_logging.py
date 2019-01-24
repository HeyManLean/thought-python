#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import logging.config  # 这样也导入了 logging


def test_simple_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        # filename='app.log',
        # filemode='w',
        datefmt='%b %d-%Y %H:%M:%S',
        format=(
            '%(levelname)8s %(asctime)s '
            '%(filename)s/%(lineno)d - %(message)s'
        )
    )

    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

    try:
        d = 1 / 0
    except:
        logging.error('Oops! Something went wrong!', exc_info=True)
        logging.exception('Oops! Something went wrong!')


def test_complex_logging():
    # --- 初始化formatter ---
    c_formatter = logging.Formatter(
        fmt='%(name)s - %(levelname)s - %(message)s',
        datefmt='%b %d-%Y')
    f_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # --- 初始化handler ---
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(
        filename='app.log',
        mode='a',
        encoding='utf-8'
    )
    # 设置level
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)
    # 设置formatter
    c_handler.setFormatter(c_formatter)
    f_handler.setFormatter(f_formatter)

    # --- 初始化logger ---
    logger = logging.getLogger(__name__)
    # 设置handler
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.warning('This is a warning!')
    logger.error('This is an error!')


def test_configdict_logging():
    LOGGING_CONF = {
        'version': 1,  # 版本必须为1
        'disable_existing_loggers': False,  # True 重新配置会使之前 logger 无效
        # formatter
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        # handler
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'info_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',  # 自动切割
                'level': 'INFO',
                'formatter': 'simple',
                'filename': 'info.log',
                'maxBytes': 10485760,
                'backupCount': 20,
                'encoding': 'utf8'
            },
            'error_file_handler': {
                'class': 'logging.FileHandler',
                'level': 'ERROR',
                'formatter': 'simple',
                'filename': 'error.log'
            }
        },
        # logger
        'loggers': {
            'test': {
                'level': 'DEBUG',
                'handlers': ['default', 'info_file_handler'],
                'propagate': False
            },
            'error': {
                'level': 'ERROR',
                'handlers': ['error_file_handler'],
                'propagate': False
            }
        }

    }
    logging.config.dictConfig(LOGGING_CONF)

    # test
    test_logger = logging.getLogger('test')
    
    test_logger.debug('This is a debug message')
    test_logger.info('This is an info message')
    test_logger.warning('This is a warning message')
    test_logger.error('This is an error message')
    test_logger.critical('This is a critical message')

    # error
    error_logger = logging.getLogger('error')

    error_logger.debug('This is a debug message')
    error_logger.info('This is an info message')
    error_logger.warning('This is a warning message')
    error_logger.error('This is an error message')
    error_logger.critical('This is a critical message')

if __name__ == '__main__':
    # test_simple_logging()
    # test_complex_logging()
    test_configdict_logging()
