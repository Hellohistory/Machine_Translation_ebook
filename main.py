# main.py

import os
from input_module.epub import process_epub


def main():
    # 获取用户输入
    epub_filename = input("请输入 EPUB 文件的路径: ")
    file_type = os.path.splitext(epub_filename)[1].lstrip('.').lower()

    if file_type != 'epub':
        print("当前只支持 EPUB 文件类型。")
        return

    if not os.path.exists(epub_filename):
        print("指定的 EPUB 文件不存在。")
        return

    source_lang = input("请输入源语言（例如：zh-tw）: ")
    target_lang = input("请输入目标语言（例如：zh-cn）: ")

    # 选择翻译服务提供商
    print("请选择翻译服务提供商：")
    print("1. zhconv (繁体中文至简体中文)")
    print("2. OpenAI (多语言翻译)")
    provider_choice = input("请输入选项（1/2）: ")

    # 调用 EPUB 处理函数
    process_epub(epub_filename, source_lang, target_lang, provider_choice)

    # 调用 EPUB 处理函数
    process_epub(epub_filename, source_lang, target_lang, provider_choice)


if __name__ == "__main__":
    main()
