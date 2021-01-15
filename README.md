# avsoft

### Требования


[Python](https://www.python.org/downloads/) v3.7 +  для запуска.
[Docker](https://www.docker.com/)

### Для запуска сервиса нужно выполнить следующие действия:
Выполнить команду в командной строке:
```sh
$ docker-compose up --build
```

После сборки образа открыть два окна в командной строке, в первом окне выполнить команду для запуска консумера "Error Handler":
```sh
$ docker exec <CONTAINER ID> python Error_Handler.py
```

Во втором окне выполнить команду для запуска продюсера:
```sh
$ docker exec <CONTAINER ID> python main.py
```

Так же имеется скрипт-парсер данных:
```sh
$ docker exec <CONTAINER ID> python pars.py
```
Консумер Parser запускается при сборке контейнеров

## Авторы

* **Vladimir Svetlakov** - [svvladimir-ru](https://github.com/svvladimir-ru)
