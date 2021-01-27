import time
time.sleep(10)
from sqlalchemy.orm.session import sessionmaker
from database import engine, Parser
import pika
import os
import re
import csv


"""подключение к mysql"""
session = sessionmaker(bind=engine)()


"""подключение к rebbitmq"""
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq-container'))
channel = connection.channel()
channel.queue_declare(queue='Parsing')


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
    print(f'Получили файл {i} в обработчик parsing\nдекодировали файл {i}\nоткрыли файл {i}')
    with open(f'files/{i}', 'r') as file:  # чтение файлов
        data = file.readlines()
        s = ''.join(data).strip('\n')  # строка из файла
        d = re.split(r'[^А-яA-z]', s)  # убираю все символы
        print('Получили все строки успешно избавились от лишних символов')
        for words in d:
            if words != '':  # убираю пустые строки
                '''добавление в базу слов'''
                print('Начало добавления слов в базу')
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
                    print(f'Счетчик слова {word} дошел до 2\nДобавляем слово в файл csv')
                    """счётчик, если количество слов доходит до 2ух добавляем его в csv
                    удаляем значение из базы"""
                    items = [{'word': word.name, 'file_name': word.file_name}]
                    print(f'Удалили слово {word} из базы')
                    session.delete(word)
                    session.commit()
                    save_file(items)
    # if i != 'requirements.txt':
    print(f'Удаляем файл {i}')
    os.remove(f'files/{i}')  # удаление файла
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume('Parsing',
                      callback,)

channel.start_consuming()
