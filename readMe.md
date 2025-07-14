В проекте используется gettext для переводов. 

**Установка на windows:**
https://mlocati.github.io/articles/gettext-iconv-windows.html
скачаем и устанавливаем

**Установка на linux (Ubuntu/Debian):**
sudo apt-get update
sudo apt-get install gettext

**Установка на macOs (с Homebrew):**
brew install gettext
brew link --force gettext

**Проверка установки:**
msguniq --version

**Команды для создание переводов (В основном используется вторая команда. Он создает переводы из файла django.po на файл django.mo):**
python manage.py makemessages -l ru
python manage.py compilemessages

Это технология переводит системные команды. Файлы конфигурации находятся на папке: 
locale/ru/LC_MESSAGES

**Тестовый пароль для клиента:**
Renter123

**Тестовый пароль для арендадатора:**
RClient123