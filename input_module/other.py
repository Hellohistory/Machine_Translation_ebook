from ebook_parser.captions.srt import SRTTranslator
from translation_module.translation_service_selector import select_translation_service


def process_srt(srt_file_path, source_lang, target_lang, provider_choice):
    # 选择翻译服务
    translator_service, max_tokens_for_model = select_translation_service(provider_choice)
    if translator_service is None:
        return

    # 创建 SRT 翻译器对象
    translator = SRTTranslator(
        srt_file_path=srt_file_path,
        translator=translator_service,
        max_tokens_for_model=max_tokens_for_model
    )

    # 执行翻译
    translator.translate_srt(source_lang, target_lang)

    print("SRT 文件已翻译！新的 SRT 文件已创建。")
