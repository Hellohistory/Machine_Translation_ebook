# input_module/epub.py
from ebook_parser.epub.epub_creator import EPUBCreator
from ebook_parser.epub.epub_translation_writer import EPUBTranslationWriter
from ebook_parser.epub.epub_translator import EPUBTextTranslator
from ebook_parser.epub.export import EPUBExtractor
from ebook_parser.epub.extract import TextExtractor
from translation_module.translation_service_selector import select_translation_service

def process_epub(epub_filename, source_lang, target_lang, provider_choice):
    # 定义文件路径
    output_folder = 'Temporary Files\output_folder'
    translated_html_folder = r'Temporary Files\translated_html_folder'
    json_input_path = 'Temporary Files\extracted_text.json'
    json_output_path = r'Temporary Files\translated_text.json'
    new_epub_path = 'new_translated_book.epub'

    # 选择翻译服务
    translator_service, max_tokens_for_model = select_translation_service(provider_choice)
    if translator_service is None:
        return

    epub_translator = EPUBTextTranslator(
        json_input_path=json_input_path,
        json_output_path=json_output_path,
        translator=translator_service,
        max_tokens_for_model=max_tokens_for_model  # 在 EPUBTextTranslator 初始化时传递 max_tokens_for_model
    )

    # 执行 EPUB 解析、提取、翻译和创建流程
    extractor = EPUBExtractor(epub_filename, output_folder)
    extractor.extract_chapters()
    extractor.extract_css_images()

    text_extractor = TextExtractor(html_folder=output_folder, json_output_path=json_input_path)
    text_extractor.extract_text_with_links_and_tags()

    epub_translator.translate_text(source_lang, target_lang)

    epub_writer = EPUBTranslationWriter(
        json_input_path=json_output_path,
        html_folder=output_folder
    )
    epub_writer.write_translated_text_to_html()

    epub_creator = EPUBCreator(
        epub_filename=epub_filename,
        translated_html_folder=translated_html_folder,
        new_epub_path=new_epub_path
    )
    epub_creator.create_new_epub()

    print("翻译完成！新的 EPUB 文件已创建。")
