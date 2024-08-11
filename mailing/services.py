import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from django.core.mail import send_mail

from config import settings
from config.settings import CACHE_ENABLED
from mailing.models import Mailing, MailingTry, Client


# Функция старта периодических задач
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(status__in=[0, 1])

    for mailing in mailings:
        # Если достигли end_date, завершить рассылку
        if mailing.last_send_datetime and current_datetime >= mailing.last_send_datetime:
            mailing.status = 3
            mailing.save()
            continue

        if mailing.next_send_datetime and current_datetime >= mailing.next_send_datetime:
            mailing.status = 1
            clients = mailing.clients.all()
            try:
                send_mail(
                    subject=mailing.message.mail_theme,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                MailingTry.objects.create(
                    mailing=mailing,
                    status=True,
                    response='',
                    try_datetime=datetime.now(zone)
                )

            except smtplib.SMTPException as e:
                print(f"Ошибка при отправке письма: {e}")
                MailingTry.objects.create(
                    mailing=mailing,
                    status=False,
                    response=str(e),
                    try_datetime=datetime.now(zone)
                )

                # Обновление времени следующей отправки
            if mailing.period == 1:
                mailing.next_send_datetime += timedelta(minutes=1)
            elif mailing.period == 60:
                mailing.next_send_datetime += timedelta(hours=1)
            elif mailing.period == 1440:
                mailing.next_send_datetime += timedelta(days=1)
            elif mailing.period == 10080:
                mailing.next_send_datetime += timedelta(weeks=1)
            elif mailing.period == 43200:
                mailing.next_send_datetime += timedelta(days=30)

            mailing.save()


def get_uniq_clients_count():
    if CACHE_ENABLED:
        key = 'uniq_clients_count'
        uniq_clients_count = cache.get(key)
        if uniq_clients_count is None:
            clients = Client.objects.all()
            email_list = []
            for client in clients:
                email_list.append(client.email)
            uniq_clients_count = len(set(email_list))
            cache.set(key, uniq_clients_count, timeout=60)
    else:
        clients = Client.objects.all()
        email_list = []
        for client in clients:
            email_list.append(client.email)
        uniq_clients_count = len(set(email_list))
    return uniq_clients_count


def get_mailings_counts():
    if CACHE_ENABLED:
        key_1 = 'mailings_count'
        key_2 = 'active_mailings_count'
        mailings_count = cache.get(key_1)
        active_mailings_count = cache.get(key_2)
        if mailings_count or active_mailings_count:
            mailings = Mailing.objects.all()
            mailings_count = mailings.count()
            active_mailings_count = mailings.filter(status=1).count()
            cache.set(key_1, mailings_count, timeout=60)
            cache.set(key_2, active_mailings_count, timeout=60)
    else:
        mailings_count = Mailing.objects.all().count()
        active_mailings_count = Mailing.objects.filter(status=1).count()
    return mailings_count, active_mailings_count
