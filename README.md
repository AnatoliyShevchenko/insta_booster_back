# insta_booster_back
Backend for instagram booster

# Описание:
Сервис по накрутке просмотров/лайков/комментариев в запрещенограме.
Не судите строго, я зарегался в нем в тот же день как начал работу, то есть сегодня.
Сервис написан на FastAPI.

# Перед запуском:
Для работы бустера необходимо установить браузер Тор, будем проксировать каждого пользователя:
- sudo apt install tor
далее, надо придумать пароль который мы запишем в .env файл и захэшировать его:
- tor --hash-password YOUR_PASSWORD
Открываем файл конфигурации Тор:
- sudo nano /etc/tor/torrc
Раскомментируем или дописываем:
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
CookieAuthentication 1

Запускаем тор: 
- sudo service tor start

Возможно сервис надо будет перезапустить.

Установка Хрома:
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

Проект использует базу данных PostgreSQL, у меня на сервере она установлена нативно, поэтому в докер композ ее пихать не будем.
Клонируем репозиторий, создаем в корневой директории файл .env, там должны быть следующие данные:
    - DB_NAME = "название базы данных"
    - DB_USER = "имя пользователя"
    - DB_PASS = "пароль пользователя"
    - DB_HOST = "127.0.0.1"
    - DB_PORT = "5432"
    - TOR_PASSWORD = "пароль браузера Тор не хэшированный"

В принципе все готово, сам проект развернем в контейнере.
