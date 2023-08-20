import requests
from bs4 import BeautifulSoup


def get_google_homepage():
    url = "https://www.google.com"

    try:
        # 发送GET请求
        response = requests.get(url)

        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, "html.parser")

            # 输出整个HTML内容
            print(soup.prettify())

        else:
            print("请求失败，状态码：", response.status_code)

    except requests.exceptions.RequestException as e:
        print("请求发生异常：", e)


if __name__ == "__main__":
    get_google_homepage()
