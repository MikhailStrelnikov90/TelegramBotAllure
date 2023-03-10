import requests
import json
import os
from minio import Minio
from aiogram import Bot, Dispatcher


with open(os.getcwd() + '/telegram.json') as tg:
    telegram_json = json.loads(tg.read())

count_env = telegram_json['base']['count_env']
env1 = telegram_json['base']['environment_1']
env2 = telegram_json['base']['environment_2']
api_token = telegram_json['telegram']['token']
chat_id = telegram_json['telegram']['chat']
run_name = telegram_json['base']['runName']
minio_bucket = telegram_json['minio']['minio']
url = telegram_json['minio']['url']
access_key = telegram_json['minio']['access_key']
secret_key = telegram_json['minio']['secret_key']
bucket_path = telegram_json['minio']['bucket_path']

PATH_ALLURE_REPORT_from_env_1 = telegram_json['base']['allureFolder_env_1']
PATH_ALLURE_REPORT_from_env_2 = telegram_json['base']['allureFolder_env_2']
bot = Bot(api_token)
dp = Dispatcher(bot)


def send_notification_to_telegram():

    if minio_bucket:
        client = Minio(endpoint=url, access_key=access_key, secret_key=secret_key)
        object_from_1st_bucket = client.get_object(bucket_path, f'{PATH_ALLURE_REPORT_from_env_1}/summary.json')
        summary_env_1 = object_from_1st_bucket.data.decode()
        summary_json_env_1 = json.loads(summary_env_1)
    else:
        with open(os.path.split(os.getcwd())[0] + f'/{PATH_ALLURE_REPORT_from_env_1}/summary.json') as sm:
            summary_json_env_1 = json.loads(sm.read())

    total_tests_from_env_1 = summary_json_env_1['statistic']['total']
    passed_tests_from_env_1 = summary_json_env_1['statistic']['passed']
    failed_tests_from_env_1 = int(summary_json_env_1['statistic']['failed']) + int(summary_json_env_1['statistic']['broken'])
    skipped_tests_from_env_1 = summary_json_env_1['statistic']['skipped']
    report_link_from_env_1 = telegram_json['base']['reportLink_env_1']

    notification_text_with_one_env = f"Название прогона: {run_name}\n" \
                                        f"Окружение: {env1}\n" \
                                        f"Общее количество тестов: {total_tests_from_env_1}\n" \
                                        f"Пройдено: {passed_tests_from_env_1}\n" \
                                        f"Упало: {str(failed_tests_from_env_1)}\n" \
                                        f"Отложено: {skipped_tests_from_env_1}\n" \
                                        f"Ссылка на отчет: {report_link_from_env_1}"

    if count_env == 1:
        requests.post(url=f"https://api.telegram.org/bot{api_token}/sendMessage", data=json.dumps({"chat_id": chat_id, "text": notification_text_with_one_env, "disable_notification": True}),
                      headers={'Content-Type': 'application/json'})

    if count_env == 2:
        if minio_bucket:
            client = Minio(endpoint=url, access_key=access_key, secret_key=secret_key)
            object_from_2nd_bucket = client.get_object(bucket_path, f'{PATH_ALLURE_REPORT_from_env_2}/summary.json')
            summary_env_2 = object_from_2nd_bucket.data.decode()
            summary_json_env_2 = json.loads(summary_env_2)
        else:
            with open(os.path.split(os.getcwd())[0] + f'/{PATH_ALLURE_REPORT_from_env_2}/widgets/summary.json') as sm:
                summary_json_env_2 = json.loads(sm.read())

        total_tests_from_env_2 = summary_json_env_2['statistic']['total']
        passed_tests_from_env_2 = summary_json_env_2['statistic']['passed']
        failed_tests_from_env_2 = int(summary_json_env_2['statistic']['failed']) + int(summary_json_env_2['statistic']['broken'])
        skipped_tests_from_env_2 = summary_json_env_2['statistic']['skipped']
        report_link_from_env_2 = telegram_json['base']['reportLink_env_2']

        notification_text_with_two_env = f"Название прогона: {run_name}\n" \
                                    f"Окружение: {env1}\n" \
                                    f"Общее количество тестов: {total_tests_from_env_1}\n" \
                                    f"Пройдено: {passed_tests_from_env_1}\n" \
                                    f"Упало: {str(failed_tests_from_env_1)}\n" \
                                    f"Отложено: {skipped_tests_from_env_1}\n" \
                                    f"Ссылка на отчет: {report_link_from_env_1}\n" \
                                    f"\n" \
                                    f"\n" \
                                    f"Название прогона: {run_name}\n" \
                                    f"Окружение: {env2}\n" \
                                    f"Общее количество тестов: {total_tests_from_env_2}\n" \
                                    f"Пройдено: {passed_tests_from_env_2}\n" \
                                    f"Упало: {str(failed_tests_from_env_2)}\n" \
                                    f"Отложено: {skipped_tests_from_env_2}\n" \
                                    f"Ссылка на отчет: {report_link_from_env_2}\n" \


        requests.post(url=f"https://api.telegram.org/bot{api_token}/sendMessage", data=json.dumps({"chat_id": chat_id, "text": notification_text_with_two_env, "disable_notification": True}), headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    send_notification_to_telegram()
