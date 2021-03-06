# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:07:36 2018

@author: Henry Wu
"""

import pika
import csv
import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


class RabbitMQ:
    def __init__(self,host,user,pwd,vhost):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.vhost = vhost

    def __GetConnect(self):
        """
        得到连接信息
        返回: connection.channel()
        """
        credentials=pika.credentials.PlainCredentials(self.user,self.pwd)
        pika_conn_params = pika.ConnectionParameters(self.host,5672,self.vhost,credentials)
        connection = pika.BlockingConnection(pika_conn_params)
        self.channel = connection.channel()

        if not self.channel:
            raise(NameError,"连接rabbitmq失败")
        else:
            return self.channel

    def ExecQuery(self):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
        """
        channel = self.__GetConnect()
        agent_queue = channel.queue_declare(queue="DTrms.AgentQueue", durable=True,exclusive=False, auto_delete=False)
        consumer_queue = channel.queue_declare(queue="DTrms.ConsumerQueue", durable=True,exclusive=False, auto_delete=False,arguments={'x-max-priority':3})        
        event_queue = channel.queue_declare(queue="DTrms.EventConsumerQueue", durable=True,exclusive=False, auto_delete=False)
        queue_st="{0},{1},{2}".format(agent_queue.method.message_count,consumer_queue.method.message_count,event_queue.method.message_count)
        print(queue_st)
        ret=[datetime.datetime.now(),agent_queue.method.message_count,consumer_queue.method.message_count,event_queue.method.message_count]
        return ret

    def ToCVSFile(self,cvsFilename,dblist):
        """
        save to cvs documents
        """
        with open(cvsFilename, 'a',encoding='utf8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(dblist)           
                
def quiryDbJob():
    print('Tick! The time is: %s' % datetime.datetime.now())
    ramq = RabbitMQ(host='10.0.0.155',user="inner_test",pwd="123456",vhost="innertest")
    resList = ramq.ExecQuery()
    ramq.ToCVSFile("queueSt.csv",resList)
    

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(quiryDbJob,'cron',second='5',minute='*',hour='*')
    print('Press--- Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except KeyboardInterrupt as SystemExit:
        scheduler.shutdown()


if __name__ == '__main__':
    main()








