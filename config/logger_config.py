import logging
import os
import shutil
import zipfile
from datetime import datetime

from config.settings import TranslationSettings


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

    # 创建一个归档文件夹用于存放压缩文件
    archive_folder = 'utils/logger/archive'
    os.makedirs(archive_folder, exist_ok=True)

    # 将压缩文件移动到归档文件夹
    if len(subfolders) >= 3:
        oldest_folder = subfolders[0]
        oldest_folder_path = os.path.join(parent_folder, oldest_folder)
        zip_file_path = os.path.join(archive_folder, f'{oldest_folder}.zip')  # 注意这里路径改为归档文件夹

        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(oldest_folder_path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), oldest_folder_path))

        shutil.rmtree(oldest_folder_path)

    # 从 TranslationSettings 类的静态方法中读取最大日志压缩文件数量
    max_log_archives = TranslationSettings.get_max_log_archives()

    # 获取归档文件夹中所有的压缩日志文件
    archive_zip_files = [f for f in os.listdir(archive_folder) if f.endswith('.zip')]
    archive_zip_files.sort()

    # 如果压缩日志文件数量超过最大限制，则删除最旧的
    while len(archive_zip_files) > max_log_archives:
        oldest_zip = archive_zip_files.pop(0)
        os.remove(os.path.join(archive_folder, oldest_zip))

    return logger

