from utils.sql import sql_db

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'Referer' : 'https://moegirl.uk/load.php?lang=zh-cn'
}

sitedata_save_filename = 'data/sitedata.json'

db = sql_db(database_path='data/characters.db')
db_table = 'characters'