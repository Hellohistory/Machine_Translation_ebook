import logging

def setup_logger():
    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 设置记录器的默认级别

    # 创建不同级别的处理器
    debug_handler = logging.FileHandler('utils/logger/debug.log') # 调试日志
    info_handler = logging.FileHandler('utils/logger/info.log') # 消息日志
    warning_handler = logging.FileHandler('utils/logger/warning.log') # 警告日志
    error_handler = logging.FileHandler('utils/logger/error.log') # 错误日志

    # 设置不同级别的处理器级别
    debug_handler.setLevel(logging.DEBUG)
    info_handler.setLevel(logging.INFO)
    warning_handler.setLevel(logging.WARNING)
    error_handler.setLevel(logging.ERROR)

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

    # 返回配置好的日志记录器
    return logger

# 使用配置好的日志记录器
logger = setup_logger()

