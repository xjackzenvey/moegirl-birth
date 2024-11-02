import sys
import requests
import logging
from bs4 import BeautifulSoup
from config import headers
import re

def remove_html_tags(text):
    # 正则表达式匹配HTML标签
    html_pattern = re.compile(r'<.*?>')
    # 替换标签为空字符串
    return re.sub(html_pattern, '', text)

class Client:
    def __init__(self,url:str) -> None:
        self.url = url
        self.test()
        self.headers = headers
        self.page_content = {}
        
    def test(self):
        try:
            requests.get(self.url)
        except:
            logging.log(level=logging.ERROR,msg="无法连接到服务器，请检查网络连接。")
            sys.exit(-1)
            
    def setHeader(self,key:str,value:str):
        self.headers[key] = value
        
    def get_page(self,url_path:str) -> str:
        try:
            page = requests.get(self.url + url_path).content
        except:
            logging.log(logging.ERROR,msg=f"在获取页面 {url_path} 时发生错误。请检查网络连接。")
            sys.exit(-1)
        
        self.page_content[url_path] = page.decode()
        return page.decode()
    
    def select(self,url_path:str,selector:str) -> list:
        try:
            _page = self.page_content[url_path]
        except:
            _page = self.get_page(self,url_path)
            
        _soup = BeautifulSoup(_page,features='lxml')
        return _soup.select(selector)