# ebook_parser/epub/epub_translation_writer.py

import json
import logging
import os
from bs4 import BeautifulSoup

# 配置日志
logger = logging.getLogger()

class EPUBTranslationWriter:
    def __init__(self, json_input_path, html_folder):
        self.json_input_path = json_input_path
        self.html_folder = html_folder

    def write_translated_text_to_html(self):
        with open(self.json_input_path, 'r', encoding='utf-8') as json_file:
            translated_data = json.load(json_file)

        updated_files = {}  # 用于跟踪已更新的 HTML 文件

        for item in translated_data:
            tag = item['tag']
            html_content = item['html_content']

            # 使用 BeautifulSoup 解析 HTML 内容
            translated_soup = BeautifulSoup(html_content, 'html.parser')

            # 遍历所有的特殊标签并删除它们
            for special_tag in translated_soup.find_all(lambda x: x.name.startswith('tag')):
                special_tag.decompose()
            filename, p_index_tag = tag.rsplit("_p", 1)
            p_index = int(p_index_tag)  # 将字符串转换为整数
            file_path = os.path.join(self.html_folder, filename)

            if file_path not in updated_files:  # 仅在首次访问文件时解析 HTML
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    updated_files[file_path] = soup

            soup = updated_files[file_path]
            paragraphs = soup.find_all('p')
            if p_index < len(paragraphs):
                original_paragraph = paragraphs[p_index]
                new_paragraph = BeautifulSoup(html_content, 'html.parser').p
                original_paragraph.replace_with(new_paragraph)
            else:
                logger.warning(f"索引 {p_index} 超出范围，文件 {file_path} 只有 {len(paragraphs)} 个段落。")

        for file_path, soup in updated_files.items():
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            logger.info(f"已更新文件：{file_path}")

        logger.info(f"已将翻译后的文本写回 HTML 文件，保存在 {self.html_folder}")


# 以下代码可用于测试
# writer = EPUBTranslationWriter(json_input_path=r'D:\Code Work\GithubProject\Machine_Translation_ebook\Temporary Files\translated_text.json',
#                                html_folder='D:\Code Work\GithubProject\Machine_Translation_ebook\Temporary Files\output_folder')
# writer.write_translated_text_to_html()
