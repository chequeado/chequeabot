# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
from credentials import CONN_DATA

class MySQLPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user = CONN_DATA['user'], \
            passwd = CONN_DATA['password'], \
            db = CONN_DATA['db'], \
            host = CONN_DATA['host'], \
            charset='utf8')
        
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        query = """SELECT EXISTS(SELECT 1 FROM feed_entries WHERE url = '%s')""" % item['noticia_url']
        self.cur.execute(query)
        existing_entry = self.cur.fetchone()[0]
        if not existing_entry:
            self.cur.execute(
            """INSERT INTO feed_entries 
            (url, source, seccion, entry_date, format, title, entry_text) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (item['noticia_url'], 
                item['source'], 
                item['seccion'] if "seccion" in item else "", 
                item['fecha'], 
                item['formato'], 
                item['titulo'], 
                item['noticia_texto']))
            
            self.conn.commit()
            
        return item
