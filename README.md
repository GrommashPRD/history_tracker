_"# history_tracker" 

History_Tracker - Веб сервис который принимает ссылки по POST запросу и выдает уникальные домены по GEt запросу.

1. Клонируете репозиторий командой -git clone https://github.com/GrommashPRD/history_tracker.git
2. Откройте папку проекта в терминале.
3. Создайте виртуальное окружение. python -m venv venv
4. Активируйте виртуальное окружение. source env/bin/activate
5. Установите зависимости из файла. "requirements.txt". pip install -r requirements.txt
6. Создайте миграции для БД. python manage.py makemigrations
7. Запустите миграции. python manage.py migrate
8. Запустите проект на локальном сервере. python3 manage.py runserver
9. Перейдите по ссылке. http://127.0.0.1:8000/
10. Создайте superuser'а. python manage.py createsuperuser
11. Введите Username: , Email address: , Password: , Password (again):
12. Перейдите по ссылке http://127.0.0.1:8000/admin и авторизуйтесь, чтобы создать свою запись через админ-панель.
13. По ссылке http://127.0.0.1:8000/visited_links/ используя POST запрос, Вы, можете добавить новые адресса, как ссылкой, так и одной строкой.
14. По ссылке http://127.0.0.1:8000/visited_domains/?from=1737868909&to=1737869227, по GET запросу, Вы,  можете получить список уникальных доменов за определенное время, где from & to - Кол-во секунд прошедших с начала эпохи. (FROM < TO)_