# ebook_parser/epub/epub_creator.py
import logging
import os
from ebooklib import epub
from lxml import etree

# 配置日志
logger = logging.getLogger()

class EPUBCreator:
    def __init__(self, epub_filename, translated_html_folder, new_epub_path):
        self.epub_filename = epub_filename
        self.translated_html_folder = translated_html_folder
        self.new_epub_path = new_epub_path

    def create_new_epub(self):
        logger.info(f"开始创建新的 EPUB 文件: {self.new_epub_path}")

        # 读取原始 EPUB 文件
        book = epub.read_epub(self.epub_filename)

        # 遍历原始章节，并用翻译后的 HTML 替换内容
        for item in book.get_items():
            if item.get_type() == 9:  # 类型 9 代表章节信息
                chapter_name = item.get_name().split('/')[-1]
                translated_html_path = os.path.join(self.translated_html_folder, chapter_name)
                if os.path.exists(translated_html_path):  # 确保翻译后的文件存在
                    with open(translated_html_path, 'r', encoding='utf-8') as html_file:
                        translated_html_content = html_file.read()

                    # 解析并重新序列化 HTML
                    parser = etree.XMLParser(recover=True)
                    html_tree = etree.fromstring(translated_html_content.encode('utf-8'), parser=parser)
                    translated_html_content_fixed = etree.tostring(html_tree, encoding='utf-8').decode('utf-8')

                    # 替换章节内容
                    item.set_content(translated_html_content_fixed)
                    logger.info(f"替换章节 {chapter_name} 的内容")

        # 写入新的 EPUB 文件
        epub.write_epub(self.new_epub_path, book)

        logger.info(f"新 EPUB 文件已创建在 {self.new_epub_path}")

# 以下代码可用于测试
# creator = EPUBCreator(epub_filename='path/to/epub',
#                       translated_html_folder='output_folder',
#                       new_epub_path='new_translated_book.epub')
# creator.create_new_epub()
