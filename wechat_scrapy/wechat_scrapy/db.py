import mysql.connector

cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='wechatcollector')

def getAllKey():
    sql = """
        select *
        from search_key;
    """
    cursor = cnx.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

# cnx.close()
