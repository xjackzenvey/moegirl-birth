from utils.net import Client,remove_html_tags
from utils.sql import sql_db
from utils.encoder import sitedataEncoder
import json
import logging
import os
import shutil
import requests
from bs4 import BeautifulSoup
from config import sitedata_save_filename,db,db_table  
logging.getLogger().setLevel(logging.INFO)
    

class Character:
    def __init__(self,name:str,birth:str,info_url:str) -> None:
        self.name = name
        self.birth = birth
        self.info_url = info_url
        self.push_to_db(db,db_table)
        logging.log(logging.INFO,msg=f"已检索到角色：{self.name}；生日：{self.birth}")
        
    def __str__(self) -> str:
        return f"name: {self.name}\nbirth: {self.birth}\nnote: {self.note}"

    def get_info(self):
        _content = requests.get("https://moegirl.uk"+self.info_url).content
        _text = BeautifulSoup(_content).select("div.mw-parser-output p")[0].text
        _text = remove_html_tags(_text)
        self.note = _text

    def push_to_db(self,db:sql_db,table:str):
        try:
            db.insert(
                table = table,
                data= {
                    'name' : self.name,
                    'birth' : self.birth,
                    'info_url' : self.info_url
                }
            )
        except:
            logging.log(logging.ERROR,msg="将数据插入数据库时发生错误。 角色名："+self.name)
            return


class Sitedata:
    def __init__(self) -> None:
        self.urls_by_month = {}
        self.characters_by_date = {}
        
    def push_urlsBymonth(self,text:str,url:str):
        self.urls_by_month[text] = url
        #self.save()
        
    def push_chBydate(self,character:Character):
        character_name,date = character.name,character.birth
        if self.characters_by_date.get(date) == None:
            self.characters_by_date[date] = [character_name]
        else:
            self.characters_by_date[date].append(character_name)
            
        self.save()
        
    def save(self):
        with open(sitedata_save_filename,'w',encoding='utf-8') as f:
            json.dump(self,ensure_ascii=False,fp=f,indent=4,cls=sitedataEncoder)


class Application:
    def __init__(self,root_url:str) -> None:
        self.client = Client(url=root_url)
        self.sitedata = Sitedata()
        self.characters = []
        self.setupClient(cookie=None)
    
    def checkenv(self):
        if not os.path.exists('./data/characters.db'):
            logging.log(logging.WARNING,msg="未找到数据库文件 data/character.db，将从characters_init.db创建。")
            shutil.copyfile("data/characters_init.db","data/characters.db")    

    def setupClient(self,cookie:str):
        if cookie != None:
            self.client.setHeader('Cookie',cookie)
            
    def run(self):
        
        self.client.get_page(url_path='/Category:按生日分类')
        for htmlElement in self.client.select(url_path='/Category:按生日分类',selector='div.CategoryTreeItem a'):
            self.sitedata.push_urlsBymonth(
                text = htmlElement.text,
                url = htmlElement['href']
            )
            
        # x month
        for url_path in self.sitedata.urls_by_month.values():
            self.client.get_page(url_path=url_path)
            # x month y day in htmlElement
            for htmlElement in self.client.select(url_path=url_path,selector='div.CategoryTreeItem a'):
                self.client.get_page(url_path=htmlElement['href'])
                for char_item_element in self.client.select(url_path=htmlElement['href'],selector='div.mw-category-group ul li a'):
                    character = Character(
                        name = char_item_element.text,
                        birth = htmlElement.text,
                        info_url = char_item_element['href']
                    )
                    self.sitedata.push_chBydate(character)
            
            
    