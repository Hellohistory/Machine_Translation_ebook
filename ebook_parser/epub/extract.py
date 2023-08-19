# ebook_parser/epub/extract.py

from bs4 import BeautifulSoup
import json
import os

class TextExtractor:
    def __init__(self, html_folder, json_output_path):
        self.html_folder = html_folder
        self.json_output_path = json_output_path

    def extract_text_with_links_and_tags(self):
        text_data = []

        # 遍历章节的 HTML 文件
        for html_file in os.listdir(self.html_folder):
            if html_file.endswith('.html') or html_file.endswith('.xhtml'):
                file_path = os.path.join(self.html_folder, html_file)

                # 解析 HTML 文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')

                    # 提取正文段落
                    paragraphs = soup.find_all('p')
                    for idx, p in enumerate(paragraphs):
                        # 创建标签
                        tag = f"{html_file}_p{idx}"
                        # 获取段落的 HTML 内容，保留链接
                        html_content = str(p)
                        text_data.append({
                            'tag': tag,
                            'html_content': html_content
                        })

        # 将提取的文本和标签保存到 JSON 文件中
        with open(self.json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(text_data, json_file, ensure_ascii=False, indent=4)

        print(f"已将带有链接的文本提取并保存到 {self.json_output_path}")

# 以下代码可用于测试
# extractor = TextExtractor(html_folder='output_folder', json_output_path='extracted_text.json')
# extractor.extract_text_with_links_and_tags()
