import pika
import os


FILE_EXPANSION = '.txt'
file_name = os.listdir(path=".")

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'rabbitmq-container'))  # подключение к базе rebbitmq
channel = connection.channel()  # rebbitmq
channel.queue_declare(queue='Parsing')
channel.queue_declare(queue='Errors')

for i in file_name:
    if i.endswith(FILE_EXPANSION) is True:
        channel.basic_publish(exchange='',
                              routing_key='Parsing',
                              body=i,
                              )
    else:
        channel.basic_publish(exchange='',
                              routing_key='Errors',
                              body=i,
                              )

connection.close()
