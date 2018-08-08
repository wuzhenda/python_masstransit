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
import json
import pickle


class MsgEvent:
    def __init__(self,EvCode,ElevatorID,MsgBody):
        self.EvCode = EvCode
        self.ElevatorID = ElevatorID
        self.MsgBody = MsgBody


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

    def SendEvent(self):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
        """
        msgEvent=MsgEvent(0x06,'0000000000000002','1')
        bodyMsg = pickle.dumps(msgEvent)
        print(bodyMsg)
        channel = self.__GetConnect()
        channel.basic_publish(exchange='DTrms.Protocol.Messaging:MsgEvent',routing_key='',body=bodyMsg,properties=pika.BasicProperties(
                                content_type = "text/plain"
                                ))
        print(msgEvent)
        channel.close()

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
    ramq.SendEvent()
        

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








