import sqlite3
from colorama import init,Fore
from requests import delete
init(autoreset=True)

'''
*类: sql_db
*功能: 用于操作数据库文件
*构造函数需要: SQLite文件路径
'''

class sql_db:
    def __init__(self,database_path):
        try:
            self.conn=sqlite3.connect(database_path,check_same_thread=False)
        except Exception as e:
            print(Fore.RED+"Connect to database Error:"+str(e))
    
    '''
    *函数: sql_db.count
    *功能: 计算数据库中符合条件的元素个数
    *若出现错误返回-1
    '''

    def count(self,table:str,condition:str='')->int:
        if not condition=='':
            condition="WHERE "+condition
        try:
            cursor=self.conn.cursor()
            sql_sentense="SELECT count(*) FROM "+table+" "+condition
            result=cursor.execute(sql_sentense)
            return int(result.fetchone()[0])
        except Exception as e:
            print(Fore.RED+"query count error:"+sql_sentense+'\ntrace:'+str(e))
            return -1
    
    '''
    *函数: sql_db.select
    *功能: 从数据库中选取相应元素
    *找不到或出错都会返回空列表
    '''    
    def select(self,table:str,element:str,condition:str=None)->list:
        try:
            if not condition==None:
                condition='WHERE '+condition
            else:
                condition=""
            cursor=self.conn.cursor()

            if element == "*":
                sql_sentense = f"select * from {table} {condition}"
                try:
                    result = cursor.execute(sql_sentense)
                    _rt_res = []
                    for row in result:
                        _rt_res.append(row)
                    return _rt_res
                except Exception as e:
                    print((Fore.RED+"SQL SELECT ERROR:%s\ntrace:%s")%(sql_sentense,str(e)))
                    return []                    
            else:    
                sql_sentense=("SELECT %s FROM %s %s")%(element,table,condition)
                try:
                    result=cursor.execute(sql_sentense)
                    res=[]
                        
                    for row in result:
                        res.append(row[0])
                    return res
                except Exception as e:
                    print((Fore.RED+"SQL SELECT ERROR:%s\ntrace:%s")%(sql_sentense,str(e)))
                    return []
                
        except Exception as e:
            print(Fore.LIGHTYELLOW_EX+"SQL SELECT unknown error:"+str(e))
            return []
        
    '''
    *函数: sql_db.insert
    *功能: 将数据插入数据库中
    *参数: 字典型,即字段与值的映射关系
    *错误返回一个负数，成功返回0
    '''    
    def insert(self,table:str,data:dict)->int:
        try:
            cursor=self.conn.cursor()
            try:
            #parse the data
                keys=""
                values=""
                for key,value in data.items():
                    keys+=(key+',')
                    if type(value)==str:
                        value="'"+value+"'"
                    else:
                        value=str(value)
                    values+=(value+',')
                keys=keys[:-1]
                values=values[:-1]
            except Exception as e:
                print(Fore.RED+"parse data error:"+str(e))
                return -1
            try:
                sql_sentense=("insert into %s (%s) values (%s)")%(table,keys,values )
                cursor.execute(sql_sentense)
                self.conn.commit()
            except Exception as e:
                print((Fore.RED+"SQL INSERT ERROR:%s\ntrace:%s")%(sql_sentense,str(e)))
                return -2
            else:
                return 0
        except Exception as e:
            print(Fore.LIGHTYELLOW_EX+"SQL INSERT unkown error:"+str(e))
            return -3
    
    def update(self,table:str,set_list:dict,condition:str)->int:
        try:
            #process arguments
            if condition is None:
                return 1
            else:
                condition="where "+condition
            set_str=''
            for k,v in set_list.items():
                if type(v)==str:
                    v="'"+v+"'"
                temp_str=k+'='+v
                set_str+=temp_str+','
            set_str=set_str[:-1]
                
            
            cursor=self.conn.cursor()
            sql_sentense=("UPDATE %s "
                          "SET %s %s")%(table,set_str,condition)
            try:
                cursor.execute(sql_sentense)
                self.conn.commit()
            except Exception as e:
                print((Fore.RED+"SQL UPDATE ERROR:%s\ntrace:%s")%(sql_sentense,str(e)))
                return -1
            else:
                return 0
        except Exception as e:
            print(Fore.LIGHTYELLOW_EX+"SQL SELECT unknown error:"+str(e))
            return -2


    '''
    #删除表中的数据：
        若未找到数据返回-1
        若condition为空返回-2
        其它错误返回-3
    '''
    def delete(self,table:str,condition:str):
        if condition == "":
            return -2
        if self.count(table,condition) <= 0:
            return -1
        else:
            condition = " where "+condition
            cursor = self.conn.cursor()
            sql_sentense = f"delete from {table} {condition} "
            try:
                cursor.execute(sql_sentense)
                self.conn.commit()
            except Exception as e:
                print(Fore.RED+"SQL Delete Error: "+str(e))
                return -3
            else:
                return 0