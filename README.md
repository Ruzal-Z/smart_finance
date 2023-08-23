Smart Finance
========================
Описание:
-------------------------
Smart Finance это социальная сеть с возможностью:
      регистр,
      создавать, редактировать и удалять сообщения,
      просматривать, комментировать посты других авторов,
      подписаться и отписаться от авторов.

Стек технологий:  
-------------------------
  * Python 3.9  
  * Django 2.2  
  * Pillow   
  * sorl-thumbnail  


Установка и запуск:
-------------------------
 
Клонируйте репозиторий:
```
     git clone https://github.com/devbkd/smart_finance.git
```
или используйте SSH-ключ:
```
     git clone git@github.com:devbkd/smart_finance.git
```
Установить и активировать виртуальную среду
```
     python -m venv venv
```
```
     source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt
```
     pip install -r requirements.txt
```
Сделать миграцию:
```
     python manage.py migrate
```
Запустите проект в режиме разработки:
```
     cd smart_finance/  
```
```
     python manage.py runserver
```
Откройте в своем браузере `localhost` или `127.0.0.1:8000`


## Автор:
Рузал Закиров [GitHub](https://github.com/devbkd/)