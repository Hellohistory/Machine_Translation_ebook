import logging
import os
import shutil
import zipfile
from datetime import datetime


class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def setup_logger():
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    # 获取当前时间戳，并创建相应的文件夹
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    folder_path = f'utils/logger/{timestamp}'
    os.makedirs(folder_path, exist_ok=True)

    # 创建日志记录器并设置级别
    logger = logging.getLogger()
    logger.handlers = []
    logger.setLevel(logging.DEBUG)

    # 创建四个不同级别的文件处理器
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    for level in log_levels:
        file_path = os.path.join(folder_path, f'{level.lower()}.log')
        handler = logging.FileHandler(file_path, encoding='utf-8')
        level_filter = LevelFilter(getattr(logging, level))
        handler.addFilter(level_filter)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # 检查母文件夹，如果存在三个或更多的时间戳文件夹，则压缩最旧的一个
    parent_folder = 'utils/logger'
    subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
    subfolders.sort()

    if len(subfolders) >= 3:
        oldest_folder = subfolders[0]
        oldest_folder_path = os.path.join(parent_folder, oldest_folder)
        zip_file_path = os.path.join(parent_folder, f'{oldest_folder}.zip')

        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(oldest_folder_path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), oldest_folder_path))

        shutil.rmtree(oldest_folder_path)

    return logger

