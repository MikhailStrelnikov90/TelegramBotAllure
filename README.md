# TelegramBotAllure
Телеграм-бот для отправки уведомлений о результатах прохождения автоматизированных тестов в Allure

1. Автоматизированные тесты с подключенным инструментом для составления отчетности запускаются командой pytest --alluredir=./allure-results ./tests/, где ./tests/ - путь к папке, в которой лежат ваши автотесты.
2. После запуска и прохождения автоматизированных тестов составляется allure-отчет командой allure generate -c ./allure-results -o ./allure-report.
3. По итогам выполнения автотестов генерируется файл summary.json в папке allure-report/widgets. Этот файл содержит общую статистику о результатах прохождения тестов, на основании которой как раз и формируется уведомление, которое отправляет бот

Для запуска необходимо:
1. Добавить файл с зависимостями requirements.txt и папку notifications с файлами telebot.py и telegram.json в корень проекта
2. Установить зависимости командой pip install -r requirements.txt
3. Создать телеграм-бота через @BotFather
4. Добавить созданного бота в канал и назначить бота администратором
5. Заполнить в файле telegram.json следующие поля:

runName - название тест-рана (заполнение обязательно)
environment_1 - название первого окружения (заполнение обязательно)
environment_2 - название второго окружения, если запуск автотестов происходит в различных браузерах
reportLink_env_1 - URL allure-отчета для первого окружения (заполнение обязательно)
reportLink_env_2 - URL allure-отчета для второго окружения
count_env - количество окружений (если окружение одно, то установить значение 1, если два, то 2 (значение типа int и обязательно к заполнению)
allureFolder_env_1 - путь к файлу summary.json в папке с allure-отчетом (при запуске команды allure generate -c ./allure-results -o ./allure-report путь будет таким: "allure-report/widgets") (заполнение обязательно)
allureFolder_env_2 - путь к файлу summary.json в папке с allure-отчетом при запуске с несколькими окружениями (при запуске команды allure generate -c ./allure-results -o ./chrome/allure-report путь будет таким: "chrome/allure-report/widgets")

token - токен telegram-бота (присылает бот @BotFather при создании нового бота) (заполнение обязательно)
chat - id чата (Для того, чтобы узнать Chat ID, надо добавить бота в целевой чат сделать его администратором, перейти по ссылке вида https://api.telegram.org/botIDвашегобота/getUpdates, написать в чат и обновить страницу)

minio - установить true, если файл summary.json после генерации отчета попадает в MinIO
url - эндпоинт бакета в MinIO (заполнение обязательно при установлении значения true в параметре minio)
access_key - access key сервисного аккаунта в MinIO (заполнение обязательно при установлении значения true в параметре minio)
secret_key - secret key сервисного аккаунта в MinIO (заполнение обязательно при установлении значения true в параметре minio)
bucket_path - название bucket'а в MinIO (заполнение обязательно при установлении значения true в параметре minio)

6. В папке notifications выполнить команду python telebot.py

Если у вас автотесты проходятся в одном окружении, например в браузере Google Chrome, то обязательно установите в telegram.json значение 1 у параметра count_env.

Пример заполнения файла telegram.json:

```
{
  "base": {
    "runName": "Regress",
    "environment_1": "Google Chrome 110.0",
    "environment_2": "Firefox 109.0",
    "reportLink_env_1": "https://chrome-allure.ru/allure-docker-service/projects/default/reports/latest/index.html#",
    "reportLink_env_2": "https://firefox-allure.ru/allure-docker-service/projects/default/reports/latest/index.html#",
    "count_env": 2,
    "allureFolder_env_1": "chrome/allure-report/widgets",
    "allureFolder_env_2": "firefox/allure-report/widgets"
  },
  "telegram": {
    "token": "6065034703:AAHU83GhJyPrMXKr_gI7irPDB3hXYrqxFWw",
    "chat": "-965612307"
  },
  "minio": {
    "minio": false,
    "url": "",
    "access_key": "",
    "secret_key": "",
    "bucket_path": ""
  }
}
```

