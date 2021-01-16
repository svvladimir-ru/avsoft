from sqlalchemy.orm.session import sessionmaker
from database import engine, Parser
import pika
import time
import os
import re
import csv

time.sleep(10)
"""подключение к mysql"""
session = sessionmaker(bind=engine)()


"""подключение к rebbitmq"""
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq-container'))
channel = connection.channel()
channel.queue_declare(queue='Parsing')
print(' [*] Waiting for messages. To exit press CTRL+C')


def save_file(items):
    """сохранение csv"""
    with open('word.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['слово', 'имена файлов'])
        for item in items:
            writer.writerow(
                [
                    item['word'],
                    item['file_name'],
                ]
            )


def callback(ch, method, properties, body):
    i = body.decode('utf-8')

    with open(i, 'r') as file:  # чтение файлов
        data = file.readlines()
        s = ''.join(data).strip('\n')  # строка из файла
        d = re.split(r'[^А-яA-z]', s)  # убираю все символы
        for words in d:
            if words != '':  # убираю пустые строки
                '''добавление в базу слов'''
                q = session.query(Parser).filter_by(name=words)
                word = q.first()
                if word is None:  # если слова нет в базе добавляю его
                    word = Parser(name=words, count=1, file_name=i)
                    session.add(word)
                    session.commit()
                else:  # если есть добавляю + 1 и проверка с какого он файла
                    if i == word.file_name:
                        word.count = word.count + 1
                        session.commit()
                    else:
                        word.file_name = word.file_name + ' ' + i
                        word.count = word.count + 1
                        session.commit()
                if word.count == 2:
                    """счётчик, если количество слов доходит до 2ух добавляем его в csv
                    удаляем значение из базы"""
                    items = [{'word': word.name, 'file_name': word.file_name}]
                    session.delete(word)
                    session.commit()
                    save_file(items)
    # if i != 'requirements.txt':
    os.remove(i)  # удаление файла
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume('Parsing',
                      callback,)

channel.start_consuming()
