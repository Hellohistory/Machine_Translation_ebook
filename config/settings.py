class TranslationSettings:
    AVAILABLE_MODELS = [
        "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-3.5-turbo",
        # 其他可用模型
    ]

    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_PROMPT = "请将下面的文本从{source_lang}翻译为{target_lang}: {sentence}"

    # OpenAI的API密钥
    OPENAI_API_KEY = ""

    # OpenAI的API代理地址
    OPENAI_API_PROXY = "https://api.openai-proxy.com"  # 你可以在此设置代理URL，或者保留为None以便在其他地方进行配置

    @staticmethod
    def get_api_key():
        return TranslationSettings.OPENAI_API_KEY

    @staticmethod
    def get_api_proxy():
        return TranslationSettings.OPENAI_API_PROXY

    @staticmethod
    def get_model_choices():
        return TranslationSettings.AVAILABLE_MODELS

    @staticmethod
    def get_default_model():
        return TranslationSettings.DEFAULT_MODEL

    @staticmethod
    def get_default_prompt():
        return TranslationSettings.DEFAULT_PROMPT
