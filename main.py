# main.py

import os
from input_module.epub import process_epub

from input_module.other import process_srt

def main():
    # 获取用户输入
    epub_filename = r"test file/pg53535.epub"
    file_type = os.path.splitext(epub_filename)[1].lstrip('.').lower()

    supported_file_types = ['epub', 'srt']
    if file_type not in supported_file_types:
        print(f"当前只支持 {', '.join(supported_file_types).upper()} 文件类型。")
        return

    if not os.path.exists(epub_filename):
        print("指定的文件不存在。")
        return

    source_lang = "英文"
    target_lang = "简体中文"

    # 选择翻译服务提供商
    print("请选择翻译服务提供商：")
    print("1. zhconv (繁体中文至简体中文)")
    print("2. OpenAI (多语言翻译)")
    print("3. 有道翻译 (多语言翻译)")
    provider_choice = input("请输入选项（1/2/3）: ")

    if file_type == 'epub':
        process_epub(epub_filename, source_lang, target_lang, provider_choice)
    elif file_type == 'srt':
        process_srt(epub_filename, source_lang, target_lang, provider_choice)

if __name__ == "__main__":
    main()
