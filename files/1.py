import pika
import os


FILE_EXPANSION = '.txt'
file_name = os.listdir(path="")
print(file_name)
if len(file_name) == 0:
    print('None')
else:
    print('not None')