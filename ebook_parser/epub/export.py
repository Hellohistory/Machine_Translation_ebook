# ebook_parser/epub/export.py

import os
from ebooklib import epub

class EPUBExtractor:
    def __init__(self, epub_filename, output_folder):
        self.epub_filename = epub_filename
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def extract_chapters(self):
        # 读取 EPUB 文件
        book = epub.read_epub(self.epub_filename)

        # 提取章节信息并保存为 HTML 文件
        for idx, item in enumerate(book.get_items()):
            if item.get_type() == 9:  # 类型 9 代表章节信息
                content = item.get_content()
                chapter_name = item.get_name().split('/')[-1]
                html_path = os.path.join(self.output_folder, chapter_name)
                with open(html_path, 'wb') as html_file:
                    html_file.write(content)

        print(f"Successfully extracted chapters to {self.output_folder}")

    def extract_css_images(self):
        # 读取 EPUB 文件
        book = epub.read_epub(self.epub_filename)

        # 创建输出文件夹
        css_folder = os.path.join(self.output_folder, 'css')
        images_folder = os.path.join(self.output_folder, 'images')
        os.makedirs(css_folder, exist_ok=True)
        os.makedirs(images_folder, exist_ok=True)

        # 提取 CSS 样式
        for idx, item in enumerate(book.get_items()):
            if item.get_type() == 2:  # 类型 2 代表 CSS 样式
                css_content = item.get_content()
                css_name = item.get_name().split('/')[-1]
                css_path = os.path.join(css_folder, css_name)
                with open(css_path, 'wb') as css_file:
                    css_file.write(css_content)

        # 提取所有图像
        for idx, item in enumerate(book.get_items()):
            if item.get_type() == 1:  # 类型 1 代表图像
                image_content = item.get_content()
                image_name = item.get_name().split('/')[-1]
                image_path = os.path.join(images_folder, image_name)
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_content)

        print(f"Successfully extracted CSS and images to {self.output_folder}")

# 以下代码可用于测试
# extractor = EPUBExtractor(epub_filename='path/to/epub', output_folder='output_folder')
# extractor.extract_chapters()
# extractor.extract_css_images()
