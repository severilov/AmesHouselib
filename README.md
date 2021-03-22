# severilov.pa

### Task 1

Документирование проектов с помощью  Sphinx. Создание HTML страницы с документацией.
Тестирование на файле ./task1/statemachine.py

Важные ссылки:
* https://github.com/nvie/gitflow
* http://docs.python-guide.org/en/latest/writing/documentation/
* https://gitlab.com/pages/sphinx

### Task 2

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
