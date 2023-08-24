# config/logger_config.py

import logging

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()  # 调用超类的__init__方法
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def setup_logger():
    logger = logging.getLogger()
    logger.handlers = []  # 清除现有的处理器

    logger.setLevel(logging.DEBUG)  # 设置记录器的默认级别

    # 创建不同级别的处理器
    debug_handler = logging.FileHandler('utils/logger/debug.log', encoding='utf-8') # 调试日志
    info_handler = logging.FileHandler('utils/logger/info.log', encoding='utf-8') # 消息日志
    warning_handler = logging.FileHandler('utils/logger/warning.log', encoding='utf-8') # 警告日志
    error_handler = logging.FileHandler('utils/logger/error.log', encoding='utf-8') # 错误日志

    # 创建级别过滤器
    debug_filter = LevelFilter(logging.DEBUG)
    info_filter = LevelFilter(logging.INFO)
    warning_filter = LevelFilter(logging.WARNING)
    error_filter = LevelFilter(logging.ERROR)

    # 为处理器添加过滤器
    debug_handler.addFilter(debug_filter)
    info_handler.addFilter(info_filter)
    warning_handler.addFilter(warning_filter)
    error_handler.addFilter(error_filter)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 将格式化器应用于处理器
    debug_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    return logger


# 使用配置好的日志记录器
logger = setup_logger()