import os
from input_module.epub import process_epub

def main():
    # 获取用户输入
    epub_filename = "test file/pg71442.epub"
    file_type = os.path.splitext(epub_filename)[1].lstrip('.').lower()

    if file_type != 'epub':
        print("当前只支持 EPUB 文件类型。")
        return

    if not os.path.exists(epub_filename):
        print("指定的 EPUB 文件不存在。")
        return

    source_lang = input("请输入源语言（例如：zh-tw）: ")
    target_lang = "zh-CHS"

    # 选择翻译服务提供商
    print("请选择翻译服务提供商：")
    print("1. zhconv (繁体中文至简体中文)")
    print("2. OpenAI (多语言翻译)")
    print("3. 有道翻译 (多语言翻译)") # 添加新的选项
    provider_choice = input("请输入选项（1/2/3）: ") # 更新输入提示

    # 调用 EPUB 处理函数
    process_epub(epub_filename, source_lang, target_lang, provider_choice)

if __name__ == "__main__":
    main()
