import pika
import os
import time
from pars import file_pars

FILE_EXPANSION = '.txt'
file_folder = os.listdir(path="/code/files")

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'rabbitmq-container'))  # подключение к базе rebbitmq

print(f'Подключились к базе rebbitmq {connection}')
channel = connection.channel()  # rebbitmq
channel.queue_declare(queue='Parsing')
channel.queue_declare(queue='Errors')


def main():
    if len(file_folder) != 0:
        print('Папка files не пустая, проходимся по ней циклом')
        for i in file_folder:
            if i.endswith(FILE_EXPANSION) is True:
                print(f'Добавили в обработчик файл {i}')
                channel.basic_publish(exchange='',
                                      routing_key='Parsing',
                                      body=i,
                                      )
            else:
                print(f'Добавили в обработчик файл {i}')
                channel.basic_publish(exchange='',
                                      routing_key='Errors',
                                      body=i,
                                      )
            print(f'Удалили файл {i}')
            os.remove(f'files/{i}')
    print('Новых файлов нет!')
    connection.close()


if __name__ == '__main__':
    main()
    time.sleep(30)
    print('Выполняю парсинг с сайта')
    file_pars()
