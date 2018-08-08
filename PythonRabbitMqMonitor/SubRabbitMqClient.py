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

def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print()
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


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

    def StartConsumeEvent(self):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        调用示例：
        """       
        channel = self.__GetConnect()
        #channel.queue_declare(queue='DTrms.EventConsumerQueue')
        channel.basic_consume(on_message,queue='DTrms.EventConsumerQueue')
        channel.start_consuming()  # 开始消费消息
        

    def ToCVSFile(ch,method,properties,body):  # 四个参数为标准格式
        print('run here')
        print(ch, method, properties)  # 打印看一下是什么
        # 管道内存对象  内容相关信息  后面讲
        print(" [x] Received %r" % body)
        time.sleep(15)
        ch.basic_ack(delivery_tag = method.delivery_tag)  # 告诉生成者，消息处理完成


def consumerJob():
    print('Tick! The time is: %s' % datetime.datetime.now())
    ramq = RabbitMQ(host='10.0.0.155',user="inner_test",pwd="123456",vhost="innertest")
    ramq.StartConsumeEvent()
        

def main():
    #scheduler = BlockingScheduler()
    #scheduler.add_job(consumerJob,'cron',second='5',minute='*',hour='*')
    consumerJob()
    print('Press--- Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except KeyboardInterrupt as SystemExit:
        scheduler.shutdown()


if __name__ == '__main__':
    main()








