import pika
import os
import smtplib
import datetime
now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'rabbitmq-container'))  # подключение к базе rebbitmq
channel = connection.channel()  # rebbitmq

channel.queue_declare(queue='Errors')

name = 'email'  # email получателя сообщений об ошибках 
password = 'pass'  # пароль почты


def callback(ch, method, properties, body):
    i = body.decode('utf-8')
    print(f'Получили файл {i} в обработчик errors\nДекодировали файл {i}')
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(f'{name}', f'{password}')
    print(f'Соедениилсь с {smtpObj}, по логину {name}, паролю {password}')
    smtpObj.sendmail(f"{name}",
                     f"{name}",
                     f"{now}\n"
                     f"file {i} not txt!"
                     )
    print('Отправка сообщения прошла успешно')
    smtpObj.quit()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'Удалили файл {i}')
    os.remove(f'files/{i}')


channel.basic_qos(prefetch_count=1)
channel.basic_consume('Errors',
                      callback, )

channel.start_consuming()

