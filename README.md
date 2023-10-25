# Проект Foodgram
Foodgram — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд, а затем осуществлять его выгрузку в формате .txt.

Проект состоит из бэкенд-приложения на Django и фронтенд-приложения на React.

Данный проект доступен по адресу ```https://foodgramyadiploma.hopto.org/```

# Установка
Клонировать репозиторий на свой компьютер:
```
git clone git@github.com:Dyabolo-light/foodgram-project-react.git
```
Подключение к удалённому серверу по SSH-ключу в формате:
```
ssh -i путь_до_SSH_ключа/название_файла_с_SSH_ключом_без_расширения login@ip
```
На сервере должен быть установлен Docker:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```
Дополнительно установите утилиту Docker compose: 
```
sudo apt-get install docker-compose-plugin
```
Проверьте, что Doker работает (```sudo systemctl status docker```).

На сервере создайте папку для проекта (```mkdir foodgram```) и файл с переменными окружения .env (```touch .env```).

В файле .env необходимо указать следующую информацию:
```
SECRET_KEY=<Ваш секретный код>
ALLOWED_HOSTS=<IP вашего сервера и html вашего сайта>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Ваш пароль>
DB_HOST=db
DB_PORT=5432
```
Из папки infra на вашем компьютере необходимо скопировать файлы на сервер:
```
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```
Для запуска сайте необходимо ввести в терминале сервера следующую команду:
```
sudo docker compose up -d
```
