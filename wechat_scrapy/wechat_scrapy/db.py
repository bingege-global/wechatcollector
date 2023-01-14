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

def saveArticle(url, title, keyId):
    sql = """
        insert sogou_content(url, title, key_id) values('%s', '%s', '%s')
    """ % (url, title, keyId)
    cursor = cnx.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        cnx.commit()
    except:
    # 发生错误时回滚
        cnx.rollback()

def existsByUrl(url):
    sql = """
        select 1 from sogou_content where url='%s'
    """ % url
    cursor = cnx.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


# cnx.close()
