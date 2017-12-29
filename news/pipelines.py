# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from MySQLdb.cursors import DictCursor
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


class NewsPipeline(object):
    def process_item(self, item, spider):
        if item['content']:
            for p in item['content']:
                p.strip('\\n')
                p.strip('\\t')
            return item
        else:
            raise DropItem("Missing content in %s" % item)

class WebcrawlerScrapyPipeline(object):
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''

    # def __init__(self):
    #     self.conn = MySQLdb.connect(host="39.106.28.174", user="root", passwd="root", db="chinese_study", charset="utf8")
    #     self.cursor = self.conn.cursor()

    def __init__(self, dbpool):
        self.dbpool = dbpool
    #
    @classmethod
    def from_settings(cls, settings):
    #     '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
    #        2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
    #        3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
    #     #读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        if item['source']:
            item['source'] = item['source'][0]
        if item['img_url']:
            item['img_url'] = item['img_url'][0]
        else:
            item['img_url'] = ''
        if item['type']:
            item['type'] = item['type'][0]
        if item['desc']:
            item['desc'] = item['desc'][0]
        else:
            item['desc'] = ''
        if item['time']:
            item['time'] = item['time'][0].replace(u'\u53d1\u5e03\u65f6\u95f4\uff1a','')
            print item['time']
        if item['content']:
            item['content'] = ','.join(item['content'])
        # sql = "insert into yw_news (`title`,`url`,`source`,`time`,`img_url`,`desc`,`type`) values(%s,%s,%s,%s,%s,%s,%s)"
        # params = (item['title'], item['url'], item['source'], item['time'], item['img_url'], item['desc'], item['type'])
        # self.cursor.execute(sql, params)
        # self.conn.commit()
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):
        sql = "insert into yw_news (`title`,`url`,`source`,`time`,`img_url`,`desc`,`type`,`content`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['title'], item['url'], item['source'] ,item['time'] ,item['img_url'] ,item['desc'], item['type'],item['content'])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue
