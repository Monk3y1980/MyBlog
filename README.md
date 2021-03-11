#Blog

<b>1. Make Project</b>
<br>

pip3 install django
django-admin startproject NewsPaper -> cd NewsPaper

python3 manage.py migrate
python3 manage.py startapp news
pip3 freeze > requirements.txt
если имеется готовый файл с зависимостями
pip install -r requirements.txt
python3 manage.py createsuperuser
python3 manage.py runserver

<b>2. Make Models</b>
<br>
python3 manage.py makemigrations
python3 manage.py migrate

<b>3. Команды для создания переводов</b>
# make .po file
python3 manage.py makemessages -l ru или
python3 manage.py makemessages --all
# compile file
python3 manage.py compilemessages


python3 manage.py update_translation_fields