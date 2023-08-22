class TranslationSettings:
    # OpenAI的设置配置
    AVAILABLE_MODELS = [
        "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-3.5-turbo","gpt-3.5-turbo-16k","gpt-3.5-turbo-0613","gpt-3.5-turbo-16k-0613"
        # 其他可用模型
    ]

    MAX_TOKENS_FOR_MODELS = {
        "gpt-4": 8192,
        "gpt-4-0613": 8192,
        "gpt-4-32k": 32768,
        "gpt-4-32k-0613": 32768,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
        "gpt-3.5-turbo-0613": 4096,
        "gpt-3.5-turbo-16k-0613": 16384
    }

    DEFAULT_MODEL = "gpt-3.5-turbo-0613"
    DEFAULT_PROMPT = "请将下面的文本从{source_lang}翻译为{target_lang}: {sentence}"

    # OpenAI的API密钥
    OPENAI_API_KEY = ""

    # Openai的API一分钟内最大处理次数的设置
    MAX_REQUESTS_PER_MINUTE = 50

    # OpenAI的API代理地址
    OPENAI_API_PROXY = "https://api.openai-proxy.com"  # 你可以在此设置代理URL，或者保留为None以便在其他地方进行配置

    # 关于OpenAI的设置
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

    @staticmethod
    def get_max_tokens_for_model(model_name):
        return TranslationSettings.MAX_TOKENS_FOR_MODELS.get(model_name, None)

    @staticmethod
    def get_max_requests_per_minute():
        return TranslationSettings.MAX_REQUESTS_PER_MINUTE
