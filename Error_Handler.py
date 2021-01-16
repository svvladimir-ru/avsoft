import pika
import os
import smtplib


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'rabbitmq-container'))  # подключение к базе rebbitmq
channel = connection.channel()  # rebbitmq

channel.queue_declare(queue='Errors')


def callback(ch, method, properties, body):
    i = body.decode('utf-8')
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('email@gmail.com', 'pass')
    smtpObj.sendmail("email@gmail.com", "email@gmail.com", f"file {i} not txt!")
    smtpObj.quit()
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume('Errors',
                      callback, )

channel.start_consuming()
