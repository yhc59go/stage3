
from mysql.connector import pooling
import os
from dotenv import load_dotenv

class communicateWithRDS():
    load_dotenv()
    databaseUsername=os.getenv("databaseUsername")
    databasePassword=os.getenv("databasePassword")
    endPoint=os.getenv("endPoint")
    
    def __init__(self,databaseName,pool_name):
        self.databaseName=databaseName
        self.db_config = {
            "user": communicateWithRDS.databaseUsername,
            "password": communicateWithRDS.databasePassword,
            "host": communicateWithRDS.endPoint,
            "database": self.databaseName,
            "raise_on_warnings": True,
        }
        self.cnx_pool = pooling.MySQLConnectionPool(
                    pool_name=pool_name,
                    pool_size=15,
                    pool_reset_session=True,
                    **self.db_config)

    def createTabel_messageBoard(self):
        #===== 建立資料表 =====#
        try:
            # 獲取連接
            connection = self.cnx_pool.get_connection()
            # 建立 cursor
            cursor = connection.cursor()
            # 建立資料表
            table = "CREATE TABLE messageBoard (message_content TEXT, image TEXT)"
            cursor.execute(table)
        except Exception as e:
            print(e)
        finally: 
            # 關閉 cursor 和連接
            cursor.close()
            connection.close()

    def InsertToTabel_messageBoard(self,message_text,message_imageURL):
        #===== 插入一筆資料 =====#
        try:
            connection = self.cnx_pool.get_connection() #get connection from connect pool
            cursor = connection.cursor()
            sql ="INSERT INTO messageBoard(message_content,image)VALUES (%s, %s);"
            val=(message_text,message_imageURL) 
            cursor.execute(sql,val)
            count = cursor.rowcount
            connection.commit()
        except Exception as e:
            print(e)
        finally: # must close cursor and conn!!
            cursor.close()
            connection.close()
        return count 
