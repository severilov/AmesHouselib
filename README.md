# severilov.pa

### Documentations

Документирование проектов с помощью  Sphinx. Создание HTML страницы с документацией.
Тестирование на файле ./task1/statemachine.py

Важные ссылки:
* https://github.com/nvie/gitflow
* http://docs.python-guide.org/en/latest/writing/documentation/
* https://gitlab.com/pages/sphinx

### ML models, scripts, EDA

Реализовать модель, которая будет предсказывать Y по имеющимся признакам

Данные: [Ames Housing Dataset](http://jse.amstat.org/v19n3/decock/AmesHousing.txt)

Результат:
* библиотека task2/houselib/
* скрипты обучения/тестирования task2/scripts/
* сохраненные модели task2/models/
* EDA ноутбук task2/AmesHousingEDA.ipynb

Запуск скриптов:
* Запуск обучения (2006-2009), линейная регрессия `python train.py -m 'linreg'`
* Запуск обучения (2006-2009), ridge регрессия `python train.py -m 'ridge'`
* Запуск тестирования сохраненной модели на 2010 `python test.py`

Документация библиотеки: https://se_ml_course.gitlab.io/2021/severilov.pa/

### Docker usage

Structure python-docker:
```
|____ app
      |____ templates
            |____ index.html
      |____ __init__.py
      |____ views.py
|____ app.py
|____ requirements.txt
|____ Dockerfile
```

Cheat sheet:
* создать докер
```
docker build --tag docker_houselib .
```
* запустить контейнер
```
docker run -d -p 5000:5000 docker_houselib
```
* посмотреть созданные контейнеры
```
docker ps -a
```
* оставновить все контейнеры
```
docker stop $(docker ps -a -q)
```
* удалить все контейнеры
```
docker rm $(docker ps -a -q)
```
* удалить все образы
```
docker rmi $(docker images -q)
```

### Unit tests
```
|____ test
      |____ test_add_new_features.py
      |____ test_delete_outliers.py
      |____ test_fill_nan.py
      |____ test_log_target.py
      |____ test_read_data.py
      |____ test_save_load_model.py
      |____ test_script_test.sh
      |____ test_script_train.sh
|____ requirements-test.txt
```
Мутационный анализ тестов (количество выживших мутантов):
* test_add_new_features.py: 2/24
* test_delete_outliers.py: 13/45
* test_fill_nan.py: 1/7
* test_log_target.py: 2/17
* test_read_data.py: 2/22
* test_save_load_model.py: 2/29

Все неубитые мутанты оказались нерелевантны для тестирования. Большая часть из неубитых 22 мутантов связана с импортом библиотеки (строка sys.path.append('./src/')) 

Bash скрипты по тестированию скриптов обучения и тестирования отработали с выводом "OK"