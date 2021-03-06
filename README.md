# Тестовое задание для Backend-разработчика

Это репозиторий тестового задания на позицию Backend-разработчика. Проект представляет из себя простой сервис сбора данных из [GitHub API](https://docs.github.com/en/rest) для последующего анализа изменений в популярности репозиториев. Сервис реализован не полностью и вам необходимо довести его до ума.

## Запуск:

- Склонировать репозиторий 
- Создать файл .env, который копия .env.excemple, прописать туда переменные окружения
- Cоздать и запустить образ docker image командой: docker-compose up --build 
- После старта всех контейнеров можно переходить на host:port
- Так как я писал api на fastapi, то он сразу предоставляет документацию по адресу http://host:port/docs 

## Описание:
Проект полностью развёртывается в докере

Сначала хочу рассказать, в чем отличие моего api от данного: 
- put v1/users/ при добавление нового пользователя, автоматически прогружаются все его репозитории
- delete v1/users/ при удалении пользователя, сначала чистятся всю статистку репозиториев данного пользователя, только после, уваляет самого пользователя

Методы
- get v1/users возвращает всех пользователей в бд
- get v1/users/{Id} ищет пользователя по Id, если пользователь не найдёт вернёт 404, и сообщение «user not’t found»
- put v1/users добавляет нового пользователя в бд
- delete v1/users/{Id} удаляет всю статистику о репозиториях и о самом пользователе
- get v1/users/{Id}/stats получение информации из бд, которая обновляется раз в сутки 

В докере добавлена cron задача, которая срабатывает 1 раз в сутки и обновляет все изменения репозиториев пользователей из бд

Добавлено логирование обновлений и добавлений записей 


## Задание

Сейчас перед вами стоят следующие задачи:

1. Скопируйте этот репозиторий. Ссылку на свою копию необходимо будет предоставить рекрутеру.
2. Изучите устройство сервиса.
3. Реализуйте ежедневное сканирование репозиториев и добавление новых записей в базу данных. Сканирование следует
   выполнять только для добавленных в базу данных пользователей.
4. Реализуйте эндпоинт **/v1/users/{id}/stats**. Пусть он возвращает данные за указанный период (**date_from**, **date_to**) в следующем формате:

```json
{
  "user": {
    "id": 1428904,
    "login": "allien",
    "name": "Allien Delon"
  },
  "stats": [
    {
      "repo_id": 7329078,
      "date": "2022-06-10",
      "stargazers": 42,
      "forks": 9,
      "watchers": 14
    },
    {
      "repo_id": 7329078,
      "date": "2022-06-11",
      "stargazers": 56,
      "forks": 10,
      "watchers": 15
    }
  ]
}
```

5. Подготовьте сервис для развертывания с помощью Docker Compose.
6. Опубликуйте репозиторий с вашим доработанным вариантом и отправьте ссылку рекрутеру.


## Дополнительная информация

- Соблюдайте PEP8.
- Используйте отдельные коммиты для разных задач.
- При внесении изменений придерживайтесь семантического версионирования.
- Используйте `aiohttp` или `httpx` для сбора данных с GitHub.
- Если потребуется, внесите изменения в схему базы данных.
- Используйте Alembic и миграции для работы с базой данных.
- Если вы видите несколько вариантов решения одной и той же задачи, сделайте выбор самостоятельно.


## Стек

- Python 3.10
- PostgreSQL
- SQLAlchemy
- Alembic
- FastAPI
- Uvicorn
- httpx или aiohttp
