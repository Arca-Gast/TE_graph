**ФИО участников:** Тихонов Дмитрий Александрович, Минеева Елена Андреевна  
**Группа:** БНМ-21-2  
Цифровая кафедра. Средства разработки инженерных приложений  
  
***Приложение для графического сравнения термоэлектрических материалов***  
  
### Постановка задачи: ###  
#### Цель проекта: #### 
Создание приложения для графического сравнение термоэлектрических материалов  
#### Задачи проекта: ####  
* Разработка алгоритма решения поставленной задачи;  
* Написание программного кода на языке Python;  
* Тестирование разработанного алгоритма;  
* Анализ полученных результатов  
#### Актуальность: ####
Термоэлектрические материалы имеют большое количество уже проведённых исследований, собрание их в одном месте и построение графиков поможет в выборе предмета исследования и сравнения материалов друг с другом 
  
  
### Используемые библиотеки: ###  
pymysql – библиотека для работы с базой данных MySQL;  
matplotlib - библиотека для визуализации данных двумерной и трёхмерной графикой;  
openpyxl - работа с файлами xlsx;  
pandas - в данном проекте нужен только для работы с файлами xlxs;  
json - работа с json файлами;  
csv - работа с csv файлами.  
  
### Описание работы программы: ###
Программа используется для создания графиков и хранения данных в базе данных. На вход нужен файл типа xlsx, по структуре совпадающий с файлом estm.xlsx, хранящимся в репозитории. Из этого файла выгружается информация о материалах.  

### Варианты доработки программы: ### 
Cоздание графического интерфейса для упрощения работы с ПО; перевод на тип .exe, чтобы пользователям не приходилось устанавливать Python; добавление возможности редактировать графики по своему желанию.  

# Инструкция: #  

Предварительно необходимо скачать Python и XAMPP  
Это можно сделать по следующим ссылкам:  
https://www.python.org/downloads/  
https://www.apachefriends.org/  
При установке XAMPP необходимо установить Apache, MySQL и phpmyadmin  
После скачать файлы из репозитория  
Для работы с файлом рекомендуется использовать PyCharm (использование других IDE не проверено)  
Также необходимо скачать следующие библиотеки для Python: pandas, openpyxl, matplotlib, pymysql  
Перед запуском программы необходимо запустить XAMPP Control Panel и нажать Start напротив Apache и MySQL  
При первом запуске необходимо преобразовать данные из файла estm.xlsx  
Это делается следующим образом: при запуске программы сначала ввести "Y", затем "estm"  
Дальнейшее управление интуинивно понятно
