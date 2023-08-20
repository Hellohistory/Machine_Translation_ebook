import hashlib
import time
import uuid

import requests

from translation_module.translation_interface import TranslationInterface


class YoudaoTranslator(TranslationInterface):
    APP_KEY = ''
    APP_SECRET = ''

    def add_auth_params(self, data, text):
        salt = str(uuid.uuid1())
        curtime = str(int(time.time()))
        signStr = self.APP_KEY + self.truncate(text) + salt + curtime + self.APP_SECRET
        sign = hashlib.sha256(signStr.encode('utf-8')).hexdigest()

        data['appKey'] = self.APP_KEY
        data['salt'] = salt
        data['sign'] = sign
        data['signType'] = 'v3'
        data['curtime'] = curtime

    def translate(self, text, source_lang, target_lang):
        lang_from = source_lang
        lang_to = target_lang

        data = {'q': text, 'from': lang_from, 'to': lang_to}
        self.add_auth_params(data, text)  # 确保添加了所有必需的身份验证参数

        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post('https://openapi.youdao.com/api', data, headers=header)

        response_json = response.json()
        error_code = response_json.get('errorCode')
        if error_code != "0":
            print(f"有道翻译API错误: {error_code}")
            return ""

        translated_text = response_json.get('translation', [])[0]
        return translated_text

    def truncate(self, q):
        # 用于生成签名的截断逻辑
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
