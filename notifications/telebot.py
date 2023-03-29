import json
import os
import asyncio
from aiogram import Bot
from minio import Minio


with open(os.getcwd() + '/telegram.json') as tg:
    telegram_json = json.loads(tg.read())

count_env: int = telegram_json['base']['count_env']
env1: str = telegram_json['base']['environment_1']
env2: str = telegram_json['base']['environment_2']
api_token: str = telegram_json['telegram']['token']
chat_id: str = telegram_json['telegram']['chat']
run_name: str = telegram_json['base']['runName']
minio_bucket: bool = telegram_json['minio']['minio']
url: str = telegram_json['minio']['url']
access_key: str = telegram_json['minio']['access_key']
secret_key: str = telegram_json['minio']['secret_key']
bucket_name: str = telegram_json['minio']['bucket_name']

PATH_ALLURE_REPORT_from_env_1: str = telegram_json['base']['allureFolder_env_1']
PATH_ALLURE_REPORT_from_env_2: str = telegram_json['base']['allureFolder_env_2']
bot = Bot(api_token)


def notification_text(launch_name: str, env: str, total_tests: int, passed_tests: int, failed_tests: int, skipped_tests: int, report_link: str) -> str:
    notification: str = f"Название прогона: {launch_name}\n" \
                   f"Окружение: {env}\n" \
                   f"Общее количество тестов: {total_tests}\n" \
                   f"Пройдено: {passed_tests}\n" \
                   f"Упало: {str(failed_tests)}\n" \
                   f"Отложено: {skipped_tests}\n" \
                   f"Ссылка на отчет: {report_link}"

    return notification


def notification_error():
    text_error: str = "Неверная конфигурация файла telegram.json, настройте конфигурацию согласно инструкции https://github.com/MikhailStrelnikov90/TelegramBotAllure/blob/main/README.md"

    return text_error


async def send_notification_to_telegram_without_minio():
    path_env_1: str = os.path.split(os.getcwd())[0] + PATH_ALLURE_REPORT_from_env_1
    path_env_2: str = os.path.split(os.getcwd())[0] + PATH_ALLURE_REPORT_from_env_2

    try:
        with open(path_env_1) as sm:
            summary_json_env_1 = json.loads(sm.read())

        total_tests_from_env_1: int = int(summary_json_env_1['statistic']['total'])
        passed_tests_from_env_1: int = int(summary_json_env_1['statistic']['passed'])
        failed_tests_from_env_1: int = int(summary_json_env_1['statistic']['failed']) + int(summary_json_env_1['statistic']['broken'])
        skipped_tests_from_env_1: int = int(summary_json_env_1['statistic']['skipped'])
        report_link_from_env_1: str = telegram_json['base']['reportLink_env_1']

        with open(path_env_2) as smr:
            summary_json_env_2 = json.loads(smr.read())

        total_tests_from_env_2: int = int(summary_json_env_2['statistic']['total'])
        passed_tests_from_env_2: int = int(summary_json_env_2['statistic']['passed'])
        failed_tests_from_env_2: int = int(summary_json_env_2['statistic']['failed']) + int(summary_json_env_2['statistic']['broken'])
        skipped_tests_from_env_2: int = int(summary_json_env_2['statistic']['skipped'])
        report_link_from_env_2: str = telegram_json['base']['reportLink_env_2']

        if count_env == 1:
            notification: str = notification_text(run_name, env1, total_tests_from_env_1, passed_tests_from_env_1, failed_tests_from_env_1, skipped_tests_from_env_1, report_link_from_env_1)
            await bot.send_message(chat_id, notification)
        elif count_env == 2:
            notification: str = f"{notification_text(run_name, env1, total_tests_from_env_1, passed_tests_from_env_1, failed_tests_from_env_1, skipped_tests_from_env_1, report_link_from_env_1)}" \
            f"\n" \
            f"\n" \
            f"{notification_text(run_name, env2, total_tests_from_env_2, passed_tests_from_env_2, failed_tests_from_env_2, skipped_tests_from_env_2, report_link_from_env_2)}"
            await bot.send_message(chat_id, notification)
        else:
            await bot.send_message(chat_id, notification_error())

    except FileNotFoundError:
        if count_env == 1:
            text_error: str = f"Файл summary.json не найден по указанному пути: {path_env_1}, генерация отчета завершилась с ошибкой или путь указан неверно"
        else:
            text_error: str = f"Файл summary.json не найден по указанному пути: {path_env_1} или {path_env_2}, генерация отчета завершилась с ошибкой или путь указан неверно"
        await bot.send_message(chat_id, text_error)


async def send_notification_to_telegram_with_minio():

    client = Minio(endpoint=url, access_key=access_key, secret_key=secret_key)
    object_from_1st_bucket = client.get_object(bucket_name, PATH_ALLURE_REPORT_from_env_1)
    summary_env_1 = object_from_1st_bucket.data.decode()
    summary_json_env_1 = json.loads(summary_env_1)

    total_tests_from_env_1: int = int(summary_json_env_1['statistic']['total'])
    passed_tests_from_env_1: int = int(summary_json_env_1['statistic']['passed'])
    failed_tests_from_env_1: int = int(summary_json_env_1['statistic']['failed']) + int(summary_json_env_1['statistic']['broken'])
    skipped_tests_from_env_1: int = int(summary_json_env_1['statistic']['skipped'])
    report_link_from_env_1: str = telegram_json['base']['reportLink_env_1']

    object_from_2nd_bucket = client.get_object(bucket_name, PATH_ALLURE_REPORT_from_env_2)
    summary_env_2 = object_from_2nd_bucket.data.decode()
    summary_json_env_2 = json.loads(summary_env_2)

    total_tests_from_env_2: int = int(summary_json_env_2['statistic']['total'])
    passed_tests_from_env_2: int = int(summary_json_env_2['statistic']['passed'])
    failed_tests_from_env_2: int = int(summary_json_env_2['statistic']['failed']) + int(summary_json_env_2['statistic']['broken'])
    skipped_tests_from_env_2: int = int(summary_json_env_2['statistic']['skipped'])
    report_link_from_env_2: str = telegram_json['base']['reportLink_env_2']

    if count_env == 1:
        notification: str = notification_text(run_name, env1, total_tests_from_env_1, passed_tests_from_env_1, failed_tests_from_env_1, skipped_tests_from_env_1, report_link_from_env_1)
        await bot.send_message(chat_id, notification)
    elif count_env == 2:
        notification: str = f"{notification_text(run_name, env1, total_tests_from_env_1, passed_tests_from_env_1, failed_tests_from_env_1, skipped_tests_from_env_1, report_link_from_env_1)}" \
                            f"\n" \
                            f"\n" \
                            f"{notification_text(run_name, env2, total_tests_from_env_2, passed_tests_from_env_2, failed_tests_from_env_2, skipped_tests_from_env_2, report_link_from_env_2)}"
        await bot.send_message(chat_id, notification)
    else:
        await bot.send_message(chat_id, notification_error())


async def send_notification_to_telegram():
    match minio_bucket:
        case True:
            await send_notification_to_telegram_with_minio()
        case False:
            await send_notification_to_telegram_without_minio()
        case _:
            await bot.send_message(chat_id, notification_error(), disable_notification=True)


if __name__ == '__main__':
    asyncio.run(send_notification_to_telegram())
