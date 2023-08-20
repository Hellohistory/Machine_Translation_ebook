# ebook_parser/epub/epub_translation_writer.py

import json
import os
from bs4 import BeautifulSoup

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
            filename, p_index_tag = tag.rsplit("_p", 1)
            p_index = int(p_index_tag)  # 将字符串转换为整数
            file_path = os.path.join(self.html_folder, filename)

            if file_path not in updated_files:  # 仅在首次访问文件时解析 HTML
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    updated_files[file_path] = soup

            soup = updated_files[file_path]
            original_paragraph = soup.find_all('p')[p_index]
            new_paragraph = BeautifulSoup(html_content, 'html.parser').p
            original_paragraph.replace_with(new_paragraph)


            original_paragraph = soup.find_all('p')[p_index]
            new_paragraph = BeautifulSoup(html_content, 'html.parser').p
            original_paragraph.replace_with(new_paragraph)

        for file_path, soup in updated_files.items():  # 将更新后的 HTML 内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

        print(f"已将翻译后的文本写回 HTML 文件，保存在 {self.html_folder}")

# 以下代码可用于测试
# writer = EPUBTranslationWriter(json_input_path='translated_text.json', html_folder='output_folder')
# writer.write_translated_text_to_html()
