# DockerTask

1. Собираю докер образ:
```docker build -t test/docker-study .```

2. Создаю сеть и присоединяю к ней контейнеры
```
docker network create master-slaves

docker network connect master-slaves master
docker network connect master-slaves slave1
docker network connect master-slaves slave2
```

3. Смотрю адреса контейнеров slave2 и slave1. Заменяю request адреса на адреса контейнеров для master.
```
docker network inspect master-slaves
```

slave1: 172.18.0.3
slave2: 172.18.0.4

По итогу:
```
t1 = threading.Thread(target=request_sender, args=[urls[:middle], 'http://172.18.0.3:8081/count', words])
t2 = threading.Thread(target=request_sender, args=[urls[middle:], 'http://172.18.0.4:8082/count', words])
```

Меняю адреса при работе с контейнером master.

4. Создаю и запускаю контейнеры
```
docker run --name master -p 8080:8080 -it test/docker-study /bin/bash
python3 wordparser.py --host 0.0.0.0 --port 8080
```
```
docker run --name slave1 -p 8081:8081 -it test/docker-study /bin/bash
python3 wordparser.py --host 0.0.0.0 --port 8081
```
```
docker run --name slave2 -p 8082:8082 -it test/docker-study /bin/bash
python3 wordparser.py --host 0.0.0.0 --port 8082
```

5. Делаю запрос
```
GET /words '{"urls": ["https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D1%8E%D0%B7_%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D1%85_%D0%A1%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA", "https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D1%8E%D0%B7_%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D1%85_%D0%A1%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA"]}'
```

6. Получаю ответ
```
{"\u0432": 2152, "\u0438": 1738, "\u0441\u0441\u0441\u0440": 1324, "\u2014": 1022, "\u2191": 732, "\u0441": 628, "\u043d\u0430": 544, "\u00bb": 522, "\u00ab": 522, "\u0433\u043e\u0434\u0430": 478}
```
