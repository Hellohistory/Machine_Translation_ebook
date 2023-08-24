# ebook_parser/epub/extract.py

import json
import os
from bs4 import BeautifulSoup

from config.logger_config import setup_logger

logger = setup_logger()

class TextExtractor:
    def __init__(self, html_folder, json_output_path):
        self.html_folder = html_folder
        self.json_output_path = json_output_path

    def extract_text_with_links_and_tags(self):
        text_data = []
        global_idx = 0  # 全局计数器，确保每个 text_tag 的值都是唯一的

        # 遍历章节的 HTML 文件
        for html_file in os.listdir(self.html_folder):
            file_idx = 0  # 单独维护每个文件的索引计数器
            if html_file.endswith('.html') or html_file.endswith('.xhtml'):
                file_path = os.path.join(self.html_folder, html_file)

                # 解析 HTML 文件
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        soup = BeautifulSoup(file, 'html.parser')

                        # 提取正文段落
                        paragraphs = soup.find_all('p')
                        for p in paragraphs:
                            # 创建标签
                            tag = f"{html_file}_p{file_idx}"
                            text_tag = f"<tag{global_idx}>"  # 使用全局计数器创建 text_tag 字段
                            # 获取段落的 HTML 内容，保留链接
                            html_content = str(p)
                            text_data.append({
                                'tag': tag,
                                'text_tag': text_tag,  # 新增的 text_tag 字段
                                'html_content': html_content
                            })
                            file_idx += 1  # 更新文件的索引计数器
                            global_idx += 1  # 更新全局计数器
                except Exception as e:
                    logger.error(f"处理文件 {file_path} 时发生错误: {e}")

        # 将提取的文本和标签保存到 JSON 文件中
        try:
            with open(self.json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(text_data, json_file, ensure_ascii=False, indent=4)
            logger.info(f"已将带有链接和文本标签的文本提取并保存到 {self.json_output_path}")
        except Exception as e:
            logger.error(f"保存JSON文件 {self.json_output_path} 时发生错误: {e}")


# 以下代码可用于测试
# extractor = TextExtractor(html_folder='output_folder', json_output_path='extracted_text.json')
# extractor.extract_text_with_links_and_tags()
